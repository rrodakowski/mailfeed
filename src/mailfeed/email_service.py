"""Email building and sending services."""

import logging
import smtplib
import traceback
from email import charset
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from typing import Dict, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class EmailService:
    """Service for building and sending HTML emails with attachments."""

    def __init__(self):
        """Initialize email service."""
        logger.info("Initialized EmailService")

    def write_email_to_file(self, filename: str, email_msg: MIMEMultipart) -> None:
        """
        Write email message to a file.
        
        Args:
            filename: Path to output file
            email_msg: Email message to write
        """
        text = email_msg.as_string()
        logger.info("Writing email to file: %s", filename)
        
        with open(filename, "w") as file:
            file.write(text)

    def build_html_email(
        self,
        from_email: str,
        to_email: str,
        subject: str,
        text: str,
        html: str,
        images: Optional[Dict[str, str]] = None
    ) -> MIMEMultipart:
        """
        Build an HTML email with embedded images.
        
        Args:
            from_email: Sender email address
            to_email: Recipient email address
            subject: Email subject line
            text: Plain text version of email
            html: HTML version of email
            images: Dict mapping image IDs to file paths (e.g., {'image1': '/path/to/img.png'})
                   Reference in HTML as: <img src="cid:image1">
                   
        Returns:
            Complete email message ready to send
        """
        logger.info("Building HTML email: subject='%s'", subject)
        
        # Configure charset to avoid base64 encoding
        # See: http://bugs.python.org/issue12552
        charset.add_charset('utf-8', charset.SHORTEST, charset.QP)

        # Create message container - multipart/alternative for text and HTML
        msg_root = MIMEMultipart('alternative')
        msg_root['Subject'] = subject
        msg_root['From'] = from_email
        msg_root['To'] = to_email

        # Attach text and HTML parts
        plain_text = MIMEText(text, 'plain')
        html_text = MIMEText(html, 'html')
        
        # According to RFC 2046, the last part of a multipart message
        # (in this case the HTML) is best and preferred
        msg_root.attach(plain_text)
        msg_root.attach(html_text)
        
        logger.info("Added headers and body")

        # Attach images
        if images:
            for image_id, image_path in images.items():
                try:
                    with open(image_path, 'rb') as fp:
                        msg_image = MIMEImage(fp.read())
                    
                    # Define the image's ID as referenced in HTML (cid:image_id)
                    msg_image.add_header('Content-ID', f'<{image_id}>')
                    msg_root.attach(msg_image)
                    logger.info("Attached image: %s from %s", image_id, image_path)
                    
                except FileNotFoundError:
                    logger.error("Could not attach image file: %s", image_path)
                    logger.error(traceback.format_exc())
                except Exception as e:
                    logger.error("Error attaching image %s: %s", image_id, e)
                    logger.error(traceback.format_exc())

        return msg_root

    def send_smtp_email(
        self,
        sender: str,
        recipient: str,
        msg: MIMEMultipart,
        host: str,
        port: int,
        smtp_username: str,
        smtp_password: str
    ) -> bool:
        """
        Send email via SMTP.
        
        Args:
            sender: Sender email address
            recipient: Recipient email address
            msg: Email message to send
            host: SMTP server hostname
            port: SMTP server port
            smtp_username: SMTP authentication username
            smtp_password: SMTP authentication password
            
        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            server = smtplib.SMTP(host, port)
            server.ehlo()
            server.starttls()
            # SMTP docs recommend calling ehlo() before & after starttls()
            server.ehlo()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender, recipient, msg.as_string())
            server.close()
            
            logger.info("Successfully sent email to: %s", recipient)
            return True
            
        except Exception as e:
            logger.error("Failed to send email: %s", e)
            logger.error(traceback.format_exc())
            return False
