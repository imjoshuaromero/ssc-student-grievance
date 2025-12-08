"""Start a local debugging SMTP server to capture emails"""
import asyncore
from smtpd import SMTPServer
import sys

class DebuggingSMTPServer(SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        print('\n' + '='*70)
        print(f'📧 EMAIL CAPTURED:')
        print(f'From: {mailfrom}')
        print(f'To: {rcpttos}')
        print(f'Message length: {len(data)} bytes')
        print('='*70)
        print(data.decode('utf-8'))
        print('='*70 + '\n')
        return

if __name__ == '__main__':
    print("Starting local debugging SMTP server on localhost:1025")
    print("Configure your app to use: MAIL_SERVER=localhost, MAIL_PORT=1025")
    print("Press Ctrl+C to stop\n")
    
    server = DebuggingSMTPServer(('localhost', 1025), None)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        print("\nStopping server...")
        sys.exit(0)
