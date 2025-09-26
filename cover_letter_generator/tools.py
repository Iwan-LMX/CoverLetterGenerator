"""Tools for web scraping and file handling."""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
from pathlib import Path
from typing import Optional, Dict, Any
from .config import Settings


class WebScraper:
    """Tool for scraping job descriptions from web pages."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': Settings.USER_AGENT})
    
    def scrape_job_description(self, url: str) -> Dict[str, Any]:
        """Scrape job description from a URL.
        
        Args:
            url: URL of the job posting
            
        Returns:
            Dictionary containing job information
        """
        try:
            response = self.session.get(url, timeout=Settings.REQUEST_TIMEOUT)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract basic info
            title = self._extract_title(soup)
            company = self._extract_company(soup, url)
            description = self._extract_description(soup)
            
            return {
                'title': title,
                'company': company,
                'description': description,
                'url': url,
                'raw_html': str(soup)
            }
            
        except requests.RequestException as e:
            raise Exception(f"Error fetching URL {url}: {str(e)}")
        except Exception as e:
            raise Exception(f"Error parsing job description: {str(e)}")
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract job title from the page."""
        # Common selectors for job titles
        selectors = [
            'h1',
            '.job-title',
            '.jobsearch-JobInfoHeader-title',
            '[data-testid="job-title"]',
            '.job-header-title'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        
        # Fallback to page title
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text(strip=True)
        
        return "Unknown Position"
    
    def _extract_company(self, soup: BeautifulSoup, url: str) -> str:
        """Extract company name from the page."""
        # Common selectors for company names
        selectors = [
            '.company-name',
            '.jobsearch-InlineCompanyRating-companyHeader',
            '[data-testid="company-name"]',
            '.company'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        
        # Fallback to domain name
        domain = urlparse(url).netloc
        return domain.replace('www.', '').split('.')[0].title()
    
    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract job description from the page."""
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "header", "footer"]):
            script.decompose()
        
        # Common selectors for job descriptions
        selectors = [
            '.job-description',
            '.jobsearch-jobDescriptionText',
            '[data-testid="job-description"]',
            '.description',
            '.job-content'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text(separator=' ', strip=True)
                return self._clean_text(text)
        
        # Fallback to body text
        body = soup.find('body')
        if body:
            text = body.get_text(separator=' ', strip=True)
            return self._clean_text(text)[:2000]  # Limit length
        
        return "Could not extract job description"
    
    def _clean_text(self, text: str) -> str:
        """Clean extracted text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters that might cause issues
        text = re.sub(r'[^\w\s\.,!?;:()\-\'/"]', '', text)
        return text.strip()


class FileHandler:
    """Tool for handling file operations."""
    
    @staticmethod
    def read_template(template_path: Optional[Path] = None) -> str:
        """Read the cover letter template.
        
        Args:
            template_path: Path to template file. If None, uses default.
            
        Returns:
            Template content
        """
        path = template_path or Settings.TEMPLATE_PATH
        
        if not path.exists():
            # Create default template if it doesn't exist
            FileHandler.create_default_template(path)
        
        return path.read_text(encoding='utf-8')
    
    @staticmethod
    def save_cover_letter(content: str, filename: Optional[str] = None) -> Path:
        """Save the generated cover letter to a file.
        
        Args:
            content: Cover letter content
            filename: Output filename. If None, generates timestamp-based name.
            
        Returns:
            Path to the saved file
        """
        output_dir = Settings.ensure_output_dir()
        
        if filename is None:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cover_letter_{timestamp}.txt"
        
        output_path = output_dir / filename
        output_path.write_text(content, encoding='utf-8')
        
        return output_path
    
    @staticmethod
    def create_default_template(template_path: Path):
        """Create a default cover letter template."""
        default_template = """Dear Hiring Manager,

I am writing to express my strong interest in the {position} position at {company}. With my background in {relevant_experience}, I am excited about the opportunity to contribute to your team.

{body_paragraph_1}

{body_paragraph_2}

Thank you for considering my application. I look forward to hearing from you soon.

Sincerely,
[Your Name]"""
        
        template_path.parent.mkdir(parents=True, exist_ok=True)
        template_path.write_text(default_template, encoding='utf-8')