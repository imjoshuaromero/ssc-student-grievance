from flask import Blueprint, request, jsonify, redirect
from backend.models.user import User
from backend.utils.auth import hash_password, verify_password, generate_token
from backend.utils.google_auth import verify_google_token, get_google_oauth_url, exchange_code_for_token
from backend.utils.email_verification import (
    generate_verification_code, 
    generate_verification_token,
    send_verification_code_email,
    send_verification_link_email
)
from backend.config.database import Database
from datetime import datetime, timedelta
import re

auth_bp = Blueprint('auth', __name__)

def validate_sr_code(sr_code):
    """Validate SR-Code format (YY-XXXXX)"""
    pattern = r'^\d{2}-\d{5}$'
    return re.match(pattern, sr_code) is not None

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new student user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['sr_code', 'email', 'password', 'first_name', 'last_name', 
                          'program', 'year_level']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Validate SR-Code format
        if not validate_sr_code(data['sr_code']):
            return jsonify({'error': 'Invalid SR-Code format. Use YY-XXXXX (e.g., 21-12345)'}), 400
        
        # Validate email
        if not validate_email(data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate year level (handle both string and int)
        try:
            year_level = int(data['year_level'])
            if year_level not in [1, 2, 3, 4]:
                return jsonify({'error': 'Year level must be between 1 and 4'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Year level must be a number between 1 and 4'}), 400
        
        # Check if user already exists
        existing_email = User.find_by_email(data['email'])
        if existing_email:
            return jsonify({'error': 'Email already registered'}), 409
        
        existing_sr = User.find_by_sr_code(data['sr_code'])
        if existing_sr:
            return jsonify({'error': 'SR-Code already registered'}), 409
        
        # Hash password
        password_hash = hash_password(data['password'])
        
        # Create user
        user = User.create(
            sr_code=data['sr_code'],
            email=data['email'],
            password_hash=password_hash,
            first_name=data['first_name'],
            last_name=data['last_name'],
            middle_name=data.get('middle_name'),
            program=data['program'],
            year_level=year_level,  # Use validated year_level
            role='student'
        )
        
        if user:
            # Generate and send verification code
            code = generate_verification_code()
            expires = datetime.now() + timedelta(minutes=15)
            
            # Store code in database
            Database.execute_query(
                """UPDATE users 
                   SET verification_code = %s, verification_code_expires = %s 
                   WHERE user_id = %s""",
                (code, expires, user['user_id'])
            )
            
            # Send verification email
            name = f"{user['first_name']} {user['last_name']}"
            email_sent = send_verification_code_email(user['email'], name, code)
            
            # Generate token (but user needs to verify email before full access)
            token = generate_token(user['user_id'], user['role'])
            
            return jsonify({
                'message': 'Registration successful. Please check your email for verification code.',
                'user': {
                    'user_id': user['user_id'],
                    'sr_code': user['sr_code'],
                    'email': user['email'],
                    'first_name': user['first_name'],
                    'last_name': user['last_name'],
                    'role': user['role'],
                    'email_verified': False
                },
                'token': token,
                'requires_verification': True,
                'verification_sent': email_sent
            }), 201
        
        return jsonify({'error': 'Registration failed'}), 500
        
    except Exception as e:
        print(f"Registration error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user (student or admin)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Find user by email
        user = User.find_by_email(data['email'])
        
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Verify password
        if not verify_password(data['password'], user['password_hash']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Check email verification for students (admins bypass this)
        if user['role'] == 'student' and not user.get('email_verified', False):
            return jsonify({
                'error': 'Email not verified',
                'requires_verification': True,
                'email': user['email']
            }), 403
        
        # Generate token
        token = generate_token(user['user_id'], user['role'])
        
        return jsonify({
            'message': 'Login successful',
            'user': {
                'user_id': user['user_id'],
                'sr_code': user['sr_code'],
                'email': user['email'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'role': user['role'],
                'program': user.get('program'),
                'year_level': user.get('year_level'),
                'email_verified': user.get('email_verified', False)
            },
            'token': token
        }), 200
        
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/verify', methods=['GET'])
def verify_token():
    """Verify if token is valid"""
    from backend.utils.auth import token_required
    
    @token_required
    def verify():
        user = User.find_by_id(request.user_id)
        if user:
            return jsonify({
                'valid': True,
                'user': {
                    'user_id': user['user_id'],
                    'sr_code': user['sr_code'],
                    'email': user['email'],
                    'first_name': user['first_name'],
                    'last_name': user['last_name'],
                    'role': user['role']
                }
            }), 200
        return jsonify({'valid': False}), 401
    
    return verify()

@auth_bp.route('/google', methods=['GET'])
def google_auth():
    """Initiate Google OAuth flow"""
    try:
        auth_url = get_google_oauth_url()
        return jsonify({'auth_url': auth_url}), 200
    except Exception as e:
        print(f"Google auth error: {e}")
        return jsonify({'error': 'Failed to initiate Google authentication'}), 500

@auth_bp.route('/google/callback', methods=['GET'])
def google_callback():
    """Handle Google OAuth callback"""
    try:
        code = request.args.get('code')
        print(f"[DEBUG] Received code: {code[:20] if code else 'None'}...")
        
        if not code:
            print("[ERROR] No authorization code provided")
            return redirect('http://localhost:5000/login?error=no_code')
        
        # Exchange code for token
        print("[DEBUG] Exchanging code for token...")
        token_data = exchange_code_for_token(code)
        
        if not token_data:
            print("[ERROR] Failed to exchange code for token")
            return redirect('http://localhost:5000/login?error=token_exchange_failed')
        
        print(f"[DEBUG] Token data received: {list(token_data.keys())}")
        
        # Verify token and get user info
        id_token = token_data.get('id_token')
        print(f"[DEBUG] ID Token: {id_token[:20] if id_token else 'None'}...")
        
        user_info = verify_google_token(id_token)
        
        if not user_info:
            print("[ERROR] Failed to verify Google token")
            return redirect('http://localhost:5000/login?error=token_verification_failed')
        
        print(f"[DEBUG] User info: {user_info.get('email')}, Google ID: {user_info.get('google_id')}")
        
        # Check if user exists
        user = User.find_by_google_id(user_info['google_id'])
        print(f"[DEBUG] User by Google ID: {'Found' if user else 'Not found'}")
        
        if not user:
            user = User.find_by_email(user_info['email'])
            print(f"[DEBUG] User by email: {'Found' if user else 'Not found'}")
        
        if user:
            # Existing user - log them in
            token = generate_token(user['user_id'], user['role'])
            
            # Store user data in URL for frontend to pick up
            print("[DEBUG] User found - redirecting to dashboard")
            
            # Redirect to appropriate dashboard with token
            if user['role'] == 'admin':
                return redirect(f'http://localhost:5000/admin-dashboard?token={token}&google_login=true')
            else:
                return redirect(f'http://localhost:5000/student-dashboard?token={token}&google_login=true')
        else:
            # New user - need additional info (SR code, program, year)
            print("[DEBUG] New user - requires registration")
            
            # Store Google user info in session or redirect with params
            google_data = {
                'email': user_info['email'],
                'first_name': user_info.get('given_name', ''),
                'last_name': user_info.get('family_name', ''),
                'google_id': user_info['google_id']
            }
            
            # For now, redirect to register page with Google data in URL
            import urllib.parse
            params = urllib.parse.urlencode({
                'google_login': 'true',
                'email': google_data['email'],
                'first_name': google_data['first_name'],
                'last_name': google_data['last_name'],
                'google_id': google_data['google_id']
            })
            
            return redirect(f'http://localhost:5000/register?{params}')
            
    except Exception as e:
        import traceback
        print(f"[ERROR] Google callback error: {str(e)}")
        print(f"[ERROR] Traceback: {traceback.format_exc()}")
        return redirect(f'http://localhost:5000/login?error=authentication_failed')

@auth_bp.route('/google/register', methods=['POST'])
def google_register():
    """Complete registration for Google sign-in users"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['google_id', 'email', 'sr_code', 'first_name', 'last_name', 
                          'program', 'year_level']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Validate SR-Code format
        if not validate_sr_code(data['sr_code']):
            return jsonify({'error': 'Invalid SR-Code format. Use YY-XXXXX'}), 400
        
        # Validate year level (handle both string and int)
        try:
            year_level = int(data['year_level'])
            if year_level not in [1, 2, 3, 4]:
                return jsonify({'error': 'Year level must be between 1 and 4'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Year level must be a number between 1 and 4'}), 400
        
        # Check if SR code already exists
        existing_sr = User.find_by_sr_code(data['sr_code'])
        if existing_sr:
            return jsonify({'error': 'SR-Code already registered'}), 409
        
        # Check if email already registered
        existing_email = User.find_by_email(data['email'])
        if existing_email:
            return jsonify({'error': 'Email already registered'}), 409
        
        # Create user (no password needed for Google auth)
        user = User.create(
            sr_code=data['sr_code'],
            email=data['email'],
            password_hash='',  # Empty for Google auth users
            first_name=data['first_name'],
            last_name=data['last_name'],
            middle_name=data.get('middle_name'),
            program=data['program'],
            year_level=year_level,  # Use validated year_level
            role='student',
            google_id=data['google_id']
        )
        
        if user:
            token = generate_token(user['user_id'], user['role'])
            
            return jsonify({
                'message': 'Registration successful',
                'user': {
                    'user_id': user['user_id'],
                    'sr_code': user['sr_code'],
                    'email': user['email'],
                    'first_name': user['first_name'],
                    'last_name': user['last_name'],
                    'role': user['role']
                },
                'token': token
            }), 201
        
        return jsonify({'error': 'Registration failed'}), 500
        
    except Exception as e:
        print(f"Google registration error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/send-verification-code', methods=['POST'])
def send_verification_code():
    """Send verification code to email"""
    try:
        data = request.get_json()
        
        if not data.get('email'):
            return jsonify({'error': 'Email is required'}), 400
        
        # Find user by email
        user = User.find_by_email(data['email'])
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if user.get('email_verified'):
            return jsonify({'message': 'Email already verified'}), 200
        
        # Generate verification code
        code = generate_verification_code()
        expires = datetime.now() + timedelta(minutes=15)
        
        # Store code in database
        Database.execute_query(
            """UPDATE users 
               SET verification_code = %s, verification_code_expires = %s 
               WHERE user_id = %s""",
            (code, expires, user['user_id'])
        )
        
        # Send email
        name = f"{user['first_name']} {user['last_name']}"
        if send_verification_code_email(user['email'], name, code):
            return jsonify({'message': 'Verification code sent successfully'}), 200
        else:
            return jsonify({'error': 'Failed to send verification code'}), 500
            
    except Exception as e:
        print(f"Send verification code error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/verify-code', methods=['POST'])
def verify_code():
    """Verify email using code"""
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('code'):
            return jsonify({'error': 'Email and code are required'}), 400
        
        # Find user
        user = User.find_by_email(data['email'])
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check if already verified
        if user.get('email_verified'):
            return jsonify({'message': 'Email already verified'}), 200
        
        # Check code and expiration
        if user.get('verification_code') != data['code']:
            return jsonify({'error': 'Invalid verification code'}), 400
        
        if not user.get('verification_code_expires') or \
           datetime.now() > user['verification_code_expires']:
            return jsonify({'error': 'Verification code expired'}), 400
        
        # Mark as verified
        Database.execute_query(
            """UPDATE users 
               SET email_verified = TRUE, 
                   verification_code = NULL, 
                   verification_code_expires = NULL 
               WHERE user_id = %s""",
            (user['user_id'],)
        )
        
        return jsonify({'message': 'Email verified successfully'}), 200
        
    except Exception as e:
        print(f"Verify code error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/send-verification-link', methods=['POST'])
def send_verification_link():
    """Send verification link to email"""
    try:
        data = request.get_json()
        
        if not data.get('email'):
            return jsonify({'error': 'Email is required'}), 400
        
        # Find user
        user = User.find_by_email(data['email'])
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if user.get('email_verified'):
            return jsonify({'message': 'Email already verified'}), 200
        
        # Generate verification token
        token = generate_verification_token()
        expires = datetime.now() + timedelta(hours=24)
        
        # Store token in database
        Database.execute_query(
            """UPDATE users 
               SET verification_token = %s, verification_code_expires = %s 
               WHERE user_id = %s""",
            (token, expires, user['user_id'])
        )
        
        # Send email
        name = f"{user['first_name']} {user['last_name']}"
        if send_verification_link_email(user['email'], name, token):
            return jsonify({'message': 'Verification link sent successfully'}), 200
        else:
            return jsonify({'error': 'Failed to send verification link'}), 500
            
    except Exception as e:
        print(f"Send verification link error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/verify-email', methods=['GET'])
def verify_email_link():
    """Verify email using token from link"""
    try:
        token = request.args.get('token')
        
        if not token:
            return redirect('/login?error=invalid_token')
        
        # Find user by token
        user = Database.execute_query(
            """SELECT * FROM users 
               WHERE verification_token = %s 
               AND verification_code_expires > NOW()""",
            (token,),
            fetch_one=True
        )
        
        if not user:
            return redirect('/login?error=invalid_or_expired_token')
        
        # Mark as verified
        Database.execute_query(
            """UPDATE users 
               SET email_verified = TRUE, 
                   verification_token = NULL, 
                   verification_code_expires = NULL 
               WHERE user_id = %s""",
            (user['user_id'],)
        )
        
        return redirect('/login?verified=true')
        
    except Exception as e:
        print(f"Verify email link error: {e}")
        return redirect('/login?error=verification_failed')

@auth_bp.route('/resend-verification', methods=['POST'])
def resend_verification():
    """Resend verification code or link"""
    try:
        data = request.get_json()
        
        if not data.get('email'):
            return jsonify({'error': 'Email is required'}), 400
        
        method = data.get('method', 'code')  # 'code' or 'link'
        
        if method == 'link':
            return send_verification_link()
        else:
            return send_verification_code()
            
    except Exception as e:
        print(f"Resend verification error: {e}")
        return jsonify({'error': 'Internal server error'}), 500
