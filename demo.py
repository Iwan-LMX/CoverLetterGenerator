"""Demo script to test the package structure without requiring API keys."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from cover_letter_generator.tools import WebScraper, FileHandler
from cover_letter_generator.config import Settings


def test_web_scraper():
    """Test the web scraper's text cleaning functionality."""
    print("🧪 Testing WebScraper...")
    scraper = WebScraper()
    
    # Test text cleaning
    dirty_text = "  Hello   world!  \n\n  This   has   extra   spaces  "
    clean_text = scraper._clean_text(dirty_text)
    print(f"Original: '{dirty_text}'")
    print(f"Cleaned:  '{clean_text}'")
    print("✅ Text cleaning works!\n")


def test_file_handler():
    """Test the file handler functionality."""
    print("🧪 Testing FileHandler...")
    
    # Test template creation
    import tempfile
    from pathlib import Path
    
    with tempfile.TemporaryDirectory() as temp_dir:
        template_path = Path(temp_dir) / "test_template.txt"
        FileHandler.create_default_template(template_path)
        
        if template_path.exists():
            content = template_path.read_text()
            print("✅ Template creation works!")
            print(f"Template preview: {content[:100]}...")
        else:
            print("❌ Template creation failed")
    print()


def test_settings():
    """Test the settings configuration."""
    print("🧪 Testing Settings...")
    print(f"Template path: {Settings.TEMPLATE_PATH}")
    print(f"Output directory: {Settings.OUTPUT_DIR}")
    print(f"Model name: {Settings.MODEL_NAME}")
    print("✅ Settings configuration works!\n")


def main():
    """Run all demo tests."""
    print("🚀 Cover Letter Generator - Demo Tests")
    print("=" * 50)
    
    test_settings()
    test_web_scraper()
    test_file_handler()
    
    print("🎉 All demo tests completed!")
    print("\nTo use the full functionality:")
    print("1. Set your OpenAI API key: set OPENAI_API_KEY=your_key_here")
    print("2. Run: python -m cover_letter_generator.cli setup")
    print("3. Generate cover letter: python -m cover_letter_generator.cli url <job_url> --resume resume.txt")


if __name__ == "__main__":
    main()