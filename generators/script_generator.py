"""
Script Generator Module
Uses Claude API to generate video scripts in Hebrew or English
"""

import os
from typing import Optional
from anthropic import Anthropic

# Try to import settings, handle if not available
try:
    from config.settings import ANTHROPIC_API_KEY, SCRIPT_CONFIG
except ImportError:
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    SCRIPT_CONFIG = {
        "language": "hebrew",
        "style": "friendly",
        "max_duration_seconds": 180,
        "target_words": 450,
    }


class ScriptGenerator:
    """Generate video scripts using Claude API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or ANTHROPIC_API_KEY
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY is required")
        
        self.client = Anthropic(api_key=self.api_key)
    
    def generate_script(
        self,
        product_info: str,
        language: str = "hebrew",
        style: str = "friendly",
        duration_seconds: int = 180
    ) -> dict:
        """
        Generate a video script for product review
        
        Args:
            product_info: Formatted product information
            language: "hebrew" or "english"
            style: "friendly", "professional", or "casual"
            duration_seconds: Target video duration
        
        Returns:
            dict with script sections and metadata
        """
        
        words_per_minute = 150 if language == "english" else 120  # Hebrew is slower
        target_words = int((duration_seconds / 60) * words_per_minute)
        
        system_prompt = self._get_system_prompt(language, style)
        user_prompt = self._get_user_prompt(product_info, target_words, language)
        
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )
        
        script_text = response.content[0].text
        
        return {
            "full_script": script_text,
            "sections": self._parse_script_sections(script_text),
            "language": language,
            "estimated_duration": duration_seconds,
            "word_count": len(script_text.split()),
        }
    
    def _get_system_prompt(self, language: str, style: str) -> str:
        """Get system prompt based on language and style"""
        
        style_instructions = {
            "friendly": "חם, ידידותי, כאילו מדבר עם חבר טוב",
            "professional": "מקצועי ואמין, אבל לא יבש",
            "casual": "קליל ומשעשע, עם הומור קל",
        }
        
        if language == "hebrew":
            return f"""אתה כותב תסריטים לסרטוני סקירת מוצרים ביוטיוב.

הסגנון שלך: {style_instructions.get(style, style_instructions['friendly'])}

כללים חשובים:
1. תמיד פתח ב-HOOK חזק שתופס תוך 3 שניות
2. היה כנה - אם יש חסרונות, תזכיר אותם
3. אל תהיה "מכירתי" מדי - אנשים מריחים את זה
4. השתמש בשפה יומיומית, לא פורמלית
5. כלול ציטוטים מביקורות אמיתיות
6. סיים עם המלצה ברורה וקריאה לפעולה

מבנה התסריט:
[HOOK] - 5-10 שניות - משפט פתיחה שתופס
[INTRO] - 10-15 שניות - היכרות והצגת המוצר
[FEATURES] - 30-45 שניות - תכונות עיקריות
[PROS] - 30-45 שניות - יתרונות עם דוגמאות
[CONS] - 20-30 שניות - חסרונות בכנות
[VERDICT] - 15-20 שניות - סיכום והמלצה
[CTA] - 10 שניות - קריאה לפעולה

סמן כל חלק ב-[שם החלק] בתחילתו."""

        else:  # English
            return f"""You write scripts for YouTube product review videos.

Your style: Warm and engaging, like talking to a good friend.

Important rules:
1. Always start with a strong HOOK that grabs attention in 3 seconds
2. Be honest - mention drawbacks if they exist
3. Don't be too "salesy" - people can tell
4. Use everyday language, not formal
5. Include real review quotes when relevant
6. End with a clear recommendation and call to action

Script structure:
[HOOK] - 5-10 seconds - Attention-grabbing opening
[INTRO] - 10-15 seconds - Introduction and product overview
[FEATURES] - 30-45 seconds - Key features
[PROS] - 30-45 seconds - Advantages with examples
[CONS] - 20-30 seconds - Honest drawbacks
[VERDICT] - 15-20 seconds - Summary and recommendation
[CTA] - 10 seconds - Call to action

Mark each section with [SECTION NAME] at the start."""
    
    def _get_user_prompt(self, product_info: str, target_words: int, language: str) -> str:
        """Get user prompt with product info"""
        
        if language == "hebrew":
            return f"""כתוב תסריט לסרטון סקירת מוצר ביוטיוב.
            
אורך מטרה: כ-{target_words} מילים (3 דקות)

מידע על המוצר:
{product_info}

דגשים:
- התחל עם הוק שמעורר סקרנות
- הדגש את הפיצ'ר הכי ייחודי (FreeSip)
- התייחס לויראליות בטיקטוק
- השווה למתחרים (Stanley, Hydro Flask)
- תן ציון מ-1 עד 10 בסוף
- סיים עם "לינק בתיאור" ובקשה ללייק ומנוי

כתוב את התסריט המלא:"""

        else:
            return f"""Write a script for a YouTube product review video.

Target length: ~{target_words} words (3 minutes)

Product information:
{product_info}

