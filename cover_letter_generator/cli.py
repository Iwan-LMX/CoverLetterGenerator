"""Command line interface for the cover letter generator."""

import argparse
import sys
from pathlib import Path
from typing import Optional
from .agent import CoverLetterAgent
from .config import Settings


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate cover letters from job postings using AI"
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate from URL command
    url_parser = subparsers.add_parser('url', help='Generate from job posting URL')
    url_parser.add_argument('job_url', help='URL of the job posting')
    url_parser.add_argument('--resume', '-r', help='Path to resume file')
    url_parser.add_argument('--resume-text', help='Resume text (if no file)')
    url_parser.add_argument('--output', '-o', help='Output filename')
    
    # Generate from text command
    text_parser = subparsers.add_parser('text', help='Generate from job description text')
    text_parser.add_argument('job_file', help='File containing job description')
    text_parser.add_argument('--resume', '-r', help='Path to resume file')
    text_parser.add_argument('--resume-text', help='Resume text (if no file)')
    text_parser.add_argument('--company', help='Company name')
    text_parser.add_argument('--position', help='Position title')
    text_parser.add_argument('--output', '-o', help='Output filename')
    
    # Preview command
    preview_parser = subparsers.add_parser('preview', help='Preview scraped job data')
    preview_parser.add_argument('job_url', help='URL of the job posting')
    
    # Setup command
    setup_parser = subparsers.add_parser('setup', help='Setup configuration')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'setup':
            setup_config()
        elif args.command == 'preview':
            preview_job(args.job_url)
        elif args.command in ['url', 'text']:
            generate_cover_letter(args)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


def setup_config():
    """Interactive setup for configuration."""
    print("🔧 Setting up Cover Letter Generator...")

    print(f"\nTemplate will be created at: {Settings.TEMPLATE_PATH}")
    print(f"Output files will be saved to: {Settings.OUTPUT_DIR}")
    
    # Create template if it doesn't exist
    from .tools import FileHandler
    if not Settings.TEMPLATE_PATH.exists():
        FileHandler.create_default_template(Settings.TEMPLATE_PATH)
        print(f"✅ Created default template at {Settings.TEMPLATE_PATH}")
    
    # Create output directory
    Settings.ensure_output_dir()
    print(f"✅ Created output directory at {Settings.OUTPUT_DIR}")
    
    print("\n🎉 Setup complete! You can now generate cover letters.")


def preview_job(job_url: str):
    """Preview job data from URL."""
    agent = CoverLetterAgent()
    job_data = agent.preview_job_data(job_url)
    
    print(f"\n📋 Job Preview:")
    print(f"Title: {job_data['title']}")
    print(f"Company: {job_data['company']}")
    print(f"URL: {job_data['url']}")
    print(f"\nDescription (first 500 chars):")
    print(job_data['description'][:500] + "..." if len(job_data['description']) > 500 else job_data['description'])
    # print(job_data)

def generate_cover_letter(args):
    """Generate cover letter based on command arguments."""
    # Get resume information
    resume_info = get_resume_info(args)
    
    # Initialize agent
    agent = CoverLetterAgent()
    
    if args.command == 'url':
        result = agent.generate_from_url(
            job_url=args.job_url,
            resume_info=resume_info,
            output_filename=args.output
        )
    else:  # text command
        job_description = Path(args.job_file).read_text(encoding='utf-8')
        result = agent.generate_from_text(
            job_description=job_description,
            resume_info=resume_info,
            company_name=args.company or "",
            position_title=args.position or "",
            output_filename=args.output
        )
    
    print(f"\n📄 Generated cover letter for: {result['job_data']['title']}")
    print(f"Company: {result['job_data']['company']}")
    print(f"Saved to: {result['output_path']}")
    
    # Show preview
    print(f"\n📝 Preview (first 300 characters):")
    print(result['cover_letter'][:300] + "...")


def get_resume_info(args) -> str:
    """Get resume information from arguments."""
    if args.resume:
        resume_path = Path(args.resume)
        if not resume_path.exists():
            raise FileNotFoundError(f"Resume file not found: {args.resume}")
        return resume_path.read_text(encoding='utf-8')
    
    elif args.resume_text:
        return args.resume_text
    
    else:
        print("Please provide either --resume (file path) or --resume-text")
        resume_text = input("Enter your resume/background information:\n")
        return resume_text


if __name__ == '__main__':
    main()