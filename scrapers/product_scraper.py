"""
Product Data Scraper Module
Collects product information from various sources
"""

import re
import json
import requests
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from bs4 import BeautifulSoup


@dataclass
class ProductData:
    """Data structure for product information"""
    name: str
    brand: str
    price: float
    currency: str
    rating: float
    review_count: int
    asin: str
    url: str
    images: List[str]
    features: List[str]
    pros: List[str]
    cons: List[str]
    description: str
    specs: Dict[str, str]
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


# =============================================================================
# OWALA FREESIP DATA - Pre-collected from research
# =============================================================================

OWALA_FREESIP_24OZ = ProductData(
    name="Owala FreeSip Insulated Stainless Steel Water Bottle",
    brand="Owala",
    price=27.99,
    currency="USD",
    rating=4.8,
    review_count=150000,  # Approximate
    asin="B085DTZQNZ",
    url="https://www.amazon.com/dp/B085DTZQNZ",
    images=[
        "https://m.media-amazon.com/images/I/61JUu5tn8GL._AC_SL1500_.jpg",
        "https://m.media-amazon.com/images/I/71wqmxNiAML._AC_SL1500_.jpg",
        "https://m.media-amazon.com/images/I/71PjcvBRr5L._AC_SL1500_.jpg",
    ],
    features=[
        "פטנט FreeSip - שתייה דרך קש או גמיעה ישירה",
        "בידוד דו-שכבתי - שומר קור עד 24 שעות",
        "מכסה עם נעילה כפולה - אטום לחלוטין",
        "ידית נשיאה נוחה שמשמשת גם כמנעול",
        "פתח רחב לניקוי קל והכנסת קרח",
        "מתאים למתקן כוסות ברכב (24oz)",
        "ללא BPA, עופרת, ופתלטים",
        "מכסה בטוח למדיח כלים",
    ],
    pros=[
        "עיצוב ייחודי - אפשר לשתות מקש או ישירות בלי לפתוח מכסה",
        "אטימות מושלמת - אפשר לזרוק לתיק בלי דאגה",
        "שומר קר מעולה - קרח נשאר יותר מיום שלם",
        "ויראלי בטיקטוק - 272 מיליון צפיות בהאשטאג",
        "מגוון צבעים ועיצובים מטורפים",
        "קש מוסתר ומוגן מחיידקים",
        "נוח לאחיזה - יש שקעים בגוף הבקבוק",
        "מחיר סביר ביחס למתחרים (Hydro Flask, Stanley)",
        "אחריות לכל החיים מהיצרן",
    ],
    cons=[
        "לא מתאים למשקאות חמים או מוגזים",
        "הגרסאות הגדולות (32oz, 40oz) לא נכנסות למתקן כוסות",
        "צריך לנקות לעיתים קרובות - עלול להצטבר עובש בחלקי הסיליקון",
        "קצת כבד בהשוואה לבקבוקי פלסטיק",
        "המכסה נפתח בכוח - צריך להיזהר שלא לפגוע בעצמך",
        "הציפוי עלול להישחק עם הזמן",
        "הדפסים לא עמידים למדיח כלים",
    ],
    description="""
    בקבוק המים Owala FreeSip הוא אחד המוצרים הויראליים ביותר בטיקטוק, 
    עם למעלה מ-272 מיליון צפיות בהאשטאג #owala. 
    
    מה שמייחד אותו מכל בקבוק אחר הוא הפטנט הייחודי FreeSip - 
    פתח כפול שמאפשר לשתות גם דרך קש מובנה וגם לגמוע ישירות, 
    בלי צורך לפתוח או להחליף מכסים.
    
    הבקבוק עשוי מנירוסטה עם בידוד דו-שכבתי שאמור לשמור על המשקאות 
    קרים עד 24 שעות. במבחנים שנעשו, הבקבוק אכן עמד בהבטחה הזו.
    
    זמין בשלושה גדלים: 24oz, 32oz, ו-40oz, ובמגוון צבעים מטורף 
    עם שמות יצירתיים כמו "Shy Marshmallow", "Smooshed Blueberry", 
    ו-"Very Very Dark".
    """,
    specs={
        "נפח": "24 אונקיות (710 מ\"ל)",
        "גובה": "10.26 אינץ' (26 ס\"מ)",
        "קוטר": "3.12 אינץ' (7.9 ס\"מ)",
        "משקל": "כ-400 גרם",
        "חומר": "נירוסטה 18/8 + פלסטיק ללא BPA",
        "בידוד": "דו-שכבתי (Double-wall)",
        "שמירת קור": "עד 24 שעות",
        "מדיח כלים": "מכסה בלבד",
        "אחריות": "לכל החיים",
    }
)


def get_product_data(product_id: str = "owala_freesip") -> ProductData:
    """
    Get product data by ID.
    Currently returns pre-collected data.
    In the future, will scrape live data.
    """
    products = {
        "owala_freesip": OWALA_FREESIP_24OZ,
    }
    
    return products.get(product_id, OWALA_FREESIP_24OZ)


def format_product_for_script(product: ProductData) -> str:
    """
    Format product data for script generation prompt
    """
    return f"""
מוצר: {product.name}
מותג: {product.brand}
מחיר: ${product.price}
דירוג: {product.rating}/5 ({product.review_count:,} ביקורות)

תיאור:
{product.description}

תכונות עיקריות:
{chr(10).join(f"• {f}" for f in product.features)}

יתרונות:
{chr(10).join(f"✓ {p}" for p in product.pros)}

חסרונות:
{chr(10).join(f"✗ {c}" for c in product.cons)}

מפרט טכני:
{chr(10).join(f"• {k}: {v}" for k, v in product.specs.items())}
"""


# =============================================================================
# FUTURE: Live scraping functions
# =============================================================================

class AmazonScraper:
    """
    Amazon product scraper
    Note: For production use, consider using Amazon Product API
    """
    
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
    
    def scrape_product(self, url: str) -> Optional[ProductData]:
        """
        Scrape product data from Amazon URL
        This is a basic implementation - Amazon blocks scrapers
        For production, use Amazon Product Advertising API
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Extract ASIN from URL
            asin_match = re.search(r'/dp/([A-Z0-9]{10})', url)
            asin = asin_match.group(1) if asin_match else ""
            
            # This would need proper selectors for real scraping
            # Amazon's HTML structure changes frequently
            
            return None  # Placeholder
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None


if __name__ == "__main__":
    # Test the module
    product = get_product_data("owala_freesip")
    print(product.to_json())
    print("\n" + "="*50 + "\n")
    print(format_product_for_script(product))
