<p align="center">
  <img src="https://raw.githubusercontent.com/rrodakowski/mailfeed/main/mailfeed-logo.svg" alt="Mailfeed Logo" width="200"/>
</p>

# Mailfeed

A reusable Python library for sending HTML emails with images and attachments.

## Features

- Build HTML emails with embedded images
- Clean and normalize HTML content
- Send emails via SMTP
- Flexible configuration via dependency injection
- Type-safe interfaces

## Installation

```bash
pip install mailfeed
```

For development:
```bash
pip install -e ".[dev]"
```

## Quick Start

```python
from mailfeed import EmailService

# Create email service
email_service = EmailService()

# Build email with images
images = {
    'image1': '/path/to/image1.png',
    'image2': '/path/to/image2.png'
}

msg = email_service.build_html_email(
    from_email='sender@example.com',
    to_email='recipient@example.com',
    subject='Hello from Mailfeed',
    text='Plain text version',
    html='<html><body><h1>Hello</h1><img src="cid:image1"/></body></html>',
    images=images
)

# Send via SMTP
email_service.send_smtp_email(
    sender='sender@example.com',
    recipient='recipient@example.com',
    msg=msg,
    host='smtp.example.com',
    port=587,
    smtp_username='username',
    smtp_password='password'
)
```

## HTML Normalization

```python
from mailfeed import HTMLNormalizer, HTMLConfig

config = HTMLConfig(
    email_image_width=600,
    email_image_height=400,
    email_image_border=0
)

normalizer = HTMLNormalizer(config)
clean_html = normalizer.clean_html(dirty_html)
```

## License

MIT License - see LICENSE file for details.
