"""Direct SMTP test - bypassing Flask"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def test_direct_smtp():
    """Test SMTP connection directly"""
    
    mail_server = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    mail_port = int(os.getenv('MAIL_PORT', 587))
    mail_username = os.getenv('MAIL_USERNAME')
    mail_password = os.getenv('MAIL_PASSWORD')
    mail_sender = os.getenv('MAIL_DEFAULT_SENDER')
    
    print("Testing Gmail SMTP connection...")
    print(f"Server: {mail_server}:{mail_port}")
    print(f"Username: {mail_username}")
    print(f"Sender: {mail_sender}")
    print()
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = mail_sender
        msg['To'] = mail_username  # Send to yourself
        msg['Subject'] = "Test Email from Grievance System"
        
        body = """
        This is a test email from the SSC Grievance System.
        
        If you receive this, your SMTP configuration is working correctly!
        """
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect and send
        print("Connecting to SMTP server...")
        server = smtplib.SMTP(mail_server, mail_port, timeout=10)
        server.set_debuglevel(1)  # Show detailed logs
        
        print("\nStarting TLS...")
        server.starttls()
        
        print("\nLogging in...")
        server.login(mail_username, mail_password)
        
        print("\nSending email...")
        server.send_message(msg)
        server.quit()
        
        print("\n✅ SUCCESS! Email sent successfully!")
        print(f"Check your inbox: {mail_username}")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_direct_smtp()
