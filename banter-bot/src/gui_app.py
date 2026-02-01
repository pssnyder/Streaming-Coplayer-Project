"""
GUI Application for Banter Bot
Modern interface with audio controls and settings
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
from pathlib import Path
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent))

from persona import PersonaManager
from conversation import ConversationManager
from ollama_client import OllamaClient
from llm_client import LLMClient
from tts_client import TTSClient
from voice_listener import VoiceListener


class BanterBotGUI:
    """GUI Application for Banter Bot"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🎤 Banter Bot")
        self.root.geometry("800x600")
        
        # Initialize components
        load_dotenv()
        self.persona_manager = PersonaManager()
        self.conversation_manager = ConversationManager()
        
        # Choose LLM provider
        llm_provider = os.getenv('LLM_PROVIDER', 'ollama').lower()
        if llm_provider == 'ollama':
            self.llm_client = OllamaClient(
                model=os.getenv('OLLAMA_MODEL', 'llama3.2:3b'),
                base_url=os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
            )
        else:
            self.llm_client = LLMClient()
        
        self.tts_client = TTSClient()
        self.voice_listener = None
        
        # Settings
        self.commentary_mode = tk.BooleanVar(value=False)
        self.voice_mode = tk.BooleanVar(value=False)
        self.active_persona = None
        self.is_processing = False
        # Settings
        self.commentary_mode = tk.BooleanVar(value=False)
        self.active_persona = None
        self.is_processing = False
        
        self.setup_ui()
        
    def setup_ui(self):
        """Create the user interface"""
        
        # ===== TOP CONTROLS =====
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill=tk.X)
        
        # Persona selection
        
        # Voice mode toggle
        self.voice_button = ttk.Checkbutton(control_frame, text="🎤 Voice Mode", 
                                           variable=self.voice_mode,
                                           command=self.toggle_voice_mode)
        self.voice_button.pack(side=tk.LEFT, padx=5)
        ttk.Label(control_frame, text="Persona:").pack(side=tk.LEFT, padx=5)
        self.persona_var = tk.StringVar()
        persona_choices = [f"{name} ({trigger})" for name, trigger in self.persona_manager.list_personas()]
        self.persona_combo = ttk.Combobox(control_frame, textvariable=self.persona_var, 
                                          values=persona_choices, width=25, state="readonly")
        self.persona_combo.pack(side=tk.LEFT, padx=5)
        self.persona_combo.current(0)
        self.persona_combo.bind('<<ComboboxSelected>>', self.on_persona_change)
        
        # Commentary mode toggle
        ttk.Checkbutton(control_frame, text="Commentary Mode", 
                       variable=self.commentary_mode).pack(side=tk.LEFT, padx=20)
        
        # Clear conversation button
        ttk.Button(control_frame, text="Clear Conversation", 
                  command=self.clear_conversation).pack(side=tk.LEFT, padx=5)
        
        # ===== CONVERSATION DISPLAY =====
        conversation_frame = ttk.LabelFrame(self.root, text="Conversation", padding="10")
        conversation_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.conversation_display = scrolledtext.ScrolledText(
            conversation_frame, 
            wrap=tk.WORD, 
            height=20,
            font=("Segoe UI", 10),
            state=tk.DISABLED
        )
        self.conversation_display.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for colors
        self.conversation_display.tag_config("user", foreground="#0066cc", font=("Segoe UI", 10, "bold"))
        self.conversation_display.tag_config("ai", foreground="#00aa00", font=("Segoe UI", 10, "bold"))
        self.conversation_display.tag_config("system", foreground="#666666", font=("Segoe UI", 9, "italic"))
        
        # ===== INPUT AREA =====
        input_frame = ttk.Frame(self.root, padding="10")
        input_frame.pack(fill=tk.X)
        
        # Input text box
        self.input_text = tk.Entry(input_frame, font=("Segoe UI", 11))
        self.input_text.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.input_text.bind('<Return>', lambda e: self.send_message())
        
        # Send button
        self.send_button = ttk.Button(input_frame, text="Send", command=self.send_message, width=10)
        self.send_button.pack(side=tk.LEFT)
        
        # ===== STATUS BAR =====
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Set initial persona after all widgets are created
        self.on_persona_change(None)
    
    def toggle_voice_mode(self):
        """Toggle voice listening on/off"""
        if self.voice_mode.get():
            # Start voice listener
            try:
                self.voice_listener = VoiceListener(on_speech_detected=self.on_voice_input)
                self.voice_listener.start()
                self.add_system_message("🎤 Voice mode activated - speak naturally!")
                self.status_var.set("Listening...")
            except Exception as e:
                self.add_system_message(f"Voice mode error: {e}")
                self.voice_mode.set(False)
        else:
            # Stop voice listener
            if self.voice_listener:
                self.voice_listener.stop()
                self.voice_listener = None
            self.add_system_message("Voice mode deactivated")
            self.status_var.set("Ready")
    
    def on_voice_input(self, transcript: str):
        """Handle voice input from continuous listening"""
        if not transcript.strip():
            return
        
        # Process the transcript as if it were typed
        self.root.after(0, lambda: self.process_message(transcript))
    
    def on_persona_change(self, event):
        self.input_text.bind('<Return>', lambda e: self.send_message())
        
        # Send button
        self.send_button = ttk.Button(input_frame, text="Send", command=self.send_message, width=10)
        self.send_button.pack(side=tk.LEFT)
        
        # ===== STATUS BAR =====
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Set initial persona after all widgets are created
        self.on_persona_change(None)
        
    def on_persona_change(self, event):
        """Handle persona selection change"""
        selected = self.persona_combo.current()
        personas = list(self.persona_manager.personas.values())
        if 0 <= selected < len(personas):
            self.active_persona = personas[selected]
            self.persona_manager.active_persona = self.active_persona
            self.add_system_message(f"Active persona: {self.active_persona.name} (trigger: '{self.active_persona.trigger_name}')")
    
    def clear_conversation(self):
        """Clear conversation history"""
        self.conversation_manager.end_conversation()
        self.conversation_display.config(state=tk.NORMAL)
        self.conversation_display.delete(1.0, tk.END)
        self.conversation_display.config(state=tk.DISABLED)
        self.add_system_message("Conversation cleared")
    
    def add_system_message(self, message):
        """Add a system message to the display"""
        self.conversation_display.config(state=tk.NORMAL)
        self.conversation_display.insert(tk.END, f"[{message}]\n\n", "system")
        self.conversation_display.see(tk.END)
        self.conversation_display.config(state=tk.DISABLED)
    
    def add_user_message(self, message):
        """Add a user message to the display"""
        self.conversation_display.config(state=tk.NORMAL)
        self.conversation_display.insert(tk.END, "You: ", "user")
        self.conversation_display.insert(tk.END, f"{message}\n")
        self.conversation_display.see(tk.END)
        self.conversation_display.config(state=tk.DISABLED)
    
    def add_ai_message(self, message):
        """Add an AI message to the display"""
        self.conversation_display.config(state=tk.NORMAL)
        self.conversation_display.insert(tk.END, f"{self.active_persona.name}: ", "ai")
        self.conversation_display.insert(tk.END, f"{message}\n\n")
        self.conversation_display.see(tk.END)
        self.conversation_display.config(state=tk.DISABLED)
    
    def send_message(self):
        """Process and send user message"""
        if self.is_processing:
            return
        
        user_input = self.input_text.get().strip()
        if not user_input:
            return
        
        # Clear input
        self.input_text.delete(0, tk.END)
        
        # Process in background thread
        threading.Thread(target=self.process_message, args=(user_input,), daemon=True).start()
    
    def process_message(self, user_input):
        """Process message in background thread"""
        self.is_processing = True
        self.root.after(0, lambda: self.status_var.set("Processing..."))
        self.root.after(0, lambda: self.send_button.config(state=tk.DISABLED))
        
        try:
            # Add user message to display
            self.root.after(0, lambda: self.add_user_message(user_input))
            
            # Check if we should respond
            should_respond = False
            
            if self.commentary_mode.get():
                should_respond = True
            elif self.active_persona.is_triggered(user_input):
                self.conversation_manager.start_conversation()
                should_respond = True
            elif self.conversation_manager.is_conversation_active():
                should_respond = True
            
            if not should_respond:
                self.root.after(0, lambda: self.add_system_message(
                    f"Trigger '{self.active_persona.trigger_name}' not detected. Use trigger name to start conversation."
                ))
                return
            
            # Get conversation context
            context = self.conversation_manager.get_context_for_llm()
            
            # Generate response
            response = self.llm_client.generate_response(
                user_input=user_input,
                system_prompt=self.active_persona.build_system_prompt(),
                conversation_context=context
            )
            
            # Add AI response to display
            self.root.after(0, lambda: self.add_ai_message(response))
            
            # Synthesize and play audio
            self.root.after(0, lambda: self.status_var.set("Speaking..."))
            audio = self.tts_client.synthesize(response)
            self.tts_client.play_audio(audio)
            
            # Update conversation history
            self.conversation_manager.add_exchange(user_input, response)
            
        except Exception as e:
            self.root.after(0, lambda: self.add_system_message(f"Error: {str(e)}"))
        
        finally:
            self.is_processing = False
            self.root.after(0, lambda: self.status_var.set("Ready"))
            self.root.after(0, lambda: self.send_button.config(state=tk.NORMAL))


def main():
    """Launch the GUI application"""
    root = tk.Tk()
    app = BanterBotGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
