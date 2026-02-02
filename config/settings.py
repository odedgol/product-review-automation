# Configuration file for Product Review Automation
# Copy this file to .env and fill in your API keys

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# =============================================================================
# API KEYS - Fill these in your .env file
# =============================================================================
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")  # Optional, for backup

# =============================================================================
# PATHS
# =============================================================================
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"
VIDEOS_DIR = OUTPUT_DIR / "videos"
ASSETS_DIR = BASE_DIR / "assets"
TEMPLATES_DIR = BASE_DIR / "templates"

# Create directories if they don't exist
for dir_path in [OUTPUT_DIR, VIDEOS_DIR, ASSETS_DIR, TEMPLATES_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# =============================================================================
# VIDEO SETTINGS
# =============================================================================
VIDEO_CONFIG = {
    "width": 1920,
    "height": 1080,
    "fps": 30,
    "format": "mp4",
    "codec": "libx264",
    "audio_codec": "aac",
}

# =============================================================================
# ELEVENLABS VOICE SETTINGS
# =============================================================================
VOICE_CONFIG = {
    "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel - default voice
    "model_id": "eleven_multilingual_v2",  # Supports Hebrew
    "stability": 0.5,
    "similarity_boost": 0.8,
    "style": 0.4,
    "use_speaker_boost": True,
}

# Hebrew voices available:
# - You can clone your own voice
# - Or use multilingual model with any voice

# =============================================================================
# SCRIPT GENERATION SETTINGS
# =============================================================================
SCRIPT_CONFIG = {
    "language": "hebrew",  # or "english"
    "style": "friendly",   # friendly, professional, casual
    "max_duration_seconds": 180,  # 3 minutes
    "target_words": 450,   # ~150 words per minute
}

# =============================================================================
# VIDEO TEMPLATE SETTINGS
# =============================================================================
TEMPLATE_CONFIG = {
    "intro_duration": 5,
    "outro_duration": 5,
    "transition_duration": 0.5,
    "background_music_volume": 0.1,
    "font_family": "Arial",
    "primary_color": "#FF6B35",
    "secondary_color": "#004E89",
    "text_color": "#FFFFFF",
}

# =============================================================================
# PRODUCT DATA STRUCTURE
# =============================================================================
PRODUCT_TEMPLATE = {
    "name": "",
    "brand": "",
    "price": 0.0,
    "currency": "USD",
    "rating": 0.0,
    "review_count": 0,
    "asin": "",
    "url": "",
    "images": [],
    "features": [],
    "pros": [],
    "cons": [],
    "description": "",
    "specs": {},
}
