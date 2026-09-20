import resend
from licht.lib.config import get_settings
import logging

logging.basicConfig(level=logging.INFO)

settings = get_settings()

resend.api_key = settings.resend_api_key

async def send_email(to: str, subject: str, html: str):
    try:
        response = await resend.Emails.send_async({
            "from": settings.email_from,
            "to": [to],
            "subject": subject,
            "html": html
        })
        return response
    except Exception as e:
        logging.error(f"Error sending email: {e}")
        return None