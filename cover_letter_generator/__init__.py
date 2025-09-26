"""Cover Letter Generator - AI-powered cover letter generation from job postings."""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .agent import CoverLetterAgent
from .llm import LLMClient
from .tools import WebScraper, FileHandler
from .config import Settings

__all__ = [
    'CoverLetterAgent',
    'LLMClient', 
    'WebScraper',
    'FileHandler',
    'Settings'
]