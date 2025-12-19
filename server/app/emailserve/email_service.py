import smtplib
from email.message import EmailMessage
import os
import logging

logging.basicConfig(level=logging.INFO)

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_SENDER = os.getenv("SENDER_EMAIL")

# 🔥 HARD FAIL if anything is missing
if not all([EMAIL_HOST, EMAIL_PORT, EMAIL_USERNAME, EMAIL_PASSWORD, EMAIL_SENDER]):
    raise RuntimeError("Email environment variables are missing")

EMAIL_PORT = int(EMAIL_PORT)  # ✅ REQUIRED


def send_email(to_email: str, subject: str, content: str):
    logging.info("Starting email send")

    msg = EmailMessage()
    msg["From"] = EMAIL_SENDER
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(content)

    try:
        logging.info(f"Connecting to SMTP {EMAIL_HOST}:{EMAIL_PORT}")

        with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT, timeout=20) as server:
            logging.info("Logging into SMTP")
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)

            logging.info("Sending email")
            server.send_message(msg)

            logging.info("Email sent successfully")

    except Exception as e:
        logging.exception("Failed to send email")
        raise
