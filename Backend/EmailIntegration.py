"""
EmailIntegration.py
A simple IMAP/SMTP email client.

Setup in .env:
    EmailAddress=you@gmail.com
    EmailPassword=your_app_password   ← use a Gmail App Password, NOT your real password
    IMAPServer=imap.gmail.com
    SMTPServer=smtp.gmail.com
    SMTPPort=587

For Gmail App Passwords: https://myaccount.google.com/apppasswords
"""

import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header
from dotenv import dotenv_values
import os

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_vars = dotenv_values(os.path.join(current_dir, ".env"))

EMAIL_ADDRESS = env_vars.get("EmailAddress", "")
EMAIL_PASSWORD = env_vars.get("EmailPassword", "")
IMAP_SERVER = env_vars.get("IMAPServer", "imap.gmail.com")
SMTP_SERVER = env_vars.get("SMTPServer", "smtp.gmail.com")
SMTP_PORT = int(env_vars.get("SMTPPort", 587))


def _decode_header_value(value: str) -> str:
    parts = decode_header(value or "")
    decoded = []
    for part, enc in parts:
        if isinstance(part, bytes):
            decoded.append(part.decode(enc or "utf-8", errors="replace"))
        else:
            decoded.append(str(part))
    return " ".join(decoded)


class EmailClient:
    def check_emails(self, limit: int = 5):
        if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
            return "Email credentials not configured. Add EmailAddress and EmailPassword to your .env file."
        try:
            mail = imaplib.IMAP4_SSL(IMAP_SERVER)
            mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            mail.select("inbox")

            _, data = mail.search(None, "ALL")
            ids = data[0].split()
            recent_ids = ids[-limit:] if len(ids) >= limit else ids
            recent_ids = list(reversed(recent_ids))

            emails = []
            for eid in recent_ids:
                _, msg_data = mail.fetch(eid, "(RFC822)")
                msg = email.message_from_bytes(msg_data[0][1])
                emails.append({
                    "sender": _decode_header_value(msg.get("From", "")),
                    "subject": _decode_header_value(msg.get("Subject", "(No Subject)")),
                    "date": msg.get("Date", ""),
                })

            mail.logout()
            return emails

        except Exception as e:
            return f"Error checking emails: {e}"

    def summarize_emails(self, limit: int = 10):
        result = self.check_emails(limit=limit)
        if isinstance(result, str):
            return result
        if not result:
            return "No emails found."
        lines = [f"{i+1}. From: {e['sender']} | Subject: {e['subject']} | {e['date']}"
                 for i, e in enumerate(result)]
        return "Recent emails:\n" + "\n".join(lines)

    def send_email(self, recipient: str, subject: str, body: str) -> str:
        if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
            return "Email credentials not configured."
        try:
            msg = MIMEMultipart()
            msg["From"] = EMAIL_ADDRESS
            msg["To"] = recipient
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.sendmail(EMAIL_ADDRESS, recipient, msg.as_string())

            return f"Email sent to {recipient}."
        except Exception as e:
            return f"Error sending email: {e}"
