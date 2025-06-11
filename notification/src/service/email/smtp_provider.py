import aiosmtplib
from schema.email import SMTPConfig


class SMTPProvider:
    """
    A provider for sending emails using SMTP.
    """

    def __init__(self, config: SMTPConfig):
        self.host = config.host
        self.port = config.port
        self.username = config.username
        self.password = config.password

    async def send_email(self, recipient: str, subject: str, body: str):
        message = f"Subject: {subject}\n\n{body}"  # Separate the subject and body with a newline
        async with aiosmtplib.SMTP(hostname=self.host, port=self.port) as smtp:
            await smtp.login(self.username, self.password)  # type: ignore
            await smtp.sendmail(self.username, recipient, message)  # type: ignore
