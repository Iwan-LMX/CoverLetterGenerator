"""Test different LLM providers and diagnose Gemini issues."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_gemini_safety():
    """Test what might be causing Gemini safety filters to trigger."""
    print("🔍 Gemini Safety Filter Diagnosis")
    print("=" * 40)
    
    # Common content that might trigger safety filters
    potential_triggers = [
        "Personal information (names, emails, phone numbers)",
        "Specific company names or job descriptions", 
        "Resume content with personal details",
        "Long text blocks (>1500 characters)",
        "Certain words or phrases in job descriptions"
    ]
    
    print("Possible causes for safety filter activation:")
    for i, trigger in enumerate(potential_triggers, 1):
        print(f"{i}. {trigger}")
    
    print(f"\n🛠️  Debugging Steps:")
    print("1. Try with a minimal test first")
    print("2. Remove personal information from resume")
    print("3. Use generic job description")
    print("4. Switch to OpenAI if Gemini continues to block")
    
    print(f"\n💡 Quick Fix - Switch to OpenAI:")
    print("Edit your .env file and change:")
    print('  LLM_MODEL="gpt-3.5-turbo"')
    print('  API_KEY="sk-proj-your_openai_key"')
    

def create_minimal_test():
    """Create a minimal test to see if basic Gemini functionality works."""
    print(f"\n🧪 Minimal Gemini Test")
    print("-" * 25)
    
    test_prompt = """Write a short professional cover letter for a software engineer position. 
    
The candidate has experience in Python and web development.
The company is looking for someone with programming skills.

Please write a brief, professional cover letter."""
    
    print("Minimal test prompt:")
    print(f'"{test_prompt}"')
    print()
    print("If this simple prompt also fails, the issue is likely:")
    print("• API key configuration")
    print("• Regional restrictions") 
    print("• Gemini model availability")
    print("• Network/firewall issues")


def show_openai_switch():
    """Show how to switch to OpenAI."""
    print(f"\n🔄 Switch to OpenAI (Recommended)")
    print("-" * 35)
    
    print("1. Get OpenAI API key from: https://platform.openai.com/api-keys")
    print("2. Edit your .env file:")
    print()
    print("   # Comment out Gemini config")
    print('   # API_KEY="AIzaSy..."')
    print('   # LLM_MODEL="gemini-2.5-flash"')
    print()
    print("   # Add OpenAI config")
    print('   API_KEY="sk-proj-your_openai_key_here"')
    print('   LLM_MODEL="gpt-3.5-turbo"')
    print()
    print("3. Test with the same command:")
    print("   python -m cover_letter_generator.cli url <job-url> --resume resume.pdf")
    print()
    print("✅ OpenAI GPT models are generally more reliable for business use cases")


def main():
    """Run LLM provider diagnostics."""
    print("🚨 LLM Provider Issue Diagnostics")
    print("=" * 50)
    
    test_gemini_safety()
    create_minimal_test()
    show_openai_switch()
    
    print(f"\n📊 Comparison:")
    print("Google Gemini:")
    print("  ✅ Free tier available")
    print("  ✅ Good performance") 
    print("  ❌ Strict safety filters")
    print("  ❌ May block legitimate business content")
    print()
    print("OpenAI GPT:")
    print("  ✅ Reliable for business use")
    print("  ✅ Less restrictive safety filters")  
    print("  ✅ Proven track record")
    print("  💰 Requires paid API key")
    print()
    print("🎯 Recommendation: Use OpenAI GPT for production cover letter generation")


if __name__ == "__main__":
    main()