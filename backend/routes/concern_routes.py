from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from backend.models.concern import Concern
from backend.models.category import Category, Office, Notification
from backend.models.user import User
from backend.utils.auth import token_required, admin_required
from backend.utils.email_service import (
    send_concern_created_email, 
    send_status_update_email,
    send_concern_resolved_email,
    send_comment_notification_email,
    send_concern_assigned_email
)

concern_bp = Blueprint('concern', __name__)

# Configure file uploads
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@concern_bp.route('/', methods=['POST'])
@token_required
def create_concern():
    """Create a new concern (Student only)"""
    try:
        if request.user_role != 'student':
            return jsonify({'error': 'Only students can file concerns'}), 403
        
        # Handle both JSON and FormData
        if request.is_json:
            data = request.get_json()
            files = []
        else:
            data = request.form.to_dict()
            files = request.files.getlist('attachments')
        
        # Validate required fields
        required_fields = ['category_id', 'title', 'description']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Validate category exists
        category = Category.find_by_id(data['category_id'])
        if not category:
            return jsonify({'error': 'Invalid category'}), 400
        
        # Handle file uploads
        attachment_paths = []
        if files:
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    # Add timestamp to avoid duplicates
                    import time
                    timestamp = str(int(time.time()))
                    filename = f"{timestamp}_{filename}"
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(filepath)
                    attachment_paths.append(filepath)
        
        # Convert is_anonymous to boolean
        is_anonymous = data.get('is_anonymous', 'false')
        if isinstance(is_anonymous, str):
            is_anonymous = is_anonymous.lower() in ['true', '1', 'yes']
        
        # Create concern
        concern = Concern.create(
            student_id=request.user_id,
            category_id=data['category_id'],
            title=data['title'],
            description=data['description'],
            assigned_office_id=data.get('assigned_office_id'),
            location=data.get('location'),
            incident_date=data.get('incident_date'),
            is_anonymous=is_anonymous,
            priority=data.get('priority', 'normal')
        )
        
        if concern:
            # Get student details for email
            student = User.find_by_id(request.user_id)
            
            # Create notification
            Notification.create(
                user_id=request.user_id,
                concern_id=concern['concern_id'],
                notification_type='concern_created',
                title='Concern Received',
                message=f'Your concern {concern["ticket_number"]} has been received and is being reviewed.'
            )
            
            # Send email notification
            if student and not is_anonymous:
                student_name = f"{student['first_name']} {student['last_name']}"
                send_concern_created_email(
                    student['email'],
                    student_name,
                    concern['ticket_number'],
                    concern['title']
                )
            
            return jsonify({
                'message': 'Concern created successfully',
                'concern': concern
            }), 201
        
        return jsonify({'error': 'Failed to create concern'}), 500
        
    except Exception as e:
        print(f"Create concern error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500

@concern_bp.route('/', methods=['GET'])
@token_required
def get_concerns():
    """Get concerns (filtered by role)"""
    try:
        status = request.args.get('status') or None
        category_id = request.args.get('category_id') or None
        priority = request.args.get('priority') or None
        
        # Students only see their own concerns
        if request.user_role == 'student':
            concerns = Concern.get_by_student(request.user_id)
        else:
            # Admins see all concerns
            concerns = Concern.get_all(status, category_id, priority)
        
        # Ensure concerns is never None
        if concerns is None:
            concerns = []
        
        return jsonify(concerns), 200  # Return array directly for frontend
        
    except Exception as e:
        print(f"Get concerns error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@concern_bp.route('/<int:concern_id>', methods=['GET'])
@token_required
def get_concern_detail(concern_id):
    """Get concern details"""
    try:
        concern = Concern.find_by_id(concern_id)
        
        if not concern:
            return jsonify({'error': 'Concern not found'}), 404
        
        # Get status history
        history = Concern.get_status_history(concern_id)
        
        # Get comments
        comments = Concern.get_comments(concern_id, include_internal=True)
        
        return jsonify(concern), 200  # Return concern directly
        
    except Exception as e:
        print(f"Get concern detail error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@concern_bp.route('/<int:concern_id>/status', methods=['PATCH'])
@admin_required
def update_concern_status(concern_id):
    """Update concern status (Admin only)"""
    try:
        data = request.get_json()
        
        if 'status' not in data:
            return jsonify({'error': 'Status is required'}), 400
        
        valid_statuses = ['pending', 'in-review', 'in-progress', 'resolved', 'closed', 'rejected']
        if data['status'] not in valid_statuses:
            return jsonify({'error': 'Invalid status'}), 400
        
        # Get concern before update to check old status
        concern = Concern.find_by_id(concern_id)
        if not concern:
            return jsonify({'error': 'Concern not found'}), 404
        
        old_status = concern['status']
        
        result = Concern.update_status(
            concern_id=concern_id,
            new_status=data['status'],
            admin_id=request.user_id,
            remarks=data.get('remarks')
        )
        
        if result:
            # Get student details for email
            student = User.find_by_id(concern['student_id'])
            
            # Create notification for student
            Notification.create(
                user_id=concern['student_id'],
                concern_id=concern_id,
                notification_type='status_changed',
                title='Status Updated',
                message=f'Your concern {concern["ticket_number"]} status has been updated to {data["status"]}.'
            )
            
            # Send email notification
            if student:
                student_name = f"{student['first_name']} {student['last_name']}"
                send_status_update_email(
                    student['email'],
                    student_name,
                    concern['ticket_number'],
                    concern['title'],
                    old_status,
                    data['status'],
                    data.get('remarks')
                )
            
            return jsonify({
                'message': 'Status updated successfully',
                'concern': result
            }), 200
        
        return jsonify({'error': 'Failed to update status'}), 500
        
    except Exception as e:
        print(f"Update status error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@concern_bp.route('/<int:concern_id>/priority', methods=['PATCH'])
@admin_required
def update_concern_priority(concern_id):
    """Update concern priority (Admin only)"""
    try:
        data = request.get_json()
        
        if 'priority' not in data:
            return jsonify({'error': 'Priority is required'}), 400
        
        valid_priorities = ['low', 'normal', 'high', 'urgent']
        if data['priority'] not in valid_priorities:
            return jsonify({'error': 'Invalid priority'}), 400
        
        # Update priority in database
        result = Concern.update_priority(concern_id, data['priority'])
        
        if result:
            return jsonify({
                'message': 'Priority updated successfully',
                'concern': result
            }), 200
        
        return jsonify({'error': 'Concern not found'}), 404
        
    except Exception as e:
        print(f"Update priority error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@concern_bp.route('/<int:concern_id>/assign', methods=['PATCH'])
@admin_required
def assign_concern(concern_id):
    """Assign concern to office (Admin only)"""
    try:
        data = request.get_json()
        
        if 'office_id' not in data:
            return jsonify({'error': 'office_id is required'}), 400
        
        # Validate office exists
        office = Office.find_by_id(data['office_id'])
        if not office:
            return jsonify({'error': 'Invalid office'}), 400
        
        result = Concern.assign_to_office(
            concern_id=concern_id,
            office_id=data['office_id'],
            admin_id=request.user_id
        )
        
        if result:
            # Get concern details
            concern = Concern.find_by_id(concern_id)
            
            # Get student details for email
            student = User.find_by_id(concern['student_id'])
            
            # Create notification
            Notification.create(
                user_id=concern['student_id'],
                concern_id=concern_id,
                notification_type='concern_assigned',
                title='Concern Assigned',
                message=f'Your concern {concern["ticket_number"]} has been assigned to {office["office_name"]}.'
            )
            
            # Send email notification
            if student:
                student_name = f"{student['first_name']} {student['last_name']}"
                send_concern_assigned_email(
                    student['email'],
                    student_name,
                    concern['ticket_number'],
                    concern['title'],
                    office['office_name']
                )
            
            return jsonify({
                'message': 'Concern assigned successfully',
                'concern': result
            }), 200
        
        return jsonify({'error': 'Concern not found'}), 404
        
    except Exception as e:
        print(f"Assign concern error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@concern_bp.route('/<int:concern_id>/resolve', methods=['PATCH'])
@admin_required
def resolve_concern(concern_id):
    """Resolve concern (Admin only)"""
    try:
        data = request.get_json()
        
        if 'resolution_notes' not in data or not data['resolution_notes']:
            return jsonify({'error': 'Resolution notes are required'}), 400
        
        result = Concern.resolve(
            concern_id=concern_id,
            admin_id=request.user_id,
            resolution_notes=data['resolution_notes']
        )
        
        if result:
            # Get concern details
            concern = Concern.find_by_id(concern_id)
            
            # Get student details for email
            student = User.find_by_id(concern['student_id'])
            
            # Create notification
            Notification.create(
                user_id=concern['student_id'],
                concern_id=concern_id,
                notification_type='concern_resolved',
                title='Concern Resolved',
                message=f'Your concern {concern["ticket_number"]} has been resolved.'
            )
            
            # Send email notification
            if student:
                student_name = f"{student['first_name']} {student['last_name']}"
                send_concern_resolved_email(
                    student['email'],
                    student_name,
                    concern['ticket_number'],
                    concern['title'],
                    data['resolution_notes']
                )
            
            return jsonify({
                'message': 'Concern resolved successfully',
                'concern': result
            }), 200
        
        return jsonify({'error': 'Concern not found'}), 404
        
    except Exception as e:
        print(f"Resolve concern error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@concern_bp.route('/<int:concern_id>/comments', methods=['POST'])
@token_required
def add_comment(concern_id):
    """Add comment to concern"""
    try:
        concern = Concern.find_by_id(concern_id)
        
        if not concern:
            return jsonify({'error': 'Concern not found'}), 404
        
        # Students can only comment on their own concerns
        if request.user_role == 'student' and concern['student_id'] != request.user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        data = request.get_json()
        
        if 'comment_text' not in data or not data['comment_text']:
            return jsonify({'error': 'Comment text is required'}), 400
        
        # Only admins can create internal comments
        is_internal = data.get('is_internal', False) and request.user_role == 'admin'
        
        comment = Concern.add_comment(
            concern_id=concern_id,
            user_id=request.user_id,
            comment_text=data['comment_text'],
            is_internal=is_internal
        )
        
        if comment and not is_internal:
            # Get user details
            commenter = User.find_by_id(request.user_id)
            commenter_name = f"{commenter['first_name']} {commenter['last_name']}" if commenter else "Unknown"
            
            # Notify the other party (student or admin)
            notify_user_id = concern['student_id'] if request.user_role == 'admin' else concern['assigned_admin_id']
            
            if notify_user_id:
                notify_user = User.find_by_id(notify_user_id)
                
                # Create in-app notification
                Notification.create(
                    user_id=notify_user_id,
                    concern_id=concern_id,
                    notification_type='comment_added',
                    title='New Comment',
                    message=f'A new comment has been added to concern {concern["ticket_number"]}.'
                )
                
                # Send email notification to student
                if notify_user and request.user_role == 'admin':
                    student_name = f"{notify_user['first_name']} {notify_user['last_name']}"
                    send_comment_notification_email(
                        notify_user['email'],
                        student_name,
                        concern['ticket_number'],
                        concern['title'],
                        commenter_name,
                        data['comment_text']
                    )
        
        return jsonify({
            'message': 'Comment added successfully',
            'comment': comment
        }), 201

    except Exception as e:
        print(f"Add comment error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@concern_bp.route('/<int:concern_id>/comments', methods=['GET'])
@token_required
def get_comments(concern_id):
    """Get comments for a concern"""
    try:
        concern = Concern.find_by_id(concern_id)

        if not concern:
            return jsonify({'error': 'Concern not found'}), 404

        # Include internal comments only for admins
        include_internal = request.user_role == 'admin'
        comments = Concern.get_comments(concern_id, include_internal=include_internal)

        return jsonify({'comments': comments}), 200

    except Exception as e:
        print(f"Get comments error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@concern_bp.route('/<int:concern_id>/history', methods=['GET'])
@token_required
def get_history(concern_id):
    """Get status history for a concern"""
    try:
        concern = Concern.find_by_id(concern_id)

        if not concern:
            return jsonify({'error': 'Concern not found'}), 404

        history = Concern.get_status_history(concern_id)

        return jsonify({'history': history}), 200

    except Exception as e:
        print(f"Get history error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@concern_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all concern categories (public)"""
    try:
        categories = Category.get_all()
        return jsonify({'categories': categories}), 200
    except Exception as e:
        print(f"Get categories error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@concern_bp.route('/categories', methods=['POST'])
@admin_required
def create_category():
    """Create a new category (Admin only)"""
    try:
        data = request.get_json()
        
        if not data.get('category_name'):
            return jsonify({'error': 'Category name is required'}), 400
        
        category = Category.create(
            category_name=data['category_name'],
            description=data.get('description')
        )
        
        if category:
            return jsonify({
                'message': 'Category created successfully',
                'category': category
            }), 201
        
        return jsonify({'error': 'Failed to create category'}), 500
        
    except Exception as e:
        print(f"Create category error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@concern_bp.route('/categories/<int:category_id>', methods=['PUT'])
@admin_required
def update_category(category_id):
    """Update a category (Admin only)"""
    try:
        data = request.get_json()
        
        if not data.get('category_name'):
            return jsonify({'error': 'Category name is required'}), 400
        
        success = Category.update(
            category_id,
            category_name=data['category_name'],
            description=data.get('description')
        )
        
        if success:
            return jsonify({'message': 'Category updated successfully'}), 200
        
        return jsonify({'error': 'Failed to update category'}), 500
        
    except Exception as e:
        print(f"Update category error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@concern_bp.route('/categories/<int:category_id>', methods=['DELETE'])
@admin_required
def delete_category(category_id):
    """Delete a category (Admin only)"""
    try:
        success = Category.delete(category_id)
        
        if success:
            return jsonify({'message': 'Category deleted successfully'}), 200
        
        return jsonify({'error': 'Failed to delete category or category has associated concerns'}), 400
        
    except Exception as e:
        print(f"Delete category error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@concern_bp.route('/offices', methods=['GET'])
def get_offices():
    """Get all offices"""
    try:
        offices = Office.get_all()
        return jsonify(offices), 200  # Return array directly
    except Exception as e:
        print(f"Get offices error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@concern_bp.route('/statistics', methods=['GET'])
@admin_required
def get_statistics():
    """Get concern statistics (Admin only)"""
    try:
        stats = Concern.get_statistics()
        return jsonify({'statistics': stats}), 200
    except Exception as e:
        print(f"Get statistics error: {e}")
        return jsonify({'error': 'Internal server error'}), 500
