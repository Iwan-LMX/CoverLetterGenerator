"""LLM interface for interacting with language models."""

from typing import Dict, List, Optional
from .config import Settings


class LLMClient:
    """Client for interacting with various LLM providers."""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """Initialize the LLM client.
        
        Args:
            api_key: API key for the LLM provider. If None, uses Settings.API_KEY
            model: Model name. If None, uses Settings.MODEL_NAME
        """
        self.api_key = api_key or Settings.API_KEY
        self.model = model or Settings.MODEL_NAME
        
        # Detect provider based on model name
        self.provider = self._detect_provider(self.model)
        
        # Initialize the appropriate client
        self._init_client()
    
    def _detect_provider(self, model: str) -> str:
        """Detect LLM provider based on model name."""
        model_lower = model.lower()
        
        if 'gpt' in model_lower or 'openai' in model_lower:
            return 'openai'
        elif 'gemini' in model_lower or 'google' in model_lower:
            return 'google'
        elif 'claude' in model_lower or 'anthropic' in model_lower:
            return 'anthropic'
        else:
            # Default to OpenAI for unknown models
            return 'openai'
    
    def _init_client(self):
        """Initialize the appropriate client based on provider."""
        if self.provider == 'openai':
            self._init_openai()
        elif self.provider == 'google':
            self._init_google()
        elif self.provider == 'anthropic':
            self._init_anthropic()
    
    def _init_openai(self):
        """Initialize OpenAI client."""
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError("OpenAI package required. Install with: pip install openai")
    
    def _init_google(self):
        """Initialize Google Gemini client."""
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel(self.model)
        except ImportError:
            raise ImportError("Google Generative AI package required. Install with: pip install google-generativeai")
    
    def _init_anthropic(self):
        """Initialize Anthropic client."""
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.api_key)
        except ImportError:
            raise ImportError("Anthropic package required. Install with: pip install anthropic")
    
    def generate_text(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7, retry_count: int = 2) -> str:
        """Generate text using the language model.
        
        Args:
            prompt: The input prompt
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0-1)
            retry_count: Number of retries if generation fails
            
        Returns:
            Generated text
        """
        last_error = None
        
        for attempt in range(retry_count + 1):
            try:
                if self.provider == 'openai':
                    return self._generate_openai(prompt, max_tokens, temperature)
                elif self.provider == 'google':
                    return self._generate_google(prompt, max_tokens, temperature)
                elif self.provider == 'anthropic':
                    return self._generate_anthropic(prompt, max_tokens, temperature)
                else:
                    raise ValueError(f"Unsupported provider: {self.provider}")
                    
            except Exception as e:
                last_error = e
                if attempt < retry_count:
                    print(f"⚠️  Attempt {attempt + 1} failed: {str(e)}")
                    print(f"🔄 Retrying with slightly different parameters...")
                    # Slightly adjust temperature for retry
                    temperature = max(0.1, temperature - 0.1)
                    continue
                else:
                    break
        
        # If all retries failed, raise the last error with helpful context
        error_msg = f"Error generating text with {self.provider}: {str(last_error)}"
        
        if self.provider == 'google' and ('safety' in str(last_error).lower() or 'blocked' in str(last_error).lower()):
            error_msg += "\n\n💡 Suggestion: Google Gemini has strict safety filters. Try:\n"
            error_msg += "   1. Using more neutral, professional language\n"
            error_msg += "   2. Switching to OpenAI: set LLM_MODEL=gpt-3.5-turbo\n"
            error_msg += "   3. Simplifying the job description or resume content"
        
        raise Exception(error_msg)
    
    def _generate_openai(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """Generate text using OpenAI API."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content.strip()
    
    def _generate_google(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """Generate text using Google Gemini API."""
        import google.generativeai as genai
        
        # Configure generation parameters
        generation_config = genai.GenerationConfig(
            max_output_tokens=max_tokens,
            temperature=temperature,
        )
        
        # Configure safety settings to be less restrictive for business content
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH", 
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]
        
        try:
            response = self.client.generate_content(
                prompt,
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            
            # Check if response was blocked
            if response.candidates:
                candidate = response.candidates[0]
                if candidate.finish_reason == 2:  # SAFETY
                    raise Exception("Content was blocked by safety filters. Try rephrasing your request or use a different model.")
                elif candidate.finish_reason == 3:  # RECITATION
                    raise Exception("Content was blocked due to recitation. Try using more original content.")
                elif candidate.finish_reason == 4:  # OTHER
                    raise Exception("Content generation failed for unknown reasons.")
            
            # Check if we have valid text
            if hasattr(response, 'text') and response.text:
                return response.text.strip()
            else:
                # Try to extract text from parts if direct text access fails
                if response.candidates and response.candidates[0].content.parts:
                    parts_text = ""
                    for part in response.candidates[0].content.parts:
                        if hasattr(part, 'text'):
                            parts_text += part.text
                    if parts_text:
                        return parts_text.strip()
                
                raise Exception("No text content was generated. The response may have been filtered.")
                
        except Exception as e:
            if "safety" in str(e).lower() or "blocked" in str(e).lower():
                raise Exception("Content was filtered by Gemini's safety system. Try rephrasing your request to be more neutral, or consider using a different LLM model.")
            else:
                raise e
    
    def _generate_anthropic(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """Generate text using Anthropic Claude API."""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()
    
    def generate_cover_letter(self, job_description: str, resume_info: str, 
                            company_name: str = "", position_title: str = "") -> str:
        """Generate a cover letter based on job description and resume.
        
        Args:
            job_description: The job posting description
            resume_info: User's resume information
            company_name: Name of the company
            position_title: Title of the position
            
        Returns:
            Generated cover letter
        """
        # Create a safer, more structured prompt for Gemini
        prompt = f"""Write a professional business cover letter.

Company Name: {company_name or 'the organization'}
Job Title: {position_title or 'the position'}

Requirements from Job Description:
{job_description[:1500]}

Candidate Background:
{resume_info[:1500]}

Format the cover letter with:
- Professional greeting
- Opening paragraph expressing interest
- 2-3 body paragraphs highlighting relevant qualifications
- Professional closing
- Appropriate business letter structure

Please write a concise, professional cover letter (300-500 words)."""
        
        return self.generate_text(prompt, max_tokens=800, temperature=0.7)