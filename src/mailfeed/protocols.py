"""Protocol definitions for mailfeed interfaces."""

from typing import Protocol, Dict
from email.mime.multipart import MIMEMultipart


class EmailSender(Protocol):
    """Protocol for email sending implementations."""
    
    def send_smtp_email(
        self,
        sender: str,
        recipient: str,
        msg: MIMEMultipart,
        host: str,
        port: int,
        smtp_username: str,
        smtp_password: str
    ) -> None:
        """Send an email via SMTP."""
        ...


class HTMLCleaner(Protocol):
    """Protocol for HTML cleaning/normalization implementations."""
    
    def clean_html(self, input_html: str) -> str:
        """Clean and normalize HTML content."""
        ...
    
    def add_full_image_path(self, article: str, link: str) -> str:
        """Convert relative image paths to absolute paths."""
        ...
    
    def add_email_markup(self, article: str) -> str:
        """Add email-specific markup to HTML content."""
        ...
