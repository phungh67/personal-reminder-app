import os
import sys

# Ensure python can find the 'app' folder
sys.path.append(os.getcwd())

from app.services.mail import *

def run_test():
    # 1. Check for credentials
    # We check if they are set in the terminal environment
    if not os.environ.get('SMTP_USER') or not os.environ.get('SMTP_PASSWORD'):
        print("❌ ERROR: Credentials missing.")
        print("Usage: SMTP_USER=x SMTP_PASSWORD=y python test_email.py")
        return

    print(f"--- Testing SMTP Connection to {os.environ.get('SMTP_SERVER', 'default')} ---")

    # 2. Initialize Service
    try:
        service = EmailService()
    except Exception as e:
        print(f"❌ Failed to initialize service: {e}")
        return

    # 3. Send Test Email
    # We send the email to yourself to verify it works
    recipient = os.environ.get('SMTP_USER')
    
    print(f"--- Sending test email to {recipient} ---")
    
    success = service.send_email(
        to_email=recipient,
        subject="DevOps Portfolio: SMTP Test",
        content="If you are reading this, your Flask Email Service is working correctly."
    )

    if success:
        print("✅ SUCCESS: Email sent!")
    else:
        print("❌ FAILED: Check error logs above.")

if __name__ == "__main__":
    run_test()