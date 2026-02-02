# 🎬 Product Review Video Automation

מערכת אוטומטית ליצירת סרטוני סקירת מוצרים ליוטיוב.

## ✨ יכולות

- 📝 יצירת תסריטים אוטומטית באמצעות Claude AI
- 🎙️ הקלטת קול אוטומטית באמצעות ElevenLabs
- 🎥 יצירת וידאו אוטומטית באמצעות MoviePy
- 🌐 תמיכה בעברית ואנגלית

## 🚀 התקנה מהירה

```bash
# Clone או הורדת הפרויקט
cd product-review-automation

# יצירת סביבה וירטואלית
python -m venv venv
source venv/bin/activate  # Linux/Mac
# או: venv\Scripts\activate  # Windows

# התקנת תלויות
pip install -r requirements.txt

# העתקת קובץ הגדרות
cp .env.example .env
# ערוך את .env והוסף את ה-API keys שלך
```

## 🔑 API Keys נדרשים

| שירות | שימוש | איפה להשיג |
|--------|-------|------------|
| Anthropic | יצירת תסריטים | https://console.anthropic.com |
| ElevenLabs | Text-to-Speech | https://elevenlabs.io |

## 📖 שימוש

### הרצת דמו (בלי API keys)
```bash
python main.py --demo
```

### הרצה מלאה
```bash
# סקירה בעברית
python main.py --product owala_freesip --language hebrew

# סקירה באנגלית
python main.py --product owala_freesip --language english
```

### רשימת מוצרים זמינים
```bash
python main.py --list-products
```

## 📁 מבנה הפרויקט

```
product-review-automation/
├── config/
│   └── settings.py          # הגדרות ו-API keys
├── scrapers/
│   └── product_scraper.py   # איסוף מידע על מוצרים
├── generators/
│   ├── script_generator.py  # יצירת תסריטים
│   ├── voice_generator.py   # ElevenLabs TTS
│   └── video_generator.py   # MoviePy video
├── templates/
│   └── fonts/               # גופנים
├── output/
│   └── videos/              # סרטונים מוכנים
├── assets/                  # תמונות, מוזיקה
├── main.py                  # נקודת כניסה
├── requirements.txt
└── README.md
```

## 🔄 תהליך העבודה

```
1. קלט: URL/שם מוצר
         ↓
2. איסוף מידע (Scraper)
         ↓
3. יצירת תסריט (Claude API)
         ↓
4. יצירת קול (ElevenLabs)
         ↓
5. יצירת וידאו (MoviePy)
         ↓
6. פלט: קובץ MP4 מוכן להעלאה
```

## 💰 עלויות משוערות

| שירות | מחיר | לסרטון של 3 דקות |
|--------|------|------------------|
| Claude API | $0.003/1K tokens | ~$0.05 |
| ElevenLabs | $0.30/1K chars | ~$0.50 |
| **סה"כ** | | **~$0.55** |

## 🛠️ פיתוח עתידי

- [ ] הוספת מוצרים נוספים
- [ ] אינטגרציה עם YouTube Data API
- [ ] יצירת Thumbnails אוטומטית
- [ ] תמיכה באווטאר AI (HeyGen)
- [ ] Web interface
- [ ] Batch processing

## 🤝 תרומה

Pull requests יתקבלו בברכה!

## 📄 רישיון

MIT License

---

נבנה עם ❤️ ו-AI
