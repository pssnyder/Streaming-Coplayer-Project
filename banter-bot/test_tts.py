"""
Test TTS (Text-to-Speech) functionality
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent / "src"))

from tts_client import TTSClient

def test_tts():
    print("Testing Google Cloud Text-to-Speech...")
    load_dotenv()
    
    try:
        tts = TTSClient()
        print("✓ TTS Client initialized")
        
        # Test synthesis
        print("\nSynthesizing test phrase...")
        audio = tts.synthesize("Hey there, this is Gary. Testing one, two, three.")
        
        if len(audio) > 0:
            print(f"✓ Audio generated ({len(audio)} bytes)")
            
            # Try to play it
            print("\n🔊 Playing audio...")
            tts.play_audio(audio)
            print("✓ Audio playback complete!")
            return True
        else:
            print("✗ No audio data generated")
            return False
            
    except Exception as e:
        print(f"✗ TTS test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_tts()
