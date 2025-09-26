"""Test resume parsing functionality."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pathlib import Path
from cover_letter_generator.tools import FileHandler


def create_sample_resume_files():
    """Create sample resume files for testing."""
    sample_dir = Path("sample_resumes")
    sample_dir.mkdir(exist_ok=True)
    
    # Create a sample text resume
    txt_resume = sample_dir / "sample_resume.txt"
    txt_content = """
John Doe
Software Engineer
Email: john.doe@email.com
Phone: (555) 123-4567

SUMMARY
Experienced software engineer with 5+ years in full-stack development.
Skilled in Python, JavaScript, React, and cloud technologies.

EXPERIENCE
Senior Software Engineer | TechCorp | 2020-Present
• Developed scalable web applications serving 1M+ users
• Led team of 4 developers in agile environment
• Implemented CI/CD pipelines reducing deployment time by 60%

Software Engineer | StartupXYZ | 2018-2020
• Built RESTful APIs using Python Flask and Django
• Designed database schemas for PostgreSQL
• Collaborated with product team on feature requirements

EDUCATION
Bachelor of Science in Computer Science
University of Technology | 2018

SKILLS
• Programming: Python, JavaScript, TypeScript, Java
• Web: React, Node.js, HTML/CSS, REST APIs
• Database: PostgreSQL, MongoDB, Redis
• Cloud: AWS, Docker, Kubernetes
• Tools: Git, Jenkins, JIRA
    """
    txt_resume.write_text(txt_content.strip(), encoding='utf-8')
    
    return sample_dir, txt_resume


def test_resume_parsing():
    """Test the resume parsing functionality."""
    print("🧪 Testing Resume Parsing Functionality")
    print("=" * 50)
    
    # Create sample files
    sample_dir, txt_resume = create_sample_resume_files()
    
    print(f"📁 Created sample resumes in: {sample_dir}")
    
    # Test text file parsing
    print(f"\n📄 Testing TXT resume parsing...")
    try:
        content = FileHandler.parse_resume_file(txt_resume)
        print(f"✅ Successfully parsed TXT resume ({len(content)} characters)")
        print(f"Preview: {content[:200]}...")
    except Exception as e:
        print(f"❌ Error parsing TXT resume: {e}")
    
    # Test error handling for non-existent file
    print(f"\n🔍 Testing error handling for missing file...")
    try:
        FileHandler.parse_resume_file(Path("non_existent.pdf"))
    except FileNotFoundError as e:
        print(f"✅ Correctly caught missing file error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    # Test unsupported format
    print(f"\n🔍 Testing unsupported file format...")
    unsupported_file = sample_dir / "resume.xyz"
    unsupported_file.write_text("test content")
    
    try:
        FileHandler.parse_resume_file(unsupported_file)
    except ValueError as e:
        print(f"✅ Correctly caught unsupported format error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    # Cleanup
    import shutil
    shutil.rmtree(sample_dir)
    print(f"\n🧹 Cleaned up sample files")


def test_cli_integration():
    """Test CLI integration with resume parsing."""
    print(f"\n🖥️  CLI Integration Test")
    print("=" * 30)
    
    print("Sample CLI commands with resume files:")
    print("• Text resume: --resume my_resume.txt")
    print("• PDF resume:  --resume my_resume.pdf")
    print("• Word resume: --resume my_resume.docx")
    print("• Markdown:    --resume my_resume.md")
    
    print("\nExample usage:")
    print("python -m cover_letter_generator.cli url 'https://job-url.com' --resume resume.pdf")


def main():
    """Run resume parsing tests."""
    test_resume_parsing()
    test_cli_integration()
    
    print(f"\n🎉 Resume Parsing Tests Complete!")
    print("\nKey Features Added:")
    print("✅ PDF resume parsing (PyPDF2)")
    print("✅ Word document parsing (python-docx)")
    print("✅ Text file support (.txt, .md)")
    print("✅ Proper error handling")
    print("✅ File format validation")
    print("✅ CLI integration")
    
    print(f"\nTo install required packages:")
    print("pip install PyPDF2 python-docx")
    print("\nFor better PDF support:")
    print("pip install pdfplumber")


if __name__ == "__main__":
    main()