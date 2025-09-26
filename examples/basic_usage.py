"""Basic usage example for Cover Letter Generator."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from cover_letter_generator import CoverLetterAgent

def main():
    """Example usage of the Cover Letter Generator."""
    
    # Initialize the agent
    agent = CoverLetterAgent()
    
    # Example 1: Generate from URL
    job_url = "https://example.com/job-posting"
    resume_info = """
    I am a software engineer with 3 years of experience in Python, JavaScript, and web development.
    I have worked on several projects involving API development, frontend frameworks like React,
    and database management. I'm passionate about creating clean, efficient code and solving
    complex problems.
    """
    
    try:
        # Generate cover letter from job URL
        result = agent.generate_from_url(
            job_url=job_url,
            resume_info=resume_info,
            output_filename="my_cover_letter.txt"
        )
        
        print("✅ Cover letter generated successfully!")
        print(f"Saved to: {result['output_path']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Example 2: Generate from job description text
    job_description = """
    We are looking for a Python Developer to join our team.
    Requirements:
    - 2+ years of Python experience
    - Experience with web frameworks (Django/Flask)
    - Knowledge of databases (PostgreSQL/MySQL)
    - Git version control
    """
    
    try:
        result = agent.generate_from_text(
            job_description=job_description,
            resume_info=resume_info,
            company_name="Tech Corp",
            position_title="Python Developer"
        )
        
        print("✅ Cover letter generated from text!")
        print(f"Saved to: {result['output_path']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()