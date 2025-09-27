# Cover Letter Generator 🤖

An AI-powered tool that automatically generates professional cover letters from job posting URLs or job descriptions. This LLM agent uses OpenAI's GPT models to create personalized cover letters based on your resume and the specific job requirements.

Here's a video might help you to quick start it https://www.youtube.com/watch?v=x40EMedih4g
## Features ✨

- 🔗 **URL Scraping**: Extract job details directly from job posting URLs
- 🤖 **AI Generation**: Create tailored cover letters using OpenAI's GPT models  
- � **Multi-Format Resume**: Support PDF, Word (.docx), text, and markdown resumes
- �📝 **Text Input**: Generate from job description text if you don't have a URL
- 💾 **File Management**: Automatic saving with timestamps
- 🔧 **CLI Interface**: Easy-to-use command line interface
- 📦 **Pip Installable**: Can be installed as a Python package

## Installation 📦

### Option 1: Install from source
```bash
git clone https://github.com/Iwan-LMX/CoverLetterGenerator.git
cd CoverLetterGenerator
pip install -e .
```

### Option 2: Install from PyPI (when published)
```bash
pip install cover-letter-generator
```

### Option 3: Development setup
```bash
git clone https://github.com/Iwan-LMX/CoverLetterGenerator.git
cd CoverLetterGenerator
pip install -r requirements.txt
```

## Quick Start 🚀

### 1. Setup
First, set your LLM provider API key:

**For OpenAI GPT models:**
```cmd
set API_KEY=sk-proj-your_openai_key_here
set LLM_MODEL=gpt-3.5-turbo
```

**For Google Gemini models:**
```cmd
set API_KEY=AIzaSy_your_google_key_here
set LLM_MODEL=gemini-2.5-flash
```

**For Anthropic Claude models:**
```cmd
set API_KEY=sk-ant-your_anthropic_key_here
set LLM_MODEL=claude-3-sonnet-20240229
```

Run the setup command:
```bash
cover-letter-gen setup
```

### 2. Generate from Job URL
```bash
cover-letter-gen url "https://jobs.example.com/software-engineer" --resume resume.txt
```

### 3. Generate from Job Description File
```bash
cover-letter-gen text job_description.txt --resume resume.txt --company "Tech Corp" --position "Software Engineer"
```

## Usage Examples 📖

### Command Line Interface

#### Generate from URL with PDF resume:
```bash
cover-letter-gen url "https://careers.company.com/job/123" \
  --resume my_resume.pdf \
  --output my_cover_letter.txt
```

#### Generate with Word document resume:
```bash
cover-letter-gen url "https://careers.company.com/job/123" \
  --resume my_resume.docx \
  --output my_cover_letter.txt
```

#### Generate from job description text:
```bash
cover-letter-gen text job_posting.txt \
  --resume my_resume.pdf \
  --company "Amazing Corp" \
  --position "Senior Developer"
```

#### Generate with resume text (no file):
```bash
cover-letter-gen text job_posting.txt \
  --resume-text "I am a software engineer with 5 years experience..." \
  --company "Amazing Corp" \
  --position "Senior Developer"
```

#### Preview job data before generating:
```bash
cover-letter-gen preview "https://careers.company.com/job/123"
```

### Python API

```python
from cover_letter_generator import CoverLetterAgent

# Initialize the agent
agent = CoverLetterAgent()

# Generate from URL
result = agent.generate_from_url(
    job_url="https://careers.company.com/job/123",
    resume_info="I am a software engineer with...",
    output_filename="cover_letter.txt"
)

# Generate from text
result = agent.generate_from_text(
    job_description="We are looking for a Python developer...",
    resume_info="I have 3 years of Python experience...",
    company_name="Tech Corp",
    position_title="Python Developer"
)

print(f"Cover letter saved to: {result['output_path']}")
```

## Project Structure 📁

```
CoverLetterGenerator/
├── cover_letter_generator/          # Main package
│   ├── __init__.py                  # Package exports
│   ├── agent.py                     # Main agent orchestrator
│   ├── llm.py                       # LLM interface (OpenAI)
│   ├── tools.py                     # Web scraping & file tools
│   ├── config.py                    # Configuration management
│   └── cli.py                       # Command line interface
├── templates/                       # Cover letter templates
├── examples/                        # Usage examples
├── tests/                          # Unit tests
├── requirements.txt                # Dependencies
├── setup.py                       # Package installation
├── pyproject.toml                 # Modern Python packaging
└── README.md                      # This file
```

## Configuration ⚙️

### Environment Variables
- `API_KEY`: Your LLM provider API key (required)
- `LLM_MODEL`: Model to use (supports OpenAI, Google, Anthropic models)

### Supported LLM Providers
- **OpenAI**: `gpt-3.5-turbo`, `gpt-4`, etc.
- **Google Gemini**: `gemini-pro`, `gemini-2.5-flash`, etc.  
- **Anthropic Claude**: `claude-3-sonnet-20240229`, etc.

### File Locations
- Templates: `templates/cover_letter_template.txt`
- Output: `output/` directory (created automatically)

## Supported Resume Formats 📄

The agent can automatically parse resumes in multiple formats:
- **PDF** (.pdf) - Most common format
- **Word Documents** (.docx) - Microsoft Word files
- **Text Files** (.txt) - Plain text resumes
- **Markdown** (.md) - Formatted text files

The parser automatically extracts text content from these files, making it easy to use your existing resume without conversion.

## Supported Job Sites 🌐

The web scraper works with most job posting sites including:
- LinkedIn Jobs
- Indeed
- Glassdoor
- Workable (job application sites)
- Company career pages
- Any site with standard HTML job postings or structured data

## Development 🛠️

### Running Tests
```bash
python -m pytest tests/
```

### Installing in Development Mode
```bash
pip install -e .
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Troubleshooting 🔍

### Common Issues

**API Key Error:**
- Make sure you've set the `OPENAI_API_KEY` environment variable
- Verify your API key is valid and has sufficient credits

**Web Scraping Issues:**
- Some sites may block automated scraping
- Try copying the job description text and use the `text` command instead

**Import Errors:**
- Make sure you've installed all requirements: `pip install -r requirements.txt`
- If using development mode, install with: `pip install -e .`

## License 📄

MIT License - see LICENSE file for details.

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.
