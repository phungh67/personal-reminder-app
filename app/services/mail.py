import os.path
import base64
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from flask import current_app

class GmailService:
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    
    def __init__(self, token_path='token.json', creds_path='credentials.json'):
        self.token_path = token_path
        self.creds_path = creds_path
        self.creds = None
        self.service = None

    def authenticate(self):
        """
        Handles the OAuth2 flow. 
        On first run, it will open a browser to ask for permission.
        It then saves the 'token.json' for future headless runs (DevOps friendly).
        """
        if os.path.exists(self.token_path):
            self.creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
            
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if not os.path.exists(self.creds_path):
                    print(f"ERROR: {self.creds_path} not found. Please download OAuth Client ID JSON from Google Cloud.")
                    return False
                    
                flow = InstalledAppFlow.from_client_secrets_file(self.creds_path, self.SCOPES)
                # Run local server for auth (requires browser on first run)
                self.creds = flow.run_local_server(port=0)
                
            # Save the credentials for the next run
            with open(self.token_path, 'w') as token:
                token.write(self.creds.to_json())

        try:
            self.service = build('gmail', 'v1', credentials=self.creds)
            return True
        except HttpError as error:
            print(f'An error occurred building service: {error}')
            return False

    def send_email(self, to_email, subject, content):
        """Builds and sends the message."""
        if not self.service:
            if not self.authenticate():
                return False

        try:
            message = EmailMessage()
            message.set_content(content)
            message['To'] = to_email
            message['From'] = 'me' # 'me' is a special value in Gmail API
            message['Subject'] = subject

            # Encode the message
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            create_message = {'raw': encoded_message}

            # Call the API
            send_message = (self.service.users().messages().send(userId="me", body=create_message).execute())
            print(f'Message Id: {send_message["id"]}')
            return True
            
        except HttpError as error:
            print(f'An error occurred: {error}')
            return False