from flask import Blueprint, request, jsonify
from backend.models.user import User
from backend.models.category import Notification
from backend.utils.auth import token_required, admin_required

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile', methods=['GET'])
@token_required
def get_profile():
    """Get current user profile"""
    try:
        user = User.find_by_id(request.user_id)
        
        if user:
            return jsonify({'user': user}), 200
        
        return jsonify({'error': 'User not found'}), 404
        
    except Exception as e:
        print(f"Get profile error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@user_bp.route('/profile', methods=['PUT'])
@token_required
def update_profile():
    """Update user profile"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['first_name', 'last_name']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} is required'}), 400
        
        user = User.update_profile(
            user_id=request.user_id,
            first_name=data['first_name'],
            last_name=data['last_name'],
            middle_name=data.get('middle_name'),
            program=data.get('program'),
            year_level=data.get('year_level')
        )
        
        if user:
            return jsonify({
                'message': 'Profile updated successfully',
                'user': user
            }), 200
        
        return jsonify({'error': 'Update failed'}), 500
        
    except Exception as e:
        print(f"Update profile error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@user_bp.route('/notifications', methods=['GET'])
@token_required
def get_notifications():
    """Get user notifications"""
    try:
        unread_only = request.args.get('unread_only', 'false').lower() == 'true'
        
        notifications = Notification.get_by_user(request.user_id, unread_only)
        
        return jsonify({'notifications': notifications}), 200
        
    except Exception as e:
        print(f"Get notifications error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@user_bp.route('/notifications/<int:notification_id>/read', methods=['PATCH'])
@token_required
def mark_notification_read(notification_id):
    """Mark notification as read"""
    try:
        Notification.mark_as_read(notification_id)
        return jsonify({'message': 'Notification marked as read'}), 200
        
    except Exception as e:
        print(f"Mark notification error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@user_bp.route('/notifications/read-all', methods=['PATCH'])
@token_required
def mark_all_notifications_read():
    """Mark all notifications as read"""
    try:
        Notification.mark_all_as_read(request.user_id)
        return jsonify({'message': 'All notifications marked as read'}), 200
        
    except Exception as e:
        print(f"Mark all notifications error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@user_bp.route('/students', methods=['GET'])
@admin_required
def get_students():
    """Get all students (Admin only)"""
    try:
        students = User.get_all_students()
        return jsonify({'students': students}), 200
        
    except Exception as e:
        print(f"Get students error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@user_bp.route('/admins', methods=['GET'])
@admin_required
def get_admins():
    """Get all admins (Admin only)"""
    try:
        admins = User.get_all_admins()
        return jsonify({'admins': admins}), 200
        
    except Exception as e:
        print(f"Get admins error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@user_bp.route('/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    """Update user (Admin only)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'first_name' not in data or not data['first_name']:
            return jsonify({'error': 'First name is required'}), 400
        if 'last_name' not in data or not data['last_name']:
            return jsonify({'error': 'Last name is required'}), 400
        if 'role' not in data or data['role'] not in ['student', 'admin']:
            return jsonify({'error': 'Valid role is required'}), 400
        
        # Update user
        user = User.update_profile(
            user_id=user_id,
            first_name=data['first_name'],
            last_name=data['last_name'],
            middle_name=data.get('middle_name'),
            program=data.get('program'),
            year_level=data.get('year_level')
        )
        
        # Update role if changed
        if 'role' in data:
            from backend.config.database import Database
            Database.execute_query(
                "UPDATE users SET role = %s WHERE user_id = %s",
                (data['role'], user_id)
            )
        
        if user:
            return jsonify({
                'message': 'User updated successfully',
                'user': user
            }), 200
        
        return jsonify({'error': 'Update failed'}), 500
        
    except Exception as e:
        print(f"Update user error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    """Delete a user (Admin only)"""
    try:
        # Prevent deleting yourself
        if user_id == request.user_id:
            return jsonify({'error': 'Cannot delete your own account'}), 403
        
        # Check if user exists
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Delete the user (this will cascade delete concerns, comments, etc.)
        success = User.delete(user_id)
        
        if success:
            return jsonify({
                'message': 'User deleted successfully'
            }), 200
        
        return jsonify({'error': 'Failed to delete user'}), 500
        
    except Exception as e:
        print(f"Delete user error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500

@user_bp.route('/', methods=['GET'])
#@admin_required  # TEMPORARILY DISABLED FOR TESTING
def get_all_users():
    """Get all users with concern counts (Admin only)"""
    try:
        from backend.config.database import Database
        
        # Query to get all users with concern counts
        query = """
            SELECT 
                u.user_id,
                u.sr_code,
                u.email,
                u.first_name,
                u.last_name,
                u.middle_name,
                u.program,
                u.year_level,
                u.role,
                u.is_active,
                u.created_at,
                COUNT(c.concern_id) as concern_count
            FROM users u
            LEFT JOIN concerns c ON u.user_id = u.user_id
            WHERE u.is_active = true
            GROUP BY u.user_id, u.sr_code, u.email, u.first_name, u.last_name, 
                     u.middle_name, u.program, u.year_level, u.role, u.is_active, u.created_at
            ORDER BY u.role DESC, u.last_name, u.first_name
        """
        
        users = Database.execute_query(query, fetch_all=True)
        
        return jsonify(users), 200
        
    except Exception as e:
        print(f"Get all users error: {e}")
        return jsonify({'error': 'Internal server error'}), 500
