"""
Ollama Client for Banter Bot
Local LLM integration using Ollama
"""

import requests
from typing import Optional


class OllamaClient:
    """Wrapper for Ollama local LLM API"""
    
    def __init__(self, model: str = "llama3.2:3b", base_url: str = "http://localhost:11434"):
        """
        Initialize Ollama client
        
        Args:
            model: Model to use (llama3.2:3b, mistral, gemma2:2b, etc.)
            base_url: Ollama API endpoint
        """
        self.model = model
        self.base_url = base_url
        self.api_url = f"{base_url}/api/generate"
        
        # Generation settings optimized for quick, conversational responses
        self.options = {
            'temperature': 0.9,  # High for creative/varied responses
            'top_p': 0.95,
            'top_k': 40,
            'num_predict': 150,  # Max tokens (1-2 sentences)
        }
    
    def generate_response(
        self, 
        user_input: str, 
        system_prompt: str, 
        conversation_context: str = ""
    ) -> str:
        """
        Generate a response from Ollama
        
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
            # Make request to Ollama
            response = requests.post(
                self.api_url,
                json={
                    'model': self.model,
                    'prompt': full_prompt,
                    'stream': False,
                    'options': self.options
                },
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Extract and clean the response
            ai_response = result.get('response', '').strip()
            
            # Remove any "You:" prefix if the model includes it
            if ai_response.startswith("You:"):
                ai_response = ai_response[4:].strip()
            
            # Sometimes models add extra context - take only first 1-2 sentences
            sentences = ai_response.split('.')
            if len(sentences) > 2:
                ai_response = '. '.join(sentences[:2]) + '.'
            
            return ai_response
            
        except requests.exceptions.ConnectionError:
            return "Error: Cannot connect to Ollama. Make sure Ollama is running (ollama serve)."
        except requests.exceptions.Timeout:
            return "Error: Ollama request timed out. Try a smaller model."
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Sorry, I had a brain freeze there. Try again?"
    
    def test_connection(self) -> bool:
        """Test if Ollama is running and model is available"""
        try:
            # Check if Ollama is running
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()
            
            # Check if our model is available
            models = response.json().get('models', [])
            model_names = [m['name'] for m in models]
            
            if self.model not in model_names:
                print(f"Model '{self.model}' not found. Available models: {model_names}")
                print(f"Run: ollama pull {self.model}")
                return False
            
            return True
            
        except Exception as e:
            print(f"Ollama connection test failed: {e}")
            print("Make sure Ollama is running: ollama serve")
            return False
    
    def list_available_models(self) -> list:
        """Get list of installed Ollama models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()
            models = response.json().get('models', [])
            return [m['name'] for m in models]
        except:
            return []
