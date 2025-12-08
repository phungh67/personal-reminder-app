import smtplib
import os
from email.message import EmailMessage

class EmailService:
    def __init__(self):
        # Load config from Environment Variables (DevOps Best Practice)
        self.smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.environ.get('SMTP_PORT', 587))
        self.smtp_user = os.environ.get('SMTP_USER')
        self.smtp_password = os.environ.get('SMTP_PASSWORD')
        
    def send_email(self, to_email, subject, content):
        """
        Sends an email using standard SMTP with TLS encryption.
        """
        if not self.smtp_user or not self.smtp_password:
            print("ERROR: SMTP credentials not found in environment variables.")
            return False

        msg = EmailMessage()
        msg.set_content(content)
        msg['Subject'] = subject
        msg['From'] = self.smtp_user
        msg['To'] = to_email

        try:
            # Connect to server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Upgrade connection to secure
            
            # Login
            server.login(self.smtp_user, self.smtp_password)
            
            # Send
            server.send_message(msg)
            server.quit()
            
            print(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            print(f"SMTP Error: {e}")
            return False