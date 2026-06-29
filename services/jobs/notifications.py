from __future__ import annotations

import smtplib
from email.message import EmailMessage

from packages.core.config import Settings


def send_email(settings: Settings, *, subject: str, body: str) -> None:
    if not settings.smtp_host:
        raise RuntimeError("SMTP_HOST is required for email notifications")
    if not settings.email_alert_to:
        raise RuntimeError("EMAIL_ALERT_TO is required for email notifications")

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = settings.email_alert_from
    message["To"] = settings.email_alert_to
    message.set_content(body)

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=30) as smtp:
        if settings.smtp_use_tls:
            smtp.starttls()
        if settings.smtp_username or settings.smtp_password:
            smtp.login(settings.smtp_username, settings.smtp_password)
        smtp.send_message(message)
