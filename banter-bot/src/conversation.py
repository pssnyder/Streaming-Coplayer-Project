"""
Conversation Manager for Banter Bot
Handles conversation state, context tracking, and response flow
"""

import time
from typing import List, Dict, Optional
from datetime import datetime, timedelta


class ConversationManager:
    """Manages conversation state and context window"""
    
    def __init__(self, max_exchanges: int = 10, timeout_seconds: int = 300):
        self.max_exchanges = max_exchanges
        self.timeout_seconds = timeout_seconds
        
        self.conversation_history: List[Dict[str, str]] = []
        self.in_conversation = False
        self.last_interaction_time: Optional[datetime] = None
        self.current_topic: Optional[str] = None
    
    def add_exchange(self, user_input: str, ai_response: str):
        """Add a user-AI exchange to the conversation history"""
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'user': user_input,
            'ai': ai_response
        })
        
        # Trim history to max exchanges
        if len(self.conversation_history) > self.max_exchanges:
            self.conversation_history = self.conversation_history[-self.max_exchanges:]
        
        self.last_interaction_time = datetime.now()
        self.in_conversation = True
    
    def is_conversation_active(self) -> bool:
        """Check if we're still in an active conversation (based on timeout)"""
        if not self.last_interaction_time:
            return False
        
        time_elapsed = datetime.now() - self.last_interaction_time
        return time_elapsed.total_seconds() < self.timeout_seconds
    
    def start_conversation(self):
        """Explicitly start a conversation (when trigger name is detected)"""
        self.in_conversation = True
        self.last_interaction_time = datetime.now()
    
    def end_conversation(self):
        """End the conversation and clear context"""
        self.in_conversation = False
        self.conversation_history.clear()
        self.last_interaction_time = None
        self.current_topic = None
    
    def get_context_for_llm(self) -> str:
        """Format conversation history for LLM context"""
        if not self.conversation_history:
            return ""
        
        context_lines = ["RECENT CONVERSATION:"]
        for exchange in self.conversation_history[-5:]:  # Last 5 exchanges
            context_lines.append(f"User: {exchange['user']}")
            context_lines.append(f"You: {exchange['ai']}")
        
        return "\n".join(context_lines)
    
    def needs_trigger(self) -> bool:
        """Determine if trigger name is required for next response"""
        if not self.is_conversation_active():
            # Conversation timed out - need trigger again
            return True
        
        if not self.in_conversation:
            # Not in conversation mode - need trigger
            return True
        
        # In active conversation - no trigger needed
        return False
    
    def get_time_since_last_interaction(self) -> Optional[float]:
        """Get seconds since last interaction"""
        if not self.last_interaction_time:
            return None
        return (datetime.now() - self.last_interaction_time).total_seconds()
