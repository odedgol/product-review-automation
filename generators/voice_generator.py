"""
Voice Generator Module
Uses ElevenLabs API to generate voice-over audio
"""

import os
from pathlib import Path
from typing import Optional

# Try to import elevenlabs
try:
    from elevenlabs import ElevenLabs, VoiceSettings
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False
    print("Warning: elevenlabs not installed. Run: pip install elevenlabs")

# Try to import settings
try:
    from config.settings import ELEVENLABS_API_KEY, VOICE_CONFIG, OUTPUT_DIR
except ImportError:
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
    VOICE_CONFIG = {
        "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel
        "model_id": "eleven_multilingual_v2",
        "stability": 0.5,
        "similarity_boost": 0.8,
        "style": 0.4,
        "use_speaker_boost": True,
    }
    OUTPUT_DIR = Path("./output")


class VoiceGenerator:
    """Generate voice-over audio using ElevenLabs API"""
    
    # Available Hebrew-friendly voices
    RECOMMENDED_VOICES = {
        "rachel": "21m00Tcm4TlvDq8ikWAM",  # Calm, professional female
        "josh": "TxGEqnHWrfWFTfGW9XjX",    # Deep, authoritative male
        "bella": "EXAVITQu4vr4xnSDxMaL",   # Friendly female
        "adam": "pNInz6obpgDQGcFmaJgB",    # Natural male
    }
    
    def __init__(self, api_key: Optional[str] = None):
        if not ELEVENLABS_AVAILABLE:
            raise ImportError("elevenlabs package not installed")
        
        self.api_key = api_key or ELEVENLABS_API_KEY
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY is required")
        
        self.client = ElevenLabs(api_key=self.api_key)
        self.output_dir = Path(OUTPUT_DIR)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_voice(
        self,
        text: str,
        output_filename: str = "voiceover.mp3",
        voice_id: Optional[str] = None,
        model_id: str = "eleven_multilingual_v2",
        stability: float = 0.5,
        similarity_boost: float = 0.8,
        style: float = 0.4,
    ) -> Path:
        """
        Generate voice-over audio from text
        
        Args:
            text: The text to convert to speech
            output_filename: Name of the output file
            voice_id: ElevenLabs voice ID
            model_id: Model to use (eleven_multilingual_v2 for Hebrew)
            stability: Voice stability (0-1)
            similarity_boost: Voice similarity (0-1)
            style: Style exaggeration (0-1)
        
        Returns:
            Path to the generated audio file
        """
        voice_id = voice_id or VOICE_CONFIG.get("voice_id", self.RECOMMENDED_VOICES["rachel"])
        
        output_path = self.output_dir / output_filename
        
        # Generate audio
        audio = self.client.text_to_speech.convert(
            voice_id=voice_id,
            output_format="mp3_44100_128",
            text=text,
            model_id=model_id,
            voice_settings=VoiceSettings(
                stability=stability,
                similarity_boost=similarity_boost,
                style=style,
                use_speaker_boost=True,
            )
        )
        
        # Save to file
        with open(output_path, "wb") as f:
            for chunk in audio:
                f.write(chunk)
        
        return output_path
    
    def generate_from_script(
        self,
        script_sections: dict,
        output_dir: Optional[Path] = None,
        voice_id: Optional[str] = None,
    ) -> dict:
        """
        Generate voice-over for each section of a script
        
        Args:
            script_sections: Dict of section_name: text
            output_dir: Directory to save audio files
            voice_id: ElevenLabs voice ID
        
        Returns:
            Dict mapping section names to audio file paths
        """
        output_dir = Path(output_dir) if output_dir else self.output_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        
        audio_files = {}
        
        for section, text in script_sections.items():
            if not text.strip():
                continue
            
            filename = f"voice_{section}.mp3"
            print(f"Generating voice for section: {section}")
            
            audio_path = self.generate_voice(
                text=text,
                output_filename=filename,
                voice_id=voice_id,
            )
            audio_files[section] = audio_path
        
        return audio_files
    
    def list_voices(self) -> list:
        """List available voices"""
        response = self.client.voices.get_all()
        return [
            {
                "voice_id": voice.voice_id,
                "name": voice.name,
                "category": voice.category,
            }
            for voice in response.voices
        ]
    
    def get_character_count(self, text: str) -> int:
        """Get character count for billing purposes"""
        return len(text)
    
    def estimate_cost(self, text: str, price_per_1k_chars: float = 0.30) -> float:
        """Estimate cost for text-to-speech conversion"""
        chars = self.get_character_count(text)
        return (chars / 1000) * price_per_1k_chars


# =============================================================================
# Mock Voice Generator for testing without API key
# =============================================================================

class MockVoiceGenerator:
    """Mock voice generator for testing without API key"""
    
    def __init__(self):
        self.output_dir = Path("./output")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_voice(self, text: str, output_filename: str = "voiceover.mp3", **kwargs) -> Path:
        """Create a placeholder file"""
        output_path = self.output_dir / output_filename
        
        # Create empty file as placeholder
        output_path.write_text(f"[PLACEHOLDER - Would contain audio for:]\n{text[:200]}...")
        
        print(f"Mock: Would generate audio for {len(text)} characters")
        print(f"Mock: Saved placeholder to {output_path}")
        
        return output_path
    
    def estimate_cost(self, text: str, price_per_1k_chars: float = 0.30) -> float:
        """Estimate cost"""
        chars = len(text)
        cost = (chars / 1000) * price_per_1k_chars
        print(f"Estimated cost: ${cost:.2f} ({chars} characters)")
        return cost


def get_voice_generator(api_key: Optional[str] = None) -> VoiceGenerator:
    """Factory function to get appropriate voice generator"""
    api_key = api_key or os.getenv("ELEVENLABS_API_KEY", "")
    
    if api_key and ELEVENLABS_AVAILABLE:
        return VoiceGenerator(api_key)
    else:
        print("Using MockVoiceGenerator (no API key or elevenlabs not installed)")
        return MockVoiceGenerator()


if __name__ == "__main__":
    # Test the module
    from generators.script_generator import get_example_script
    
    script = get_example_script()
    
    # Use mock generator for testing
    voice_gen = MockVoiceGenerator()
    
    # Estimate cost for full script
    full_text = script["full_script"]
    cost = voice_gen.estimate_cost(full_text)
    
    print(f"\nScript word count: {script['word_count']}")
    print(f"Character count: {len(full_text)}")
    print(f"Estimated ElevenLabs cost: ${cost:.2f}")
