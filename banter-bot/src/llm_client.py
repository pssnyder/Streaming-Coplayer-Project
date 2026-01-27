"""
LLM Client for Banter Bot
Handles communication with Google Gemini API
"""

import os
import google.generativeai as genai
from typing import Optional


class LLMClient:
    """Wrapper for Google Gemini API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found. Set it in .env file.")
        
        genai.configure(api_key=self.api_key)
        
        # Using Gemini 1.5 Flash for fast, conversational responses
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        self.generation_config = {
            'temperature': 0.9,  # Higher for more creative/varied responses
            'top_p': 0.95,
            'top_k': 40,
            'max_output_tokens': 100,  # Short responses only
        }
    
    def generate_response(
        self, 
        user_input: str, 
        system_prompt: str, 
        conversation_context: str = ""
    ) -> str:
        """
        Generate a response from the LLM
        
        Args:
            user_input: The user's current statement
            system_prompt: The persona's system prompt
            conversation_context: Recent conversation history
        
        Returns:
            AI-generated response string
        """
        # Build the full prompt
        full_prompt = f"""{system_prompt}

{conversation_context}

User: {user_input}
You:"""
        
        try:
            response = self.model.generate_content(
                full_prompt,
                generation_config=self.generation_config
            )
            
            # Extract and clean the response
            ai_response = response.text.strip()
            
            # Remove any "You:" prefix if the model includes it
            if ai_response.startswith("You:"):
                ai_response = ai_response[4:].strip()
            
            return ai_response
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Sorry, I had a brain freeze there. Try again?"
    
    def test_connection(self) -> bool:
        """Test if the API connection works"""
        try:
            response = self.model.generate_content("Say 'hello'")
            return len(response.text) > 0
        except Exception as e:
            print(f"API connection test failed: {e}")
            return False
