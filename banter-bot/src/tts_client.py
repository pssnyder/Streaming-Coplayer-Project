"""
Text-to-Speech Client for Banter Bot
Handles voice synthesis using Google Cloud TTS
"""

import os
from google.cloud import texttospeech
from typing import Optional
import io


class TTSClient:
    """Wrapper for Google Cloud Text-to-Speech"""
    
    def __init__(self):
        # Google Cloud credentials should be set via GOOGLE_APPLICATION_CREDENTIALS env var
        self.client = texttospeech.TextToSpeechClient()
        
        # Voice configuration
        self.voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Neural2-J",  # Male voice, casual tone
            # Options: Neural2-A (female), Neural2-C (female), Neural2-D (male), Neural2-J (male)
        )
        
        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=1.0,  # Normal speed
            pitch=0.0,          # Normal pitch
        )
    
    def synthesize(self, text: str, output_file: Optional[str] = None) -> bytes:
        """
        Convert text to speech
        
        Args:
            text: The text to synthesize
            output_file: Optional path to save audio file
        
        Returns:
            Audio data as bytes
        """
        synthesis_input = texttospeech.SynthesisInput(text=text)
        
        try:
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=self.voice,
                audio_config=self.audio_config
            )
            
            # Optionally save to file
            if output_file:
                with open(output_file, 'wb') as out:
                    out.write(response.audio_content)
            
            return response.audio_content
            
        except Exception as e:
            print(f"Error synthesizing speech: {e}")
            return b""
    
    def play_audio(self, audio_data: bytes):
        """
        Play audio data through default output device
        Uses pydub and simpleaudio for playback
        """
        try:
            from pydub import AudioSegment
            from pydub.playback import play
            
            # Convert bytes to AudioSegment
            audio = AudioSegment.from_mp3(io.BytesIO(audio_data))
            play(audio)
            
        except Exception as e:
            print(f"Error playing audio: {e}")
    
    def set_voice(self, voice_name: str):
        """Change the TTS voice"""
        self.voice.name = voice_name
    
    def test_tts(self) -> bool:
        """Test if TTS is working"""
        try:
            test_audio = self.synthesize("Testing one two three")
            return len(test_audio) > 0
        except Exception as e:
            print(f"TTS test failed: {e}")
            return False
