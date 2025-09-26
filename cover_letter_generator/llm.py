"""LLM interface for interacting with language models."""

import openai
from typing import Dict, List, Optional
from .config import Settings


class LLMClient:
    """Client for interacting with OpenAI's API."""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """Initialize the LLM client.
        
        Args:
            api_key: OpenAI API key. If None, uses Settings.API_KEY
            model: Model name. If None, uses Settings.MODEL_NAME
        """
        self.api_key = api_key or Settings.API_KEY
        self.model = model or Settings.MODEL_NAME
        
        # Set the API key
        openai.api_key = self.api_key
    
    def generate_text(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """Generate text using the language model.
        
        Args:
            prompt: The input prompt
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0-1)
            
        Returns:
            Generated text
        """
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise Exception(f"Error generating text: {str(e)}")
    
    def generate_cover_letter(self, job_description: str, resume_info: str, 
                            company_name: str = "", position_title: str = "") -> str:
        """Generate a cover letter based on job description and resume.
        
        Args:
            job_description: The job posting description
            resume_info: User's resume information
            company_name: Name of the company
            position_title: Title of the position
            
        Returns:
            Generated cover letter
        """
        prompt = f"""
        Please write a professional cover letter based on the following information:
        
        Company: {company_name}
        Position: {position_title}
        
        Job Description:
        {job_description}
        
        My Background:
        {resume_info}
        
        Please create a compelling cover letter that:
        1. Addresses the specific requirements mentioned in the job description
        2. Highlights relevant experience from my background
        3. Shows enthusiasm for the role and company
        4. Is professional and concise (around 3-4 paragraphs)
        5. Includes proper formatting for a business letter
        
        Cover Letter:
        """
        
        return self.generate_text(prompt, max_tokens=800, temperature=0.7)