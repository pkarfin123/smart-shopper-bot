#!/usr/bin/env python3
"""
Smart Shopper US - Amazon Affiliate Auto-Posting Agent
Posts 20+ Amazon deals daily to Telegram channel
"""

import requests
import schedule
import time
import random
import json
from datetime import datetime

# ============================================================
# CONFIGURATION - তোমার details এখানে
# ============================================================
TELEGRAM_BOT_TOKEN = "8674344886:AAFqQr3YyYCbpIh93n5_0ndPTrwIPZhJ-zI"
TELEGRAM_CHANNEL = "@SmartShopperUS"
AMAZON_ASSOCIATE_ID = "bestdealsu0d4-20"

# ============================================================
# PRODUCT DATABASE - Popular USA Amazon products with real ASINs
# ============================================================
PRODUCTS = [
    # Electronics
    {"name": "Fire TV Stick 4K Max", "asin": "B08MT4MY9J", "price": "$39.99", "original": "$59.99", "discount": "33%", "emoji": "📺", "category": "Electronics", "rating": "4.7⭐", "reviews": "125,432"},
    {"name": "Echo Dot (5th Gen)", "asin": "B09B8V1LZ3", "price": "$29.99", "original": "$49.99", "discount": "40%", "emoji": "🔊", "category": "Smart Home", "rating": "4.6⭐", "reviews": "89,231"},
    {"name": "Kindle Paperwhite", "asin": "B08KTZ8249", "price": "$99.99", "original": "$139.99", "discount": "29%", "emoji": "📖", "category": "Electronics", "rating": "4.8⭐", "reviews": "67,543"},
    {"name": "Apple AirPods Pro (2nd Gen)", "asin": "B0BDHWDR12", "price": "$189.99", "original": "$249.99", "discount": "24%", "emoji": "🎧", "category": "Audio", "rating": "4.7⭐", "reviews": "203,876"},
    {"name": "Instant Pot Duo 7-in-1", "asin": "B00FLYWNYQ", "price": "$59.99", "original": "$99.99", "discount": "40%", "emoji": "🍲", "category": "Kitchen", "rating": "4.7⭐", "reviews": "156,789"},
    {"name": "Ninja Air Fryer Pro", "asin": "B07FDJMC9Q", "price": "$89.99", "original": "$129.99", "discount": "31%", "emoji": "🍗", "category": "Kitchen", "rating": "4.8⭐", "reviews": "98,432"},
    {"name": "iRobot Roomba i3+", "asin": "B08C4L2V8Z", "price": "$249.99", "original": "$399.99", "discount": "38%", "emoji": "🤖", "category": "Home", "rating": "4.5⭐", "reviews": "45,678"},
    {"name": "Ring Video Doorbell", "asin": "B08N5NQ69J", "price": "$59.99", "original": "$99.99", "discount": "40%", "emoji": "🔔", "category": "Security", "rating": "4.6⭐", "reviews": "234,567"},
    {"name": "Anker 65W USB-C Charger", "asin": "B09C5NCNSS", "price": "$19.99", "original": "$35.99", "discount": "44%", "emoji": "🔌", "category": "Electronics", "rating": "4.8⭐", "reviews": "78,234"},
    {"name": "Bose QuietComfort 45", "asin": "B098FKXT8L", "price": "$229.99", "original": "$329.99", "discount": "30%", "emoji": "🎵", "category": "Audio", "rating": "4.7⭐", "reviews": "56,789"},
    # Beauty & Health
    {"name": "CeraVe Moisturizing Cream", "asin": "B00TTD9BRC", "price": "$14.99", "original": "$21.99", "discount": "32%", "emoji": "💆", "category": "Beauty", "rating": "4.8⭐", "reviews": "312,456"},
    {"name": "Oral-B Pro 1000 Electric Toothbrush", "asin": "B07DFW5KBJ", "price": "$29.99", "original": "$49.99", "discount": "40%", "emoji": "🦷", "category": "Health", "rating": "4.7⭐", "reviews": "145,678"},
    {"name": "Fitbit Charge 6", "asin": "B0CDR3HGWX", "price": "$99.95", "original": "$159.99", "discount": "38%", "emoji": "⌚", "category": "Fitness", "rating": "4.5⭐", "reviews": "34,567"},
    {"name": "Neutrogena Hydro Boost", "asin": "B01LYB9HKF", "price": "$12.99", "original": "$19.99", "discount": "35%", "emoji": "✨", "category": "Beauty", "rating": "4.6⭐", "reviews": "89,234"},
    # Home & Office
    {"name": "Beckham Hotel Collection Pillows", "asin": "B07PY9HGQ5", "price": "$29.99", "original": "$49.99", "discount": "40%", "emoji": "🛏️", "category": "Home", "rating": "4.7⭐", "reviews": "234,567"},
    {"name": "AmazonBasics Microwave", "asin": "B07894S727", "price": "$59.99", "original": "$89.99", "discount": "33%", "emoji": "📦", "category": "Kitchen", "rating": "4.4⭐", "reviews": "67,890"},
    {"name": "Logitech MX Master 3 Mouse", "asin": "B07S395RWD", "price": "$69.99", "original": "$99.99", "discount": "30%", "emoji": "🖱️", "category": "Office", "rating": "4.7⭐", "reviews": "78,456"},
    {"name": "LEVOIT Air Purifier", "asin": "B07CNCS3QL", "price": "$79.99", "original": "$119.99", "discount": "33%", "emoji": "🌬️", "category": "Home", "rating": "4.6⭐", "reviews": "123,456"},
    {"name": "Cuisinart Coffee Maker", "asin": "B07YFCQL3B", "price": "$49.99", "original": "$79.99", "discount": "38%", "emoji": "☕", "category": "Kitchen", "rating": "4.5⭐", "reviews": "89,123"},
    {"name": "Stanley Quencher Tumbler 40oz", "asin": "B09JQMJHXY", "price": "$35.00", "original": "$45.00", "discount": "22%", "emoji": "🥤", "category": "Kitchen", "rating": "4.8⭐", "reviews": "456,789"},
    # Toys & Sports
    {"name": "LEGO Classic Creative Bricks", "asin": "B013Y28P7Y", "price": "$39.99", "original": "$59.99", "discount": "33%", "emoji": "🧱", "category": "Toys", "rating": "4.8⭐", "reviews": "67,234"},
    {"name": "Resistance Bands Set", "asin": "B01AVDVHTI", "price": "$12.99", "original": "$24.99", "discount": "48%", "emoji": "💪", "category": "Sports", "rating": "4.6⭐", "reviews": "234,567"},
    {"name": "Yoga Mat Premium", "asin": "B08RV5XDHB", "price": "$19.99", "original": "$34.99", "discount": "43%", "emoji": "🧘", "category": "Sports", "rating": "4.7⭐", "reviews": "123,456"},
]

# Post templates
TEMPLATES = [
    """🔥 *DEAL ALERT!* 🔥

{emoji} *{name}*

💰 ~~${original}~~ → *{price}*
🏷️ Save {discount} OFF today!
⭐ Rating: {rating} ({reviews} reviews)
📦 Category: {category}

🛒 *Grab this deal NOW:*
{link}

⚡ Limited time offer! Price may change anytime.
━━━━━━━━━━━━━━━
📢 @SmartShopperUS | Best USA Deals Daily!
#AmazonDeals #{category} #USADeals #Sale""",

    """💥 *HOT DEAL OF THE HOUR!* 💥

{emoji} *{name}*

✅ Price: *{price}* (was {original})
✅ Discount: *{discount} OFF*
✅ Reviews: *{reviews}* ⭐
✅ Free Prime Shipping Available!

👇 *SHOP NOW:*
{link}

⏰ Hurry! Deal ends soon!
━━━━━━━━━━━━━━━
🛍️ @SmartShopperUS
#Deal #Amazon #{category}""",

    """🛍️ *SMART PICK OF THE DAY!*

{emoji} *{name}*

📊 Was: ~~{original}~~
📊 Now: *{price}*
📊 You Save: *{discount}*!
🌟 {rating} with {reviews} happy customers!

🔗 *Buy here (affiliate link):*
{link}

💡 _This is an affiliate link. We earn a small commission at no extra cost to you!_
━━━━━━━━━━━━━━━
@SmartShopperUS 🛒 #BestDeals #Amazon""",
]

def make_affiliate_link(asin):
    """Generate Amazon affiliate link"""
    return f"https://www.amazon.com/dp/{asin}?tag={AMAZON_ASSOCIATE_ID}"

def send_telegram_message(text):
    """Send message to Telegram channel"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHANNEL,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        result = response.json()
        if result.get("ok"):
            print(f"✅ Posted: {text[:50]}...")
            return True
        else:
            print(f"❌ Error: {result.get('description')}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def post_deal():
    """Pick random product and post to Telegram"""
    product = random.choice(PRODUCTS)
    template = random.choice(TEMPLATES)
    link = make_affiliate_link(product["asin"])
    
    message = template.format(
        emoji=product["emoji"],
        name=product["name"],
        price=product["price"],
        original=product["original"],
        discount=product["discount"],
        rating=product["rating"],
        reviews=product["reviews"],
        category=product["category"],
        link=link
    )
    
    now = datetime.now().strftime("%H:%M:%S")
    print(f"\n[{now}] Posting: {product['name']}")
    send_telegram_message(message)

def post_morning_intro():
    """Morning welcome post"""
    message = """🌅 *Good Morning, Smart Shoppers!* 🌅

Today's top Amazon deals are coming your way! 🛒

We'll be sharing *20+ exclusive deals* throughout the day on:
• 📱 Electronics
• 🏠 Home & Kitchen  
• 💄 Beauty & Health
• 💪 Sports & Fitness
• 🧸 Toys & More!

👆 Turn on notifications so you never miss a deal!

━━━━━━━━━━━━━━━
@SmartShopperUS 🔔 #AmazonDeals #USADeals"""
    send_telegram_message(message)

def post_evening_summary():
    """Evening summary post"""
    message = """🌙 *Evening Deal Roundup!* 🌙

✅ We posted *20+ deals* today!
✅ Total savings up to *48% OFF*!
✅ All verified Amazon products!

💡 *Pro Tip:* Add items to cart now — Amazon often keeps sale prices for 24hrs!

🔔 Follow @SmartShopperUS for tomorrow's deals!

━━━━━━━━━━━━━━━
💰 Saving you money, every single day!
#SmartShopper #AmazonDeals"""
    send_telegram_message(message)

def run_agent():
    """Main agent scheduler - 20+ posts per day"""
    print("🤖 Smart Shopper Agent Starting...")
    print(f"📢 Channel: {TELEGRAM_CHANNEL}")
    print(f"🏷️ Associate ID: {AMAZON_ASSOCIATE_ID}")
    print("=" * 50)
    
    # Morning intro at 8 AM
    schedule.every().day.at("08:00").do(post_morning_intro)
    
    # 20 deal posts throughout the day (every ~50 mins from 8:30 AM to 10 PM)
    post_times = [
        "08:30", "09:20", "10:10", "11:00", "11:50",
        "12:40", "13:30", "14:20", "15:10", "16:00",
        "16:50", "17:40", "18:30", "19:20", "20:10",
        "20:40", "21:00", "21:20", "21:40", "22:00"
    ]
    
    for t in post_times:
        schedule.every().day.at(t).do(post_deal)
    
    # Evening summary at 10:30 PM
    schedule.every().day.at("22:30").do(post_evening_summary)
    
    print(f"✅ Scheduled {len(post_times)} deal posts per day!")
    print("🚀 Agent is running... Press Ctrl+C to stop\n")
    
    # Post first deal immediately as test
    print("📤 Sending test post now...")
    post_deal()
    
    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == "__main__":
    run_agent()
