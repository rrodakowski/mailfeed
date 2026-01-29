"""
Mailfeed - Reusable library for sending HTML emails with images and attachments.
"""

from .email_service import EmailService
from .html_normalizer import HTMLNormalizer
from .config import HTMLConfig
from .protocols import EmailSender, HTMLCleaner

__version__ = "0.1.0"

__all__ = [
    "EmailService",
    "HTMLNormalizer",
    "HTMLConfig",
    "EmailSender",
    "HTMLCleaner",
]
