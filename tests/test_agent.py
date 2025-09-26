"""Tests for the Cover Letter Generator."""

import unittest
from unittest.mock import Mock, patch
from pathlib import Path
import sys
import os

# Add the package to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from cover_letter_generator.agent import CoverLetterAgent
from cover_letter_generator.config import Settings
from cover_letter_generator.tools import WebScraper, FileHandler


class TestCoverLetterAgent(unittest.TestCase):
    """Test cases for CoverLetterAgent."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Mock the API key to avoid validation error
        with patch.object(Settings, 'API_KEY', 'test-api-key'):
            self.agent = CoverLetterAgent()
    
    @patch('cover_letter_generator.tools.WebScraper.scrape_job_description')
    @patch('cover_letter_generator.llm.LLMClient.generate_cover_letter')
    @patch('cover_letter_generator.tools.FileHandler.save_cover_letter')
    def test_generate_from_url(self, mock_save, mock_generate, mock_scrape):
        """Test generating cover letter from URL."""
        # Mock responses
        mock_scrape.return_value = {
            'title': 'Software Engineer',
            'company': 'Test Corp',
            'description': 'Great job opportunity',
            'url': 'https://test.com/job'
        }
        mock_generate.return_value = "Dear Hiring Manager, ..."
        mock_save.return_value = Path("/test/output.txt")
        
        # Test the method
        result = self.agent.generate_from_url(
            job_url="https://test.com/job",
            resume_info="Test resume"
        )
        
        # Assertions
        self.assertTrue(result['success'])
        self.assertEqual(result['job_data']['title'], 'Software Engineer')
        mock_scrape.assert_called_once()
        mock_generate.assert_called_once()
        mock_save.assert_called_once()


class TestWebScraper(unittest.TestCase):
    """Test cases for WebScraper."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.scraper = WebScraper()
    
    def test_clean_text(self):
        """Test text cleaning function."""
        dirty_text = "  Hello   world!  \n\n  Extra   spaces  "
        clean_text = self.scraper._clean_text(dirty_text)
        self.assertEqual(clean_text, "Hello world! Extra spaces")


class TestFileHandler(unittest.TestCase):
    """Test cases for FileHandler."""
    
    def test_create_default_template(self):
        """Test creating default template."""
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            template_path = Path(temp_dir) / "test_template.txt"
            FileHandler.create_default_template(template_path)
            
            self.assertTrue(template_path.exists())
            content = template_path.read_text()
            self.assertIn("Dear Hiring Manager", content)


if __name__ == '__main__':
    unittest.main()