"""HTML normalization and cleaning utilities."""

import logging
from typing import Optional

import lxml.html
from lxml.html.clean import Cleaner

from .config import HTMLConfig

logger = logging.getLogger(__name__)


class HTMLNormalizer:
    """HTML operations to remove unwanted tags and normalize content."""

    def __init__(self, config: Optional[HTMLConfig] = None):
        """
        Initialize HTML normalizer.
        
        Args:
            config: HTML configuration. If None, uses default config.
        """
        self.config = config or HTMLConfig()
        
        # Setup lxml's HTML cleaner
        self.cleaner = Cleaner()
        self.cleaner.style = True  # Activate the styles and stylesheet filter
        self.cleaner.javascript = True  # Activate the javascript filter
        self.cleaner.remove_tags = ['span']  # Keep text inside spans
        self.cleaner.kill_tags = ['br']  # Remove including children nodes

    def clean_html(self, input_html: str) -> str:
        """
        Remove unwanted tags and attributes from HTML.
        
        Args:
            input_html: Raw HTML string to clean
            
        Returns:
            Cleaned HTML string
        """
        attributes = ['class', 'id', 'style', 'width', 'height', 'border']
        cleaner_html = self.cleaner.clean_html(input_html)

        domhtml = lxml.html.fromstring(cleaner_html)

        for attribute in attributes:
            # xpath for attribute looks like: '//*[@id]'
            for tag in domhtml.xpath(f'//*[@{attribute}]'):
                # For each element with an attribute, remove that attribute
                tag.attrib.pop(attribute)
                
        return lxml.html.tostring(domhtml).decode("utf-8")

    def add_full_image_path(self, article: str, link: str) -> str:
        """
        Convert relative image paths to absolute paths.
        
        Args:
            article: HTML article content
            link: Base URL for converting relative paths
            
        Returns:
            HTML with absolute image paths
        """
        domarticle = lxml.html.fromstring(article.encode("utf-8"))
        last_index = link.rindex('.')
        last_index = last_index + 4
        link_prefix = link[0:last_index]
        
        for img in domarticle.xpath('//img'):
            if 'src' in img.attrib and 'http' not in img.attrib['src']:
                img.attrib['src'] = link_prefix + img.attrib['src']

        return lxml.html.tostring(domarticle).decode("utf-8")

    def add_email_markup(self, article: str) -> str:
        """
        Standardize image sizes in HTML for email display.
        
        Args:
            article: HTML article content
            
        Returns:
            HTML with standardized image attributes
        """
        attrs = self.config.get_email_image_styles()
        domarticle = lxml.html.fromstring(article.encode("utf-8"))

        for img in domarticle.xpath('//img'):
            img.attrib['width'] = str(attrs['width'])
            img.attrib['height'] = str(attrs['height'])
            img.attrib['border'] = str(attrs['border'])
            
        return lxml.html.tostring(domarticle).decode("utf-8")
