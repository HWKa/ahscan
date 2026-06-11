"""
Send email via Gmail SMTP using an App Password.
Configure via environment variables or config.py (gitignored).
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime


def send_email(html_body: str):
    """Send the report email. Reads credentials from env vars."""
    smtp_user     = os.environ.get("SMTP_USER")      # your Gmail address
    smtp_password = os.environ.get("SMTP_PASSWORD")   # 16-char App Password
    recipient     = os.environ.get("REPORT_EMAIL", smtp_user)

    if not smtp_user or not smtp_password:
        print("SMTP credentials not set — skipping email send.")
        return

    subject = f"Icecrown AH Gem Report — {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = smtp_user
    msg["To"]      = recipient
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, recipient, msg.as_string())

    print(f"Email sent to {recipient}")
