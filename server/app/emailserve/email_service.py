import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_SENDER=os.getenv("SENDER_EMAIL")


def send_email(to_email: str, subject: str, content: str):
    
    msg = EmailMessage()
    msg["From"] = EMAIL_SENDER
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(content)
    try:
        with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT, timeout=20) as server:
            
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
           
            server.send_message(msg)
            
    except Exception as e:
        print(f" Failed to send email: {e}")