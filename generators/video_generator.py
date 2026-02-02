"""
Video Generator Module - Simplified Version
Creates storyboards and videos for product reviews
"""

import os
from pathlib import Path
from typing import List, Dict, Optional

# Try to import settings
try:
    from config.settings import OUTPUT_DIR
except ImportError:
    OUTPUT_DIR = Path("./output")


class SimpleVideoGenerator:
    """Creates markdown storyboards for video production"""
    
    def __init__(self):
        self.output_dir = Path(OUTPUT_DIR) if isinstance(OUTPUT_DIR, str) else OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_storyboard(
        self,
        product_name: str,
        product_images: List[str],
        script_sections: Dict[str, str],
        pros: List[str],
        cons: List[str],
        score: float,
        output_filename: str = "storyboard.md",
    ) -> Path:
        """Generate a markdown storyboard for the video"""
        
        images_list = "\n".join(f"  {i+1}. {img}" for i, img in enumerate(product_images[:5])) if product_images else "  [Add product images]"
        pros_list = "\n".join(f"  ✓ {pro}" for pro in pros[:5])
        cons_list = "\n".join(f"  ✗ {con}" for con in cons[:5])
        
        storyboard = f"""# Video Storyboard: {product_name}

## Technical Specs
- Resolution: 1920x1080
- FPS: 30
- Duration: ~3 minutes

---

## Scene 1: Title (0:00-0:05)
Text: "{product_name}"

## Scene 2: Hook (0:05-0:15)
{script_sections.get('hook', '[Hook]')}

## Scene 3: Showcase (0:15-0:30)
Images:
{images_list}

Script:
{script_sections.get('intro', '[Intro]')}

## Scene 4: Features (0:30-1:15)
{script_sections.get('features', '[Features]')}

## Scene 5: Pros (1:15-1:45)
{pros_list}

{script_sections.get('pros', '[Pros script]')}

## Scene 6: Cons (1:45-2:10)
{cons_list}

{script_sections.get('cons', '[Cons script]')}

## Scene 7: Verdict (2:10-2:40)
Score: {score}/10

{script_sections.get('verdict', '[Verdict]')}

## Scene 8: CTA (2:40-3:00)
{script_sections.get('cta', '[CTA]')}

---
## Assets Needed
- Product images
- Voice-over MP3
- Background music
"""
        
        output_path = self.output_dir / output_filename
        output_path.write_text(storyboard, encoding="utf-8")
        return output_path


def get_video_generator():
    """Get video generator instance"""
    return SimpleVideoGenerator()
