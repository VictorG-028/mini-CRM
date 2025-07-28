
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from email.mime.base import MIMEBase
from email import encoders
from email_server.config import EMAIL_CONFIG
from email_server.utils import get_email_credentials

"""
This module provides functionality to send emails using SMTP.
"""

def send_email(body: str, 
               subject: str, 
               to: list[str]
            ) -> None:
    
    """Sends an email with the specified body, subject, and recipient list."""

    # Get email credentials
    email, password = get_email_credentials()
    if not email or not password:
        raise ValueError("Email credentials are not set in the environment.")
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = formataddr((EMAIL_CONFIG['sender_name'], email))
    msg['To'] = ', '.join(to)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    # Set up the SMTP server
    try:
        with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
            server.starttls()  # Upgrade to a secure connection
            server.login(email, password)  # Log in to the email account
            server.sendmail(email, to, msg.as_string())  # Send the email
            print(f"Email sent successfully to {', '.join(to)}")
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

