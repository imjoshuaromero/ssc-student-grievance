"""Email verification utilities"""

import random
import string
import os
from datetime import datetime, timedelta
from backend.utils.email_service import send_email

def generate_verification_code():
    """Generate a 6-digit verification code"""
    return ''.join(random.choices(string.digits, k=6))

def generate_verification_token():
    """Generate a random verification token"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=64))

def send_verification_code_email(email, name, code):
    """Send verification code email"""
    subject = "Email Verification - SSC Grievance System"
    
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
            <h2 style="color: #004d99;">Email Verification</h2>
            <p>Dear {name},</p>
            <p>Thank you for registering with the SSC Grievance System. Please verify your email address to complete your registration.</p>
            
            <div style="background-color: #f5f5f5; padding: 20px; border-radius: 5px; margin: 20px 0; text-align: center;">
                <p style="margin: 5px 0; font-size: 14px;">Your verification code is:</p>
                <h1 style="margin: 10px 0; color: #004d99; letter-spacing: 8px; font-size: 36px;">{code}</h1>
                <p style="margin: 5px 0; font-size: 12px; color: #666;">This code will expire in 15 minutes.</p>
            </div>
            
            <p>If you didn't request this verification, please ignore this email.</p>
            
            <p style="margin-top: 30px;">Thank you,<br>
            <strong>Supreme Student Council</strong><br>
            BatState-U TNEU Lipa</p>
        </div>
    </body>
    </html>
    """
    
    return send_email(email, subject, html_content)

def send_verification_link_email(email, name, token):
    """Send verification link email"""
    base_url = os.getenv('BASE_URL', 'http://localhost:5000')
    subject = "Email Verification - SSC Grievance System"
    verification_link = f"{base_url}/verify-email?token={token}"
    
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
            <h2 style="color: #004d99;">Email Verification</h2>
            <p>Dear {name},</p>
            <p>Thank you for registering with the SSC Grievance System. Please verify your email address to complete your registration.</p>
            
            <div style="background-color: #f5f5f5; padding: 20px; border-radius: 5px; margin: 20px 0; text-align: center;">
                <p style="margin: 10px 0;">Click the button below to verify your email:</p>
                <a href="{verification_link}" 
                   style="display: inline-block; padding: 12px 30px; background-color: #004d99; color: white; text-decoration: none; border-radius: 5px; font-weight: bold; margin: 10px 0;">
                    Verify Email Address
                </a>
                <p style="margin: 10px 0; font-size: 12px; color: #666;">This link will expire in 24 hours.</p>
            </div>
            
            <p style="font-size: 12px; color: #666;">If the button doesn't work, copy and paste this link into your browser:</p>
            <p style="font-size: 12px; color: #004d99; word-break: break-all;">{verification_link}</p>
            
            <p>If you didn't request this verification, please ignore this email.</p>
            
            <p style="margin-top: 30px;">Thank you,<br>
            <strong>Supreme Student Council</strong><br>
            BatState-U TNEU Lipa</p>
        </div>
    </body>
    </html>
    """
    
    return send_email(email, subject, html_content)
