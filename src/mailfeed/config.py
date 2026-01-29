"""Configuration classes for mailfeed."""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class HTMLConfig:
    """Configuration for HTML processing."""
    
    email_image_width: int = 600
    email_image_height: int = 400
    email_image_border: int = 0
    
    def get_email_image_styles(self) -> Dict[str, Any]:
        """Get image styles as a dictionary."""
        return {
            'width': self.email_image_width,
            'height': self.email_image_height,
            'border': self.email_image_border
        }


@dataclass
class SMTPConfig:
    """Configuration for SMTP email sending."""
    
    host: str
    port: int = 587
    username: str = ""
    password: str = ""
    use_tls: bool = True
