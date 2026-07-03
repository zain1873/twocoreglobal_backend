import json
import urllib.error
import urllib.request

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend


class ResendAPIBackend(BaseEmailBackend):
    """Sends mail via Resend's HTTPS API instead of SMTP.

    SMTP ports are frequently blocked/hang on cloud hosts (Railway included),
    which turns a slow mail send into a worker timeout and a 500 for the
    whole request. The HTTPS API avoids that failure mode entirely.
    """

    api_url = "https://api.resend.com/emails"

    def send_messages(self, email_messages):
        if not email_messages:
            return 0

        sent_count = 0
        for message in email_messages:
            payload = {
                "from": message.from_email,
                "to": message.to,
                "subject": message.subject,
                "text": message.body,
            }
            if message.cc:
                payload["cc"] = message.cc
            if message.bcc:
                payload["bcc"] = message.bcc
            if message.reply_to:
                payload["reply_to"] = message.reply_to

            request = urllib.request.Request(
                self.api_url,
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {settings.RESEND_API_KEY}",
                    "Content-Type": "application/json",
                    # Resend's Cloudflare front blocks requests carrying
                    # urllib's default User-Agent as a bot signature.
                    "User-Agent": "twocoreglobal-backend/1.0",
                },
                method="POST",
            )
            try:
                with urllib.request.urlopen(request, timeout=10) as response:
                    response.read()
                sent_count += 1
            except Exception:
                if not self.fail_silently:
                    raise
        return sent_count
