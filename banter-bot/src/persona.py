"""
Persona Management for Banter Bot
Loads and manages AI personality configurations
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional


class Persona:
    """Represents an AI personality with trigger detection and prompt building"""
    
    def __init__(self, config_path: str):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.name = self.config['name']
        self.trigger_name = self.config['trigger_name'].lower()
        self.personality = self.config['personality']
        self.directives = self.config['directives']
        self.example_responses = self.config.get('example_responses', [])
    
    def build_system_prompt(self) -> str:
        """Constructs the system prompt for the LLM"""
        examples = "\n".join([f"- {ex}" for ex in self.example_responses])
        directives = "\n".join([f"- {d}" for d in self.directives])
        
        prompt = f"""You are {self.name}, a conversational AI companion.

PERSONALITY:
{self.personality['description']}

TONE: {self.personality['tone']}
RESPONSE STYLE: {self.personality['response_style']}

DIRECTIVES:
{directives}

EXAMPLE RESPONSES:
{examples}

Remember: You are {self.name}. Stay in character. Keep it short and conversational."""
        
        return prompt
    
    def is_triggered(self, text: str) -> bool:
        """Check if the trigger name appears in the text"""
        return self.trigger_name in text.lower()
    
    def should_comment(self, text: str, commentary_mode: bool = False) -> bool:
        """Determine if the AI should respond (trigger mode or commentary mode)"""
        if commentary_mode:
            # In commentary mode, respond randomly or based on content
            # For now, always respond in commentary mode
            return True
        else:
            # Only respond if trigger name is detected
            return self.is_triggered(text)


class PersonaManager:
    """Manages multiple personas and switching between them"""
    
    def __init__(self, personas_dir: str = "config/personas"):
        self.personas: Dict[str, Persona] = {}
        self.personas_dir = Path(personas_dir)
        self.load_personas()
        self.active_persona: Optional[Persona] = None
    
    def load_personas(self):
        """Load all persona JSON files from the personas directory"""
        if not self.personas_dir.exists():
            raise FileNotFoundError(f"Personas directory not found: {self.personas_dir}")
        
        for json_file in self.personas_dir.glob("*.json"):
            try:
                persona = Persona(str(json_file))
                self.personas[persona.trigger_name] = persona
                print(f"✓ Loaded persona: {persona.name} (trigger: '{persona.trigger_name}')")
            except Exception as e:
                print(f"✗ Failed to load {json_file.name}: {e}")
    
    def set_active_persona(self, trigger_name: str) -> bool:
        """Set the active persona by trigger name"""
        trigger_name = trigger_name.lower()
        if trigger_name in self.personas:
            self.active_persona = self.personas[trigger_name]
            print(f"Active persona: {self.active_persona.name}")
            return True
        return False
    
    def get_persona_by_trigger(self, text: str) -> Optional[Persona]:
        """Find which persona (if any) is triggered by the text"""
        for persona in self.personas.values():
            if persona.is_triggered(text):
                return persona
        return None
    
    def list_personas(self) -> list:
        """Return list of available personas"""
        return [(p.name, p.trigger_name) for p in self.personas.values()]
