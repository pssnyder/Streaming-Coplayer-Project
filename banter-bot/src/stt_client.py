"""
Speech-to-Text Client for Banter Bot
Handles voice input using Google Cloud STT
"""

import os
from google.cloud import speech
import pyaudio
import queue
import threading
from typing import Optional, Callable


class STTClient:
    """Wrapper for Google Cloud Speech-to-Text with microphone input"""
    
    # Audio recording parameters
    RATE = 16000
    CHUNK = int(RATE / 10)  # 100ms chunks
    
    def __init__(self):
        self.client = speech.SpeechClient()
        
        self.config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=self.RATE,
            language_code="en-US",
            enable_automatic_punctuation=True,
        )
        
        self.streaming_config = speech.StreamingRecognitionConfig(
            config=self.config,
            interim_results=True  # Get partial results while speaking
        )
        
        self._audio_queue = queue.Queue()
        self._is_recording = False
    
    def _audio_generator(self):
        """Generator that yields audio chunks from the microphone"""
        while self._is_recording:
            chunk = self._audio_queue.get()
            if chunk is None:
                return
            yield chunk
    
    def _record_audio(self, audio_interface: pyaudio.PyAudio, stream):
        """Background thread to record audio"""
        while self._is_recording:
            try:
                data = stream.read(self.CHUNK, exception_on_overflow=False)
                self._audio_queue.put(data)
            except Exception as e:
                print(f"Audio recording error: {e}")
                break
    
    def listen_continuous(self, on_transcript: Callable[[str, bool], None]):
        """
        Continuously listen to microphone and call callback with transcripts
        
        Args:
            on_transcript: Callback function(transcript: str, is_final: bool)
        """
        audio_interface = pyaudio.PyAudio()
        
        try:
            stream = audio_interface.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK,
            )
            
            print("🎤 Listening... (Press Ctrl+C to stop)")
            self._is_recording = True
            
            # Start recording thread
            record_thread = threading.Thread(
                target=self._record_audio,
                args=(audio_interface, stream)
            )
            record_thread.start()
            
            # Create streaming request
            requests = (
                speech.StreamingRecognizeRequest(audio_content=content)
                for content in self._audio_generator()
            )
            
            responses = self.client.streaming_recognize(
                self.streaming_config,
                requests
            )
            
            # Process responses
            for response in responses:
                if not response.results:
                    continue
                
                result = response.results[0]
                if not result.alternatives:
                    continue
                
                transcript = result.alternatives[0].transcript
                is_final = result.is_final
                
                # Call the callback with the transcript
                on_transcript(transcript, is_final)
                
        except KeyboardInterrupt:
            print("\n🛑 Stopping...")
        finally:
            self._is_recording = False
            self._audio_queue.put(None)
            stream.stop_stream()
            stream.close()
            audio_interface.terminate()
    
    def record_once(self, duration_seconds: int = 5) -> str:
        """
        Record audio for a fixed duration and return transcript
        
        Args:
            duration_seconds: How long to record
        
        Returns:
            Transcribed text
        """
        audio_interface = pyaudio.PyAudio()
        
        try:
            stream = audio_interface.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK,
            )
            
            print(f"🎤 Recording for {duration_seconds} seconds...")
            
            frames = []
            for i in range(0, int(self.RATE / self.CHUNK * duration_seconds)):
                data = stream.read(self.CHUNK, exception_on_overflow=False)
                frames.append(data)
            
            print("⏸️  Recording complete. Transcribing...")
            
            audio_data = b''.join(frames)
            
            # Transcribe
            audio = speech.RecognitionAudio(content=audio_data)
            response = self.client.recognize(config=self.config, audio=audio)
            
            if response.results:
                transcript = response.results[0].alternatives[0].transcript
                return transcript
            else:
                return ""
                
        finally:
            stream.stop_stream()
            stream.close()
            audio_interface.terminate()
    
    def test_microphone(self) -> bool:
        """Test if microphone is accessible"""
        try:
            audio = pyaudio.PyAudio()
            stream = audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK,
            )
            data = stream.read(self.CHUNK)
            stream.close()
            audio.terminate()
            return len(data) > 0
        except Exception as e:
            print(f"Microphone test failed: {e}")
            return False