Key points:
- Start with a curiosity-provoking hook
- Highlight the most unique feature (FreeSip)
- Reference TikTok virality
- Compare to competitors (Stanley, Hydro Flask)
- Give a score from 1 to 10 at the end
- End with "link in description" and like/subscribe request

Write the full script:"""
    
    def _parse_script_sections(self, script_text: str) -> dict:
        """Parse script into sections"""
        
        sections = {}
        current_section = "intro"
        current_text = []
        
        section_markers = ["HOOK", "INTRO", "FEATURES", "PROS", "CONS", "VERDICT", "CTA"]
        
        for line in script_text.split('\n'):
            # Check if line starts a new section
            found_section = False
            for marker in section_markers:
                if f"[{marker}]" in line.upper():
                    # Save previous section
                    if current_text:
                        sections[current_section] = '\n'.join(current_text).strip()
                    current_section = marker.lower()
                    current_text = []
                    # Add the rest of the line after the marker
                    remaining = line.split(']', 1)[-1].strip()
                    if remaining:
                        current_text.append(remaining)
                    found_section = True
                    break
            
            if not found_section and line.strip():
                current_text.append(line)
        
        # Save last section
        if current_text:
            sections[current_section] = '\n'.join(current_text).strip()
        
        return sections


# =============================================================================
# Pre-generated script example (for use without API key)
# =============================================================================

EXAMPLE_SCRIPT_HEBREW = """
[HOOK]
בקבוק מים ב-28 דולר שמכר יותר מכל Stanley ו-Hydro Flask ביחד? בואו נבדוק אם זה באמת שווה את ההייפ.

[INTRO]
היי, מה קורה? היום אנחנו בודקים את Owala FreeSip - הבקבוק שכבש את טיקטוק עם 272 מיליון צפיות. אני אגלה לכם בדיוק למה כולם משתגעים עליו, ומה הדברים שאף אחד לא מספר לכם.

[FEATURES]
אז מה מיוחד פה? הפיצ'ר המטורף הוא ה-FreeSip - פתח כפול שמאפשר לשתות גם מקש וגם לגמוע ישירות. בלי להחליף מכסים, בלי להתעסק. פשוט לוחצים על הכפתור ושותים.

יש פה בידוד דו-שכבתי שאמור לשמור על הקור 24 שעות. בדקתי את זה - שמתי קרח בלילה, ובבוקר אחרי הוא עדיין היה שם. מרשים.

המכסה נועל פעמיים - פעם עם הכפתור ופעם עם הידית. אפשר לזרוק לתיק בלי דאגה.

[PROS]
בואו נדבר על היתרונות:
ראשית, העיצוב פשוט מדהים. יש פה צבעים שאף מותג אחר לא מעז לעשות - "Smooshed Blueberry", "Shy Marshmallow" - השמות לבד שווים את הכסף.

שנית, הקש המוסתר. בניגוד ל-Stanley שהקש שלו חשוף לכל החיידקים בעולם, פה הוא מוגן בתוך המכסה.

ומשתמשים כותבים: "הפלתי אותו לנהר, הוא שרד" ו"הדבר הכי טוב שקניתי השנה".

[CONS]
עכשיו בואו נהיה כנים. יש פה כמה דברים שצריך לדעת:
אחד - זה לא למשקאות חמים. הקש לא מתאים לזה.
שניים - הגרסאות הגדולות לא נכנסות למתקן כוסות ברכב. ה-24 אונקיות בקושי נכנס.
שלוש - צריך לנקות לפחות פעם בשבוע. יש חלקי סיליקון שיכולים לתפוס עובש אם מזניחים.

[VERDICT]
אז האם זה שווה את הכסף? 
בהחלט כן. במחיר של 28 דולר, אתם מקבלים בקבוק עם פיצ'רים של בקבוקים ב-50 דולר. האיכות מעולה, העיצוב מדהים, והשימושיות פשוט הכי נוחה שניסיתי.

הציון שלי: 8.5 מתוך 10. נקודה וחצי הורדתי על הגודל שלא תמיד מתאים ועל הניקיון התדיר.

[CTA]
אם אתם רוצים לרכוש - יש לינק בתיאור עם המחיר הכי טוב שמצאתי.
אהבתם? תנו לייק ותירשמו לערוץ. יש לי עוד המון סקירות כאלה בדרך.
נתראה בסרטון הבא!
"""


def get_example_script() -> dict:
    """Return pre-generated example script"""
    generator = ScriptGenerator.__new__(ScriptGenerator)
    sections = generator._parse_script_sections(EXAMPLE_SCRIPT_HEBREW)
    
    return {
        "full_script": EXAMPLE_SCRIPT_HEBREW,
        "sections": sections,
        "language": "hebrew",
        "estimated_duration": 180,
        "word_count": len(EXAMPLE_SCRIPT_HEBREW.split()),
    }


if __name__ == "__main__":
    # Test with example script (no API key needed)
    print("=== Example Script ===\n")
    script = get_example_script()
    print(script["full_script"])
    print("\n=== Sections ===")
    for section, text in script["sections"].items():
        print(f"\n[{section.upper()}]")
        print(text[:100] + "..." if len(text) > 100 else text)
