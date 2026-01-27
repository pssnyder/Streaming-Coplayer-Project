"""
Banter Bot - Main Application
Conversational AI companion for streamers and solo gamers
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from persona import PersonaManager
from conversation import ConversationManager
from llm_client import LLMClient
from tts_client import TTSClient
from stt_client import STTClient


# Initialize colorama for colored terminal output
init()


class BanterBot:
    """Main application controller"""
    
    def __init__(self):
        print(f"{Fore.CYAN}╔══════════════════════════════════════╗")
        print(f"║      🎤 BANTER BOT v1.0 🎤          ║")
        print(f"╚══════════════════════════════════════╝{Style.RESET_ALL}\n")
        
        # Load environment variables
        load_dotenv()
        
        # Initialize components
        print(f"{Fore.YELLOW}Initializing components...{Style.RESET_ALL}")
        
        self.persona_manager = PersonaManager()
        self.conversation_manager = ConversationManager()
        self.llm_client = LLMClient()
        self.tts_client = TTSClient()
        self.stt_client = STTClient()
        
        # Settings
        self.commentary_mode = False
        self.use_voice_input = False  # Start with text, can enable voice
        
        print(f"{Fore.GREEN}✓ All systems ready!{Style.RESET_ALL}\n")
    
    def select_persona(self):
        """Let user choose a persona"""
        personas = self.persona_manager.list_personas()
        
        print(f"{Fore.CYAN}Available Personas:{Style.RESET_ALL}")
        for i, (name, trigger) in enumerate(personas, 1):
            print(f"  {i}. {name} (trigger: '{trigger}')")
        
        while True:
            choice = input(f"\n{Fore.YELLOW}Select persona (1-{len(personas)}): {Style.RESET_ALL}")
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(personas):
                    trigger_name = personas[idx][1]
                    self.persona_manager.set_active_persona(trigger_name)
                    return
            except ValueError:
                pass
            print(f"{Fore.RED}Invalid choice. Try again.{Style.RESET_ALL}")
    
    def configure_settings(self):
        """Configure commentary mode and input method"""
        print(f"\n{Fore.CYAN}Settings:{Style.RESET_ALL}")
        
        # Commentary mode
        commentary = input(f"Enable commentary mode? (AI responds without trigger name) [y/N]: ").lower()
        self.commentary_mode = commentary == 'y'
        
        # Input method
        voice = input(f"Use voice input? (Otherwise text input) [y/N]: ").lower()
        self.use_voice_input = voice == 'y'
        
        print(f"\n{Fore.GREEN}Configuration:{Style.RESET_ALL}")
        print(f"  • Commentary Mode: {'ON' if self.commentary_mode else 'OFF'}")
        print(f"  • Input Method: {'Voice' if self.use_voice_input else 'Text'}")
        print()
    
    def process_input(self, user_input: str):
        """Process user input and generate response"""
        if not user_input.strip():
            return
        
        persona = self.persona_manager.active_persona
        if not persona:
            print(f"{Fore.RED}No persona selected!{Style.RESET_ALL}")
            return
        
        # Check if we should respond
        should_respond = False
        
        if self.commentary_mode:
            # In commentary mode, always respond
            should_respond = True
        elif persona.is_triggered(user_input):
            # Trigger name detected - start/continue conversation
            self.conversation_manager.start_conversation()
            should_respond = True
        elif self.conversation_manager.is_conversation_active():
            # In active conversation - continue without trigger
            should_respond = True
        
        if not should_respond:
            print(f"{Fore.YELLOW}(Trigger '{persona.trigger_name}' not detected. Use trigger name to start conversation){Style.RESET_ALL}")
            return
        
        # Display user input
        print(f"{Fore.BLUE}You: {user_input}{Style.RESET_ALL}")
        
        # Get conversation context
        context = self.conversation_manager.get_context_for_llm()
        
        # Generate response
        print(f"{Fore.YELLOW}🤔 Thinking...{Style.RESET_ALL}", end="\r")
        response = self.llm_client.generate_response(
            user_input=user_input,
            system_prompt=persona.build_system_prompt(),
            conversation_context=context
        )
        
        # Display response
        print(f"{Fore.GREEN}{persona.name}: {response}{Style.RESET_ALL}")
        
        # Synthesize and play audio
        print(f"{Fore.YELLOW}🔊 Speaking...{Style.RESET_ALL}", end="\r")
        audio = self.tts_client.synthesize(response)
        self.tts_client.play_audio(audio)
        print(" " * 50, end="\r")  # Clear status line
        
        # Update conversation history
        self.conversation_manager.add_exchange(user_input, response)
    
    def run_text_mode(self):
        """Run in text input mode"""
        print(f"{Fore.CYAN}{'─' * 50}")
        print(f"Text Input Mode")
        print(f"• Type your messages and press Enter")
        print(f"• Use trigger name '{self.persona_manager.active_persona.trigger_name}' to start conversation")
        print(f"• Type 'quit' to exit")
        print(f"{'─' * 50}{Style.RESET_ALL}\n")
        
        while True:
            try:
                user_input = input(f"{Fore.MAGENTA}> {Style.RESET_ALL}")
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print(f"{Fore.CYAN}Goodbye!{Style.RESET_ALL}")
                    break
                
                self.process_input(user_input)
                print()  # Blank line between exchanges
                
            except KeyboardInterrupt:
                print(f"\n{Fore.CYAN}Goodbye!{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
    
    def run_voice_mode(self):
        """Run in voice input mode with continuous listening"""
        print(f"{Fore.CYAN}{'─' * 50}")
        print(f"Voice Input Mode")
        print(f"• Speak into your microphone")
        print(f"• Use trigger name '{self.persona_manager.active_persona.trigger_name}' to start conversation")
        print(f"• Press Ctrl+C to exit")
        print(f"{'─' * 50}{Style.RESET_ALL}\n")
        
        current_transcript = ""
        
        def on_transcript(transcript: str, is_final: bool):
            nonlocal current_transcript
            
            if is_final:
                # Final transcript - process it
                print(f"\r{' ' * 100}\r", end="")  # Clear line
                self.process_input(transcript)
                print()
                current_transcript = ""
            else:
                # Interim result - show what's being said
                current_transcript = transcript
                print(f"\r{Fore.YELLOW}🎤 {transcript}{Style.RESET_ALL}", end="")
        
        self.stt_client.listen_continuous(on_transcript)
    
    def run(self):
        """Main entry point"""
        self.select_persona()
        self.configure_settings()
        
        if self.use_voice_input:
            self.run_voice_mode()
        else:
            self.run_text_mode()


def main():
    """Application entry point"""
    try:
        bot = BanterBot()
        bot.run()
    except Exception as e:
        print(f"{Fore.RED}Fatal error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
