import os
from pathlib import Path

# Get package root directory
PACKAGE_ROOT = Path(__file__).parent
PROJECT_ROOT = PACKAGE_ROOT.parent

class Settings:
    """Configuration settings for the Cover Letter Generator."""
    
    # LLM Configuration
    API_KEY = os.getenv("OPENAI_API_KEY", "your_api_key_here")
    MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    # File paths
    TEMPLATE_PATH = PROJECT_ROOT / "templates" / "cover_letter_template.txt"
    OUTPUT_DIR = PROJECT_ROOT / "output"
    
    # Web scraping settings
    REQUEST_TIMEOUT = 10
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    
    @classmethod
    def ensure_output_dir(cls):
        """Ensure the output directory exists."""
        cls.OUTPUT_DIR.mkdir(exist_ok=True)
        return cls.OUTPUT_DIR
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present."""
        if cls.API_KEY == "your_api_key_here":
            raise ValueError("Please set your OPENAI_API_KEY environment variable")
        
        if not cls.TEMPLATE_PATH.exists():
            raise FileNotFoundError(f"Template file not found: {cls.TEMPLATE_PATH}")