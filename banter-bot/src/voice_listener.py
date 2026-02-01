"""
Voice Activity Detection and Continuous Listening
Detects when user is speaking and triggers transcription
"""

import pyaudio
import numpy as np
import queue
import threading
from google.cloud import speech
from typing import Callable, Optional


class VoiceListener:
    """Continuous microphone monitoring with voice activity detection"""
    
    # Audio settings
    RATE = 16000
    CHUNK = int(RATE / 10)  # 100ms chunks
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    
    # Voice activity detection thresholds
    ENERGY_THRESHOLD = 500  # RMS energy threshold for voice detection
    SILENCE_DURATION = 1.5  # Seconds of silence before considering speech complete
    MIN_SPEECH_DURATION = 0.3  # Minimum duration to consider as speech
    
    def __init__(self, on_speech_detected: Callable[[str], None]):
        """
        Initialize voice listener
        
        Args:
            on_speech_detected: Callback function(transcript: str) called when speech is detected
        """
        self.on_speech_detected = on_speech_detected
        self.is_listening = False
        self.audio_queue = queue.Queue()
        self.speech_client = speech.SpeechClient()
        
        self.config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=self.RATE,
            language_code="en-US",
            enable_automatic_punctuation=True,
        )
    
    def calculate_rms(self, audio_data: bytes) -> float:
        """Calculate RMS (root mean square) energy of audio"""
        audio_array = np.frombuffer(audio_data, dtype=np.int16)
        return np.sqrt(np.mean(audio_array**2))
    
    def start(self):
        """Start continuous listening"""
        self.is_listening = True
        
        # Start audio capture thread
        audio_thread = threading.Thread(target=self._audio_capture_loop, daemon=True)
        audio_thread.start()
        
        # Start processing thread
        process_thread = threading.Thread(target=self._process_audio_loop, daemon=True)
        process_thread.start()
        
        print("🎤 Voice listener started - speak naturally!")
    
    def stop(self):
        """Stop listening"""
        self.is_listening = False
    
    def _audio_capture_loop(self):
        """Continuously capture audio from microphone"""
        audio = pyaudio.PyAudio()
        
        try:
            stream = audio.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK,
            )
            
            while self.is_listening:
                try:
                    data = stream.read(self.CHUNK, exception_on_overflow=False)
                    self.audio_queue.put(data)
                except Exception as e:
                    print(f"Audio capture error: {e}")
                    break
        
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()
    
    def _process_audio_loop(self):
        """Process audio chunks and detect speech"""
        speech_buffer = []
        silence_chunks = 0
        is_speaking = False
        
        while self.is_listening:
            try:
                # Get audio chunk
                audio_chunk = self.audio_queue.get(timeout=0.1)
                
                # Calculate energy
                energy = self.calculate_rms(audio_chunk)
                
                # Voice activity detection
                if energy > self.ENERGY_THRESHOLD:
                    # Voice detected
                    speech_buffer.append(audio_chunk)
                    silence_chunks = 0
                    
                    if not is_speaking:
                        is_speaking = True
                        # print("🗣️ Speech detected...")
                
                elif is_speaking:
                    # In speech, but current chunk is silent
                    speech_buffer.append(audio_chunk)
                    silence_chunks += 1
                    
                    # Check if silence duration exceeded
                    silence_duration = silence_chunks * (self.CHUNK / self.RATE)
                    
                    if silence_duration >= self.SILENCE_DURATION:
                        # Speech complete - process it
                        speech_duration = len(speech_buffer) * (self.CHUNK / self.RATE)
                        
                        if speech_duration >= self.MIN_SPEECH_DURATION:
                            # Transcribe the speech
                            self._transcribe_speech(speech_buffer)
                        
                        # Reset
                        speech_buffer = []
                        silence_chunks = 0
                        is_speaking = False
            
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Processing error: {e}")
    
    def _transcribe_speech(self, audio_chunks: list):
        """Transcribe captured speech"""
        try:
            # Combine audio chunks
            audio_data = b''.join(audio_chunks)
            
            # Create recognition audio
            audio = speech.RecognitionAudio(content=audio_data)
            
            # Transcribe
            response = self.speech_client.recognize(config=self.config, audio=audio)
            
            if response.results:
                transcript = response.results[0].alternatives[0].transcript
                # print(f"📝 Transcribed: {transcript}")
                
                # Call the callback
                self.on_speech_detected(transcript)
        
        except Exception as e:
            print(f"Transcription error: {e}")


class SimpleVoiceListener:
    """Simpler voice listener using keyboard trigger (fallback option)"""
    
    def __init__(self, on_speech_detected: Callable[[str], None]):
        self.on_speech_detected = on_speech_detected
        self.is_listening = False
        self.speech_client = speech.SpeechClient()
        
        self.RATE = 16000
        self.CHUNK = int(self.RATE / 10)
        
        self.config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=self.RATE,
            language_code="en-US",
            enable_automatic_punctuation=True,
        )
    
    def record_and_transcribe(self, duration: int = 3):
        """Record for a fixed duration and transcribe"""
        audio = pyaudio.PyAudio()
        
        try:
            stream = audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK,
            )
            
            print(f"🎤 Recording for {duration} seconds...")
            frames = []
            
            for i in range(0, int(self.RATE / self.CHUNK * duration)):
                data = stream.read(self.CHUNK, exception_on_overflow=False)
                frames.append(data)
            
            print("⏸️  Processing...")
            
            audio_data = b''.join(frames)
            audio_obj = speech.RecognitionAudio(content=audio_data)
            
            response = self.speech_client.recognize(config=self.config, audio=audio_obj)
            
            if response.results:
                transcript = response.results[0].alternatives[0].transcript
                self.on_speech_detected(transcript)
            else:
                print("No speech detected")
        
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()
