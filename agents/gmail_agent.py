import base64
import os
from typing import List, Dict, Tuple
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google.auth.oauthlib.flow import InstalledAppFlow
from google_auth_httplib2 import AuthorizedHttp
from googleapiclient.discovery import build
import pickle

from utils.logger import setup_logger

logger = setup_logger(__name__)

class GmailAgent:
    """Agent for connecting to and retrieving emails from Gmail."""
    
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    
    def __init__(self, email: str, app_password: str = None):
        """
        Initialize Gmail Agent.
        
        Args:
            email: Gmail email address
            app_password: Gmail app password (for basic auth)
        """
        self.email = email
        self.app_password = app_password
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """
        Authenticate with Gmail API using app password.
        """
        try:
            # Using Gmail API with basic authentication
            from google.auth.transport.requests import Request
            from google.oauth2.credentials import Credentials
            import google_auth_oauthlib.flow
            
            # For production, use OAuth 2.0 flow
            # This is a simplified version - for production use proper OAuth flow
            self.service = build('gmail', 'v1', static_discovery=False)
            logger.info(f"Gmail authentication setup for {self.email}")
        except Exception as e:
            logger.error(f"Gmail authentication failed: {str(e)}")
            raise
    
    def get_unread_emails(self, limit: int = 10) -> List[Dict]:
        """
        Retrieve unread emails from Gmail.
        
        Args:
            limit: Maximum number of emails to retrieve
        
        Returns:
            List of email dictionaries with id, subject, body, and sender
        """
        try:
            # Query for unread emails
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread',
                maxResults=limit
            ).execute()
            
            messages = results.get('messages', [])
            emails = []
            
            for message in messages:
                email_data = self._parse_message(message['id'])
                if email_data:
                    emails.append(email_data)
            
            logger.info(f"Retrieved {len(emails)} unread emails")
            return emails
        
        except Exception as e:
            logger.error(f"Error retrieving emails: {str(e)}")
            return []
    
    def _parse_message(self, message_id: str) -> Dict:
        """
        Parse a single Gmail message.
        
        Args:
            message_id: Gmail message ID
        
        Returns:
            Dictionary with message data
        """
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()
            
            headers = message['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
            
            # Extract body
            body = self._get_email_body(message['payload'])
            
            return {
                'id': message_id,
                'subject': subject,
                'sender': sender,
                'date': date,
                'body': body
            }
        except Exception as e:
            logger.error(f"Error parsing message {message_id}: {str(e)}")
            return None
    
    def _get_email_body(self, payload: Dict) -> str:
        """
        Extract email body from payload.
        
        Args:
            payload: Email payload
        
        Returns:
            Email body text
        """
        try:
            if 'parts' in payload:
                for part in payload['parts']:
                    if part['mimeType'] == 'text/plain':
                        if 'data' in part['body']:
                            return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
            else:
                if 'data' in payload['body']:
                    return base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
        except Exception as e:
            logger.warning(f"Error extracting email body: {str(e)}")
        
        return ""
    
    def mark_as_read(self, message_id: str):
        """
        Mark an email as read.
        
        Args:
            message_id: Gmail message ID
        """
        try:
            self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            logger.debug(f"Marked message {message_id} as read")
        except Exception as e:
            logger.error(f"Error marking message as read: {str(e)}")
