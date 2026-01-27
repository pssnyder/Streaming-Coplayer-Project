"""
Quick Test Script for Banter Bot
Tests the LLM and persona system without requiring TTS/STT setup
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from persona import PersonaManager
from conversation import ConversationManager
from llm_client import LLMClient


def test_basic_workflow():
    """Test the core conversation flow"""
    print("=" * 60)
    print("BANTER BOT - QUICK TEST (Text-Only, No Audio)")
    print("=" * 60)
    print()
    
    # Load environment
    load_dotenv()
    
    # Check for API key
    if not os.getenv('GEMINI_API_KEY'):
        print("❌ ERROR: GEMINI_API_KEY not found in .env file")
        print("\nQuick setup:")
        print("1. Copy .env.example to .env")
        print("2. Get API key from: https://aistudio.google.com/app/apikey")
        print("3. Add it to .env as: GEMINI_API_KEY=your_key_here")
        return
    
    try:
        # Initialize components
        print("Initializing...")
        persona_manager = PersonaManager()
        conversation_manager = ConversationManager()
        llm_client = LLMClient()
        
        # Test API connection
        print("Testing Gemini API connection...")
        if llm_client.test_connection():
            print("✓ Gemini API connected!\n")
        else:
            print("✗ Gemini API test failed\n")
            return
        
        # Set Gary as active persona
        persona_manager.set_active_persona("gary")
        persona = persona_manager.active_persona
        
        print(f"Active Persona: {persona.name}")
        print(f"Trigger: '{persona.trigger_name}'")
        print("=" * 60)
        print()
        
        # Test phrases (gaming scenarios)
        test_conversations = [
            # Conversation 1: Triggered start
            ("Gary, that jump scare got me so bad", True),
            ("I need to heal like right now", False),  # Follow-up without trigger
            ("The game is broken, not me", False),     # Continued conversation
            
            # Break - simulate timeout
            ("TIMEOUT", True),
            
            # Conversation 2: New triggered start
            ("Gary, I've been running in circles for 10 minutes", True),
            ("What's the worst that could happen", False),
            
            # Single commentary test
            ("TIMEOUT", True),
            ("Ahhhh what was that!!??", True),  # Triggered
        ]
        
        for i, (user_input, needs_trigger) in enumerate(test_conversations):
            if user_input == "TIMEOUT":
                print("\n" + "─" * 60)
                print("⏱️  [Simulating conversation timeout - context reset]")
                print("─" * 60 + "\n")
                conversation_manager.end_conversation()
                continue
            
            # Check if should respond
            should_respond = False
            if persona.is_triggered(user_input):
                conversation_manager.start_conversation()
                should_respond = True
            elif conversation_manager.is_conversation_active():
                should_respond = True
            
            # Display user input
            print(f"💬 YOU: {user_input}")
            
            if not should_respond:
                print(f"   ⚠️  (Trigger '{persona.trigger_name}' not detected - no response)")
                print()
                continue
            
            # Get context and generate response
            context = conversation_manager.get_context_for_llm()
            
            print("   🤔 Generating response...", end=" ")
            response = llm_client.generate_response(
                user_input=user_input,
                system_prompt=persona.build_system_prompt(),
                conversation_context=context
            )
            
            print(f"\r   🎤 {persona.name.upper()}: {response}")
            print()
            
            # Update conversation history
            conversation_manager.add_exchange(user_input, response)
        
        print("=" * 60)
        print("✓ Test complete!")
        print("\nTo run the full interactive version:")
        print("  python src/main.py")
        
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_basic_workflow()
