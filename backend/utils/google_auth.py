from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from backend.config.config import Config
import requests

def verify_google_token(token):
    """Verify Google OAuth token and return user info"""
    try:
        # Verify the token
        idinfo = id_token.verify_oauth2_token(
            token, 
            google_requests.Request(), 
            Config.GOOGLE_CLIENT_ID
        )
        
        # Check if token is for correct client
        if idinfo['aud'] != Config.GOOGLE_CLIENT_ID:
            return None
        
        # Extract user information
        user_info = {
            'email': idinfo.get('email'),
            'name': idinfo.get('name'),
            'given_name': idinfo.get('given_name'),
            'family_name': idinfo.get('family_name'),
            'picture': idinfo.get('picture'),
            'google_id': idinfo.get('sub'),
            'email_verified': idinfo.get('email_verified', False)
        }
        
        return user_info
        
    except ValueError as e:
        print(f"Token verification error: {e}")
        return None
    except Exception as e:
        print(f"Google auth error: {e}")
        return None

def get_google_oauth_url():
    """Generate Google OAuth authorization URL"""
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    
    params = {
        'client_id': Config.GOOGLE_CLIENT_ID,
        'redirect_uri': Config.GOOGLE_REDIRECT_URI,
        'response_type': 'code',
        'scope': 'openid email profile',
        'access_type': 'offline',
        'prompt': 'consent'
    }
    
    # Build URL with parameters
    param_string = '&'.join([f"{k}={v}" for k, v in params.items()])
    return f"{base_url}?{param_string}"

def exchange_code_for_token(code):
    """Exchange authorization code for access token"""
    token_url = "https://oauth2.googleapis.com/token"
    
    data = {
        'code': code,
        'client_id': Config.GOOGLE_CLIENT_ID,
        'client_secret': Config.GOOGLE_CLIENT_SECRET,
        'redirect_uri': Config.GOOGLE_REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    
    try:
        print(f"[DEBUG] Sending token request to Google...")
        print(f"[DEBUG] Redirect URI: {Config.GOOGLE_REDIRECT_URI}")
        response = requests.post(token_url, data=data)
        
        print(f"[DEBUG] Google response status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"[ERROR] Google token exchange failed: {response.text}")
            return None
            
        response.raise_for_status()
        token_data = response.json()
        print(f"[DEBUG] Token exchange successful")
        return token_data
    except Exception as e:
        print(f"[ERROR] Token exchange error: {str(e)}")
        import traceback
        print(f"[ERROR] Traceback: {traceback.format_exc()}")
        return None
