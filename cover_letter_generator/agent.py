"""Main agent class for cover letter generation."""

from pathlib import Path
from typing import Optional, Dict, Any
from .llm import LLMClient
from .tools import WebScraper, FileHandler
from .config import Settings


class CoverLetterAgent:
    """Agent for generating cover letters from job descriptions."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the cover letter agent.
        
        Args:
            api_key: OpenAI API key. If None, uses environment variable.
        """
        self.llm = LLMClient(api_key)
        self.scraper = WebScraper()
        self.file_handler = FileHandler()
        
        # Validate configuration
        Settings.validate_config()
    
    def generate_from_url(self, job_url: str, resume_info: str, 
                         output_filename: Optional[str] = None) -> Dict[str, Any]:
        """Generate a cover letter from a job posting URL.
        
        Args:
            job_url: URL of the job posting
            resume_info: User's resume/background information
            output_filename: Name for the output file
            
        Returns:
            Dictionary with generation results
        """
        print(f"🔍 Scraping job posting from: {job_url}")
        
        # Step 1: Scrape the job posting
        job_data = self.scraper.scrape_job_description(job_url)
        
        print(f"✅ Found job: {job_data['title']} at {job_data['company']}")
        
        # Step 2: Generate the cover letter
        print("🤖 Generating cover letter...")
        
        cover_letter = self.llm.generate_cover_letter(
            job_description=job_data['description'],
            resume_info=resume_info,
            company_name=job_data['company'],
            position_title=job_data['title']
        )
        
        # Step 3: Save the cover letter (both PDF and TXT)
        output_paths = self.file_handler.save_cover_letter(
            content=cover_letter,
            filename=output_filename,
            company_name=job_data['company'],
            position_title=job_data['title']
        )
        
        print(f"💾 Cover letter saved to:")
        print(f"   📄 Text: {output_paths['txt']}")
        print(f"   📋 PDF:  {output_paths['pdf']}")
        print(f"   📁 Folder: {output_paths['folder']}")
        
        return {
            'job_data': job_data,
            'cover_letter': cover_letter,
            'output_paths': output_paths,
            'success': True
        }
    
    def generate_from_text(self, job_description: str, resume_info: str,
                          company_name: str = "", position_title: str = "",
                          output_filename: Optional[str] = None) -> Dict[str, Any]:
        """Generate a cover letter from job description text.
        
        Args:
            job_description: The job posting text
            resume_info: User's resume/background information
            company_name: Name of the company
            position_title: Title of the position
            output_filename: Name for the output file
            
        Returns:
            Dictionary with generation results
        """
        print("🤖 Generating cover letter from provided text...")
        
        # Generate the cover letter
        cover_letter = self.llm.generate_cover_letter(
            job_description=job_description,
            resume_info=resume_info,
            company_name=company_name,
            position_title=position_title
        )
        
        # Save the cover letter (both PDF and TXT)
        output_paths = self.file_handler.save_cover_letter(
            content=cover_letter,
            filename=output_filename,
            company_name=company_name,
            position_title=position_title
        )
        
        print(f"💾 Cover letter saved to:")
        print(f"   📄 Text: {output_paths['txt']}")
        print(f"   📋 PDF:  {output_paths['pdf']}")
        print(f"   📁 Folder: {output_paths['folder']}")
        
        return {
            'job_data': {
                'title': position_title,
                'company': company_name,
                'description': job_description,
                'url': None
            },
            'cover_letter': cover_letter,
            'output_paths': output_paths,
            'success': True
        }
    
    def set_resume_info(self, resume_path: Optional[Path] = None, 
                       resume_text: Optional[str] = None) -> str:
        """Set resume information from file or text.
        
        Args:
            resume_path: Path to resume file
            resume_text: Resume text content
            
        Returns:
            Resume content
        """
        if resume_path and resume_path.exists():
            return resume_path.read_text(encoding='utf-8')
        elif resume_text:
            return resume_text
        else:
            raise ValueError("Either resume_path or resume_text must be provided")
    
    def preview_job_data(self, job_url: str) -> Dict[str, Any]:
        """Preview job data without generating a cover letter.
        
        Args:
            job_url: URL of the job posting
            
        Returns:
            Scraped job data
        """
        return self.scraper.scrape_job_description(job_url)