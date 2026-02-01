"""
Test Ollama integration
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from ollama_client import OllamaClient

def test_ollama():
    print("Testing Ollama connection...")
    print("=" * 60)
    
    # Try different models in order of preference
    models_to_try = [
        "llama3.2:3b",      # Fast, good quality (3B params)
        "gemma2:2b",        # Very fast, decent quality (2B params)
        "mistral",          # Good quality but slower (7B params)
        "llama3.2:1b",      # Fastest, basic quality (1B params)
    ]
    
    client = None
    
    for model in models_to_try:
        print(f"\nTrying model: {model}")
        test_client = OllamaClient(model=model)
        
        if test_client.test_connection():
            print(f"✓ Connected with model: {model}")
            client = test_client
            break
        else:
            print(f"✗ Model {model} not available")
    
    if not client:
        print("\n❌ No Ollama models found!")
        print("\nQuick setup:")
        print("1. Make sure Ollama is running:")
        print("   ollama serve")
        print("\n2. Pull a fast model:")
        print("   ollama pull llama3.2:3b")
        return
    
    print("\n" + "=" * 60)
    print("Testing responses with Gary persona...")
    print("=" * 60 + "\n")
    
    # Simple system prompt
    system_prompt = """You are Gary, a sarcastic gaming companion. 
Keep responses to 1-2 sentences max. Be witty and roast mistakes. 
Use casual language."""
    
    # Test phrases
    test_inputs = [
        "Gary, that jump scare got me so bad",
        "I need to heal like right now",
        "The game is broken, not me",
    ]
    
    for user_input in test_inputs:
        print(f"💬 YOU: {user_input}")
        print(f"   🤔 Generating...", end=" ", flush=True)
        
        response = client.generate_response(
            user_input=user_input,
            system_prompt=system_prompt,
            conversation_context=""
        )
        
        print(f"\r   🎤 GARY: {response}")
        print()
    
    print("=" * 60)
    print("✓ Ollama test complete!")
    print(f"\nModel used: {client.model}")
    print("\nAvailable models:", client.list_available_models())

if __name__ == "__main__":
    test_ollama()
