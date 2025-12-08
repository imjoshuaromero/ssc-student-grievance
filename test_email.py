"""Test email configuration"""
from backend.config.config import config
import os

c = config['development']
print("Email Configuration:")
print(f"MAIL_SERVER: {c.MAIL_SERVER}")
print(f"MAIL_PORT: {c.MAIL_PORT}")
print(f"MAIL_USE_TLS: {c.MAIL_USE_TLS}")
print(f"MAIL_USERNAME: {c.MAIL_USERNAME}")
print(f"MAIL_PASSWORD: {'***' if c.MAIL_PASSWORD else 'NOT SET'}")
print(f"MAIL_DEFAULT_SENDER: {c.MAIL_DEFAULT_SENDER}")

# Test direct SMTP connection
print("\nTesting SMTP connection...")
import smtplib
try:
    server = smtplib.SMTP(c.MAIL_SERVER, c.MAIL_PORT, timeout=10)
    server.starttls()
    server.login(c.MAIL_USERNAME, c.MAIL_PASSWORD)
    print("✓ SMTP connection successful!")
    server.quit()
except Exception as e:
    print(f"✗ SMTP connection failed: {e}")
