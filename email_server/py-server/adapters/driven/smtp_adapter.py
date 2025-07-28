from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import smtplib
import ssl
import certifi
from email.mime.text import MIMEText
from core.ports.driven_ports import IEmailSender, ILogger
from core.domain.email import Email
from core.domain.sender_behavior_enum import SenderBehaviorEnum
from config.global_env_vars import (
    GOOGLE_EMAIL_API_KEY, 
    GOOGLE_SENDER_EMAIL, GOOGLE_SENDER_PASSWORD, 
    SMTP_SERVER, SMTP_PORT
)
from typing import Any, Optional
import os.path

# # https://developers.google.com/workspace/gmail/api/quickstart/python?hl=pt_BR
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError

# SCOPES = [
#     "https://www.googleapis.com/auth/gmail.readonly",
#     "https://www.googleapis.com/auth/gmail.send"
# ]

class SmtpAdapter(IEmailSender):
    def __init__(self, logger: ILogger):
        self._logger = logger
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.load_verify_locations(cafile=certifi.where())

    def send(self, email: MIMEMultipart | MIMEText, to: str) -> bool:

        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls(context=self.ssl_context) # For secure connection
                server.login(GOOGLE_SENDER_EMAIL, GOOGLE_SENDER_PASSWORD)
                server.sendmail(GOOGLE_SENDER_EMAIL, to, email.as_string())
                self._logger.log_info(f"Email sent successfully by {GOOGLE_SENDER_EMAIL} to {to}")
            return True
        except smtplib.SMTPAuthenticationError as auth_error:
            self._logger.log_error(f"Authentication Error for {GOOGLE_SENDER_EMAIL}: {auth_error}. Check App Password/Less Secure Apps.")
            return False
        except smtplib.SMTPException as smtp_error:
            self._logger.log_error(f"SMTP Error during sending from {GOOGLE_SENDER_EMAIL}: {smtp_error}")
            return False
        except Exception as e:
            self._logger.log_error(f"An unexpected error occurred during email sending: {e}")
            return False
        

        




