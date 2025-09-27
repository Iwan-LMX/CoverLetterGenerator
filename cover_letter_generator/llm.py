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
            
            # Configure with API key
            genai.configure(api_key=self.api_key)
            
            # Disable safety filters completely (like Cherry Studio likely does)
            safety_config = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH", 
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE"
                }
            ]
            
            self.client = genai.GenerativeModel(
                model_name=self.model,
                safety_settings=safety_config
            )
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
        """Generate text using Google Gemini API (Cherry Studio compatible)."""
        import google.generativeai as genai
        
        # Use simple configuration like Cherry Studio
        generation_config = {
            "max_output_tokens": max_tokens,
            "temperature": temperature,
            "top_p": 0.8,
            "top_k": 40
        }
        
        try:
            # Use the simplest approach possible
            response = self.client.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            # Simple response handling - if there's text, return it
            # print("DEBUG: ", response)
            if response and response.text:
                return response.text.strip()
            
            # If no direct text, try to extract from parts
            if response.candidates and len(response.candidates) > 0:
                candidate = response.candidates[0]
                
                # Check for content in parts
                if candidate.content and candidate.content.parts:
                    text_parts = []
                    for part in candidate.content.parts:
                        if hasattr(part, 'text') and part.text:
                            text_parts.append(part.text)
                    
                    if text_parts:
                        return " ".join(text_parts).strip()
                
                # Provide more specific error based on finish_reason
                finish_reason = getattr(candidate, 'finish_reason', None)
                if finish_reason == 2:
                    raise Exception("Content blocked by safety filter. Gemini flagged the content as potentially unsafe.")
                elif finish_reason == 3:
                    raise Exception("Content blocked due to recitation detection.")
                elif finish_reason == 4:
                    raise Exception("Generation stopped due to other reasons.")
                
            raise Exception("No content generated - empty response from Gemini.")
                
        except Exception as e:
            # Re-raise with original error message for better debugging
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
        # Load the template
        from .tools import FileHandler
        try:
            template = FileHandler.read_template()
        except:
            # Fallback template if file doesn't exist
            template = """Dear Hiring Manager,

I am writing to express my strong interest in the {position} position at {company}. With my background in {relevant_experience}, I am excited about the opportunity to contribute to your team.

{body_paragraph_1}

{body_paragraph_2}

Thank you for considering my application. I look forward to discussing how my skills and experience can benefit your organization.

Sincerely,
[Your Name]"""
        
        # Create a comprehensive but safe prompt that includes actual resume and job data
        prompt = f"""You are a professional cover letter writer. Please create a personalized cover letter using the template and information provided.

TEMPLATE TO FOLLOW:
{template}

COMPANY: {company_name or 'the organization'}
POSITION: {position_title or 'the position'}

JOB REQUIREMENTS (first 2000 chars):
{job_description[:2000]}

CANDIDATE BACKGROUND (first 800 chars):
{resume_info[:800]}

INSTRUCTIONS:
1. Follow the template structure exactly
2. Replace {{position}} with the actual position title
3. Replace {{company}} with the company name  
4. Replace {{relevant_experience}} with specific skills from the candidate's background that match the job
5. Write {{body_paragraph_1}} highlighting the candidate's most relevant experience for this specific job
6. Write {{body_paragraph_2}} showing enthusiasm and knowledge about the company/role
7. Keep it professional and concise
8. Use specific examples from the candidate's background when possible

Please write the complete cover letter now:"""
        
        return self.generate_text(prompt, max_tokens=3000, temperature=0.7)