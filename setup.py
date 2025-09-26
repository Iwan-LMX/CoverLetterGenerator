"""Setup configuration for Cover Letter Generator package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = []
if (this_directory / "requirements.txt").exists():
    requirements = (this_directory / "requirements.txt").read_text().strip().split('\n')

setup(
    name="cover-letter-generator",
    version="0.1.0",
    author="Iwan Li",
    author_email="iwan.li@outlook.com",
    description="AI-powered cover letter generation from job postings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/cover-letter-generator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    include_package_data=True,
    package_data={
        'cover_letter_generator': ['../templates/*.txt'],
    },
    entry_points={
        "console_scripts": [
            "cover-letter-gen=cover_letter_generator.cli:main",
        ],
    },
    keywords="ai, cover letter, job application, automation, openai",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/cover-letter-generator/issues",
        "Source": "https://github.com/yourusername/cover-letter-generator",
    },
)