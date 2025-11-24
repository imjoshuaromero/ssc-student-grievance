from flask_mail import Mail, Message
from flask import current_app
import os
import time

mail = Mail()

def init_mail(app):
    """Initialize Flask-Mail with app"""
    mail.init_app(app)

def send_email(to, subject, body_text, body_html=None, max_retries=3):
    """Send email notification with retry logic"""
    for attempt in range(max_retries):
        try:
            msg = Message(
                subject=subject,
                recipients=[to] if isinstance(to, str) else to,
                body=body_text,
                html=body_html or body_text
            )
            mail.send(msg)
            print(f"✓ Email sent successfully to {to}")
            return True
        except Exception as e:
            print(f"Email attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)  # Wait 2 seconds before retry
            else:
                print(f"✗ Failed to send email to {to} after {max_retries} attempts")
                return False

def send_concern_created_email(student_email, student_name, ticket_number, title):
    """Send email when concern is created"""
    subject = f"Concern Received - {ticket_number}"
    
    body_html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
            <h2 style="color: #004d99;">Concern Received</h2>
            <p>Dear {student_name},</p>
            <p>Your concern has been successfully received and is being reviewed by the Supreme Student Council.</p>
            
            <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p style="margin: 5px 0;"><strong>Ticket Number:</strong> {ticket_number}</p>
                <p style="margin: 5px 0;"><strong>Title:</strong> {title}</p>
                <p style="margin: 5px 0;"><strong>Status:</strong> Pending</p>
            </div>
            
            <p>You will receive email updates when there are changes to your concern status.</p>
            <p>You can track your concern by logging into the Grievance System.</p>
            
            <p style="margin-top: 30px;">Thank you,<br>
            <strong>Supreme Student Council</strong><br>
            BatState-U TNEU Lipa</p>
        </div>
    </body>
    </html>
    """
    
    return send_email(student_email, subject, body_html, body_html)

def send_status_update_email(student_email, student_name, ticket_number, title, old_status, new_status, remarks=None):
    """Send email when concern status is updated"""
    subject = f"Status Update - {ticket_number}"
    
    body_html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
            <h2 style="color: #004d99;">Concern Status Updated</h2>
            <p>Dear {student_name},</p>
            <p>There has been an update to your concern:</p>
            
            <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p style="margin: 5px 0;"><strong>Ticket Number:</strong> {ticket_number}</p>
                <p style="margin: 5px 0;"><strong>Title:</strong> {title}</p>
                <p style="margin: 5px 0;"><strong>Previous Status:</strong> <span style="color: #666;">{old_status}</span></p>
                <p style="margin: 5px 0;"><strong>New Status:</strong> <span style="color: #00aa00; font-weight: bold;">{new_status}</span></p>
                {f'<p style="margin: 5px 0;"><strong>Remarks:</strong> {remarks}</p>' if remarks else ''}
            </div>
            
            <p>Please log in to the Grievance System to view more details and updates.</p>
            
            <p style="margin-top: 30px;">Thank you,<br>
            <strong>Supreme Student Council</strong><br>
            BatState-U TNEU Lipa</p>
        </div>
    </body>
    </html>
    """
    
    return send_email(student_email, subject, body_html, body_html)

def send_concern_resolved_email(student_email, student_name, ticket_number, title, resolution_notes):
    """Send email when concern is resolved"""
    subject = f"Concern Resolved - {ticket_number}"
    
    body_html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
            <h2 style="color: #00aa00;">Concern Resolved ✓</h2>
            <p>Dear {student_name},</p>
            <p>Great news! Your concern has been resolved.</p>
            
            <div style="background-color: #f0f8f0; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #00aa00;">
                <p style="margin: 5px 0;"><strong>Ticket Number:</strong> {ticket_number}</p>
                <p style="margin: 5px 0;"><strong>Title:</strong> {title}</p>
                <p style="margin: 5px 0;"><strong>Status:</strong> <span style="color: #00aa00;">Resolved</span></p>
            </div>
            
            <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p style="margin: 5px 0;"><strong>Resolution Details:</strong></p>
                <p style="margin: 10px 0;">{resolution_notes}</p>
            </div>
            
            <p>If you have any questions or concerns regarding the resolution, please don't hesitate to reach out to the SSC office.</p>
            
            <p style="margin-top: 30px;">Thank you,<br>
            <strong>Supreme Student Council</strong><br>
            BatState-U TNEU Lipa</p>
        </div>
    </body>
    </html>
    """
    
    return send_email(student_email, subject, body_html, body_html)

def send_comment_notification_email(student_email, student_name, ticket_number, title, commenter_name, comment_text):
    """Send email when new comment is added"""
    subject = f"New Comment - {ticket_number}"
    
    body_html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
            <h2 style="color: #004d99;">New Comment Added</h2>
            <p>Dear {student_name},</p>
            <p>A new comment has been added to your concern:</p>
            
            <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p style="margin: 5px 0;"><strong>Ticket Number:</strong> {ticket_number}</p>
                <p style="margin: 5px 0;"><strong>Title:</strong> {title}</p>
            </div>
            
            <div style="background-color: #fff; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #004d99;">
                <p style="margin: 5px 0;"><strong>From:</strong> {commenter_name}</p>
                <p style="margin: 10px 0;">{comment_text}</p>
            </div>
            
            <p>Log in to the Grievance System to view all comments and respond.</p>
            
            <p style="margin-top: 30px;">Thank you,<br>
            <strong>Supreme Student Council</strong><br>
            BatState-U TNEU Lipa</p>
        </div>
    </body>
    </html>
    """
    
    return send_email(student_email, subject, body_html, body_html)

def send_concern_assigned_email(student_email, student_name, ticket_number, title, office_name):
    """Send email when concern is assigned to an office"""
    subject = f"Concern Assigned - {ticket_number}"
    
    body_html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
            <h2 style="color: #004d99;">Concern Assigned</h2>
            <p>Dear {student_name},</p>
            <p>Your concern has been assigned to the appropriate office for handling:</p>
            
            <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p style="margin: 5px 0;"><strong>Ticket Number:</strong> {ticket_number}</p>
                <p style="margin: 5px 0;"><strong>Title:</strong> {title}</p>
                <p style="margin: 5px 0;"><strong>Assigned To:</strong> <span style="color: #004d99; font-weight: bold;">{office_name}</span></p>
            </div>
            
            <p>The assigned office will review your concern and take appropriate action.</p>
            
            <p style="margin-top: 30px;">Thank you,<br>
            <strong>Supreme Student Council</strong><br>
            BatState-U TNEU Lipa</p>
        </div>
    </body>
    </html>
    """
    
    return send_email(student_email, subject, body_html, body_html)
