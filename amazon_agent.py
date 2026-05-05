#!/usr/bin/env python3
"""
Smart Shopper US - Agent v4
Downloads product images and uploads directly to Telegram
"""

import requests
import schedule
import time
import random
import io
from datetime import datetime

TELEGRAM_BOT_TOKEN = "8674344886:AAFqQr3YyYCbpIh93n5_0ndPTrwIPZhJ-zI"
TELEGRAM_CHANNEL = "@SmartShopperUS"
AMAZON_ASSOCIATE_ID = "bestdealsu0d4-20"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
    "Referer": "https://www.amazon.com/",
}

PRODUCTS = [
    {"name": "Fire TV Stick 4K Max", "asin": "B08MT4MY9J", "img": "https://m.media-amazon.com/images/I/51TjJOTfslL._AC_SL500_.jpg", "price": "$39.99", "original": "$59.99", "discount": "33%", "emoji": "📺", "cat": "Electronics"},
    {"name": "Echo Dot 5th Gen", "asin": "B09B8V1LZ3", "img": "https://m.media-amazon.com/images/I/61yGZjXYnwL._AC_SL500_.jpg", "price": "$29.99", "original": "$49.99", "discount": "40%", "emoji": "🔊", "cat": "SmartHome"},
    {"name": "Kindle Paperwhite", "asin": "B08KTZ8249", "img": "https://m.media-amazon.com/images/I/61t3qDjWRHL._AC_SL500_.jpg", "price": "$99.99", "original": "$139.99", "discount": "29%", "emoji": "📖", "cat": "Electronics"},
    {"name": "Apple AirPods Pro 2nd Gen", "asin": "B0BDHWDR12", "img": "https://m.media-amazon.com/images/I/61SUj2aKoEL._AC_SL500_.jpg", "price": "$189.99", "original": "$249.99", "discount": "24%", "emoji": "🎧", "cat": "Audio"},
    {"name": "Bose QuietComfort 45", "asin": "B098FKXT8L", "img": "https://m.media-amazon.com/images/I/51JOBkygupL._AC_SL500_.jpg", "price": "$229.99", "original": "$329.99", "discount": "30%", "emoji": "🎵", "cat": "Audio"},
    {"name": "Anker 65W USB-C Charger", "asin": "B09C5NCNSS", "img": "https://m.media-amazon.com/images/I/61mEuJkvYYL._AC_SL500_.jpg", "price": "$19.99", "original": "$35.99", "discount": "44%", "emoji": "🔌", "cat": "Electronics"},
    {"name": "Logitech MX Master 3 Mouse", "asin": "B07S395RWD", "img": "https://m.media-amazon.com/images/I/61ni3t1ryQL._AC_SL500_.jpg", "price": "$69.99", "original": "$99.99", "discount": "30%", "emoji": "🖱️", "cat": "Office"},
    {"name": "Sony WH-1000XM5", "asin": "B09XS7JWHH", "img": "https://m.media-amazon.com/images/I/61lRdMzTCRL._AC_SL500_.jpg", "price": "$279.99", "original": "$399.99", "discount": "30%", "emoji": "🎧", "cat": "Audio"},
    {"name": "Ring Video Doorbell", "asin": "B08N5NQ69J", "img": "https://m.media-amazon.com/images/I/71F7bOoHIAL._AC_SL500_.jpg", "price": "$59.99", "original": "$99.99", "discount": "40%", "emoji": "🔔", "cat": "Security"},
    {"name": "SanDisk 1TB Portable SSD", "asin": "B08GYM5F8G", "img": "https://m.media-amazon.com/images/I/71NIFbKhEHL._AC_SL500_.jpg", "price": "$79.99", "original": "$129.99", "discount": "38%", "emoji": "💾", "cat": "Storage"},
    {"name": "Echo Show 8 2nd Gen", "asin": "B084DC4LW6", "img": "https://m.media-amazon.com/images/I/61yh5K4ASEL._AC_SL500_.jpg", "price": "$89.99", "original": "$129.99", "discount": "31%", "emoji": "🖥️", "cat": "SmartHome"},
    {"name": "Instant Pot Duo 7-in-1", "asin": "B00FLYWNYQ", "img": "https://m.media-amazon.com/images/I/71V1cYvFqNL._AC_SL500_.jpg", "price": "$59.99", "original": "$99.99", "discount": "40%", "emoji": "🍲", "cat": "Kitchen"},
    {"name": "Ninja Air Fryer Pro", "asin": "B07FDJMC9Q", "img": "https://m.media-amazon.com/images/I/71+8LYjLxrL._AC_SL500_.jpg", "price": "$89.99", "original": "$129.99", "discount": "31%", "emoji": "🍗", "cat": "Kitchen"},
    {"name": "Cuisinart Coffee Maker", "asin": "B07YFCQL3B", "img": "https://m.media-amazon.com/images/I/71pNjLXGJIL._AC_SL500_.jpg", "price": "$49.99", "original": "$79.99", "discount": "38%", "emoji": "☕", "cat": "Kitchen"},
    {"name": "Stanley Quencher 40oz", "asin": "B09JQMJHXY", "img": "https://m.media-amazon.com/images/I/71oBGfMlFSL._AC_SL500_.jpg", "price": "$35.00", "original": "$45.00", "discount": "22%", "emoji": "🥤", "cat": "Kitchen"},
    {"name": "KitchenAid Stand Mixer", "asin": "B00005UP2P", "img": "https://m.media-amazon.com/images/I/81mSLY3IULL._AC_SL500_.jpg", "price": "$349.99", "original": "$499.99", "discount": "30%", "emoji": "👨‍🍳", "cat": "Kitchen"},
    {"name": "Nespresso Vertuo Coffee", "asin": "B07NQBQB6Z", "img": "https://m.media-amazon.com/images/I/61Np3KYDPSL._AC_SL500_.jpg", "price": "$99.00", "original": "$179.00", "discount": "45%", "emoji": "☕", "cat": "Kitchen"},
    {"name": "Lodge Cast Iron Skillet", "asin": "B00006JSUA", "img": "https://m.media-amazon.com/images/I/71o2JwaTFzL._AC_SL500_.jpg", "price": "$19.90", "original": "$33.99", "discount": "41%", "emoji": "🍳", "cat": "Kitchen"},
    {"name": "Keurig K-Mini Coffee Maker", "asin": "B07GV2S1GS", "img": "https://m.media-amazon.com/images/I/71coPHjPYlL._AC_SL500_.jpg", "price": "$59.99", "original": "$99.99", "discount": "40%", "emoji": "☕", "cat": "Kitchen"},
    {"name": "Dash Mini Waffle Maker", "asin": "B074W5PMQD", "img": "https://m.media-amazon.com/images/I/81VdcGr3Y5L._AC_SL500_.jpg", "price": "$9.99", "original": "$19.99", "discount": "50%", "emoji": "🧇", "cat": "Kitchen"},
    {"name": "iRobot Roomba i3+", "asin": "B08C4L2V8Z", "img": "https://m.media-amazon.com/images/I/71L9xBbB7GL._AC_SL500_.jpg", "price": "$249.99", "original": "$399.99", "discount": "38%", "emoji": "🤖", "cat": "Home"},
    {"name": "LEVOIT Air Purifier", "asin": "B07CNCS3QL", "img": "https://m.media-amazon.com/images/I/617yD5JRDIL._AC_SL500_.jpg", "price": "$79.99", "original": "$119.99", "discount": "33%", "emoji": "🌬️", "cat": "Home"},
    {"name": "Beckham Hotel Pillows", "asin": "B07PY9HGQ5", "img": "https://m.media-amazon.com/images/I/81hQHGBaRHL._AC_SL500_.jpg", "price": "$29.99", "original": "$49.99", "discount": "40%", "emoji": "🛏️", "cat": "Home"},
    {"name": "Philips Hue Smart Bulb 4pk", "asin": "B07QLQH4MX", "img": "https://m.media-amazon.com/images/I/71kD9UdEGXL._AC_SL500_.jpg", "price": "$44.99", "original": "$64.99", "discount": "31%", "emoji": "💡", "cat": "SmartHome"},
    {"name": "Amazon Smart Plug", "asin": "B089DR29T6", "img": "https://m.media-amazon.com/images/I/31ynpME0QfL._AC_SL500_.jpg", "price": "$14.99", "original": "$24.99", "discount": "40%", "emoji": "🔌", "cat": "SmartHome"},
    {"name": "Shark Robot Vacuum", "asin": "B07THHQMHM", "img": "https://m.media-amazon.com/images/I/61H6YOOFUNL._AC_SL500_.jpg", "price": "$179.99", "original": "$299.99", "discount": "40%", "emoji": "🤖", "cat": "Home"},
    {"name": "CeraVe Moisturizing Cream", "asin": "B00TTD9BRC", "img": "https://m.media-amazon.com/images/I/61S+O2yvLBL._AC_SL500_.jpg", "price": "$14.99", "original": "$21.99", "discount": "32%", "emoji": "💆", "cat": "Beauty"},
    {"name": "Neutrogena Hydro Boost", "asin": "B01LYB9HKF", "img": "https://m.media-amazon.com/images/I/71rXtFuXAcL._AC_SL500_.jpg", "price": "$12.99", "original": "$19.99", "discount": "35%", "emoji": "✨", "cat": "Beauty"},
    {"name": "Oral-B Pro 1000 Toothbrush", "asin": "B07DFW5KBJ", "img": "https://m.media-amazon.com/images/I/71YBYKHFSBL._AC_SL500_.jpg", "price": "$29.99", "original": "$49.99", "discount": "40%", "emoji": "🦷", "cat": "Health"},
    {"name": "Revlon Hair Dryer Brush", "asin": "B01LSUQSB0", "img": "https://m.media-amazon.com/images/I/71eFCBJTlHL._AC_SL500_.jpg", "price": "$34.88", "original": "$59.99", "discount": "42%", "emoji": "💇", "cat": "Beauty"},
    {"name": "Vitamin D3 5000 IU", "asin": "B00FQKTSRQ", "img": "https://m.media-amazon.com/images/I/71i4iNDvLIL._AC_SL500_.jpg", "price": "$14.99", "original": "$24.99", "discount": "40%", "emoji": "💊", "cat": "Health"},
    {"name": "Collagen Peptides Powder", "asin": "B00K6HLD4O", "img": "https://m.media-amazon.com/images/I/61DlKwBDdgL._AC_SL500_.jpg", "price": "$29.99", "original": "$44.99", "discount": "33%", "emoji": "💪", "cat": "Health"},
    {"name": "EltaMD UV Clear Sunscreen", "asin": "B002MSN3QQ", "img": "https://m.media-amazon.com/images/I/61wT58u3ndL._AC_SL500_.jpg", "price": "$38.00", "original": "$52.00", "discount": "27%", "emoji": "☀️", "cat": "Beauty"},
    {"name": "Natrol Melatonin 10mg", "asin": "B00012NGIE", "img": "https://m.media-amazon.com/images/I/71TzqrYceiL._AC_SL500_.jpg", "price": "$8.49", "original": "$14.99", "discount": "43%", "emoji": "😴", "cat": "Health"},
    {"name": "Resistance Bands Set 11pc", "asin": "B01AVDVHTI", "img": "https://m.media-amazon.com/images/I/81TDyEKPxGL._AC_SL500_.jpg", "price": "$12.99", "original": "$24.99", "discount": "48%", "emoji": "💪", "cat": "Sports"},
    {"name": "Yoga Mat Premium 6mm", "asin": "B08RV5XDHB", "img": "https://m.media-amazon.com/images/I/71xjp9WKYCL._AC_SL500_.jpg", "price": "$19.99", "original": "$34.99", "discount": "43%", "emoji": "🧘", "cat": "Sports"},
    {"name": "Hydro Flask Water Bottle", "asin": "B01ACAOB96", "img": "https://m.media-amazon.com/images/I/81iaTrJHRGL._AC_SL500_.jpg", "price": "$34.95", "original": "$49.95", "discount": "30%", "emoji": "💧", "cat": "Sports"},
    {"name": "Fitbit Charge 6", "asin": "B0CDR3HGWX", "img": "https://m.media-amazon.com/images/I/71bL4MdM+PL._AC_SL500_.jpg", "price": "$99.95", "original": "$159.99", "discount": "38%", "emoji": "⌚", "cat": "Fitness"},
    {"name": "Bowflex Adjustable Dumbbells", "asin": "B001ARYU58", "img": "https://m.media-amazon.com/images/I/71U-sPZGKJL._AC_SL500_.jpg", "price": "$279.00", "original": "$399.00", "discount": "30%", "emoji": "🏋️", "cat": "Sports"},
    {"name": "Foam Roller for Muscles", "asin": "B00XM2MXK8", "img": "https://m.media-amazon.com/images/I/71H0YvOLKNL._AC_SL500_.jpg", "price": "$19.99", "original": "$34.99", "discount": "43%", "emoji": "🏃", "cat": "Sports"},
    {"name": "LEGO Classic Creative Bricks", "asin": "B013Y28P7Y", "img": "https://m.media-amazon.com/images/I/81wkBdaE6tL._AC_SL500_.jpg", "price": "$39.99", "original": "$59.99", "discount": "33%", "emoji": "🧱", "cat": "Toys"},
    {"name": "Hot Wheels 20 Car Pack", "asin": "B07GDPCNSC", "img": "https://m.media-amazon.com/images/I/81SnBObFgML._AC_SL500_.jpg", "price": "$19.97", "original": "$34.99", "discount": "43%", "emoji": "🚗", "cat": "Toys"},
    {"name": "Play-Doh 36 Can Bundle", "asin": "B00JM5GW10", "img": "https://m.media-amazon.com/images/I/91sD7fBUlCL._AC_SL500_.jpg", "price": "$22.44", "original": "$39.99", "discount": "44%", "emoji": "🎨", "cat": "Toys"},
    {"name": "PS5 DualSense Controller", "asin": "B08FC6C75Y", "img": "https://m.media-amazon.com/images/I/61HzTFVBXQL._AC_SL500_.jpg", "price": "$54.99", "original": "$69.99", "discount": "21%", "emoji": "🎮", "cat": "Gaming"},
    {"name": "Nintendo Switch Mario Kart", "asin": "B09V1JCJ7N", "img": "https://m.media-amazon.com/images/I/71bXLSJjMCL._AC_SL500_.jpg", "price": "$299.00", "original": "$399.00", "discount": "25%", "emoji": "🎮", "cat": "Gaming"},
    {"name": "Atomic Habits Book", "asin": "0735211299", "img": "https://m.media-amazon.com/images/I/81wgcld4wxL._AC_SL500_.jpg", "price": "$14.99", "original": "$27.00", "discount": "44%", "emoji": "📚", "cat": "Books"},
    {"name": "The Psychology of Money", "asin": "0857197681", "img": "https://m.media-amazon.com/images/I/71g2ednj0JL._AC_SL500_.jpg", "price": "$14.29", "original": "$22.99", "discount": "38%", "emoji": "💰", "cat": "Books"},
    {"name": "Coleman Camping Tent 4P", "asin": "B002TPZDAU", "img": "https://m.media-amazon.com/images/I/81Hy4TCNiWL._AC_SL500_.jpg", "price": "$89.99", "original": "$149.99", "discount": "40%", "emoji": "⛺", "cat": "Outdoor"},
    {"name": "Yeti Rambler 30oz Tumbler", "asin": "B073WP39WL", "img": "https://m.media-amazon.com/images/I/71UT8J2fUZL._AC_SL500_.jpg", "price": "$34.99", "original": "$45.00", "discount": "22%", "emoji": "🥤", "cat": "Outdoor"},
    {"name": "KONG Classic Dog Toy", "asin": "B0002AR0I8", "img": "https://m.media-amazon.com/images/I/81FNBM1GCCL._AC_SL500_.jpg", "price": "$13.49", "original": "$19.99", "discount": "33%", "emoji": "🐕", "cat": "Pets"},
    {"name": "Cat Tree Tower Scratcher", "asin": "B07HCRLTG1", "img": "https://m.media-amazon.com/images/I/71-VOdJY5GL._AC_SL500_.jpg", "price": "$49.99", "original": "$79.99", "discount": "38%", "emoji": "🐈", "cat": "Pets"},
    {"name": "AmazonBasics Monitor Arm", "asin": "B00MIBN16O", "img": "https://m.media-amazon.com/images/I/81ohHpVJQRL._AC_SL500_.jpg", "price": "$29.99", "original": "$49.99", "discount": "40%", "emoji": "🖥️", "cat": "Office"},
    {"name": "Blue Light Glasses", "asin": "B07VCM8BLD", "img": "https://m.media-amazon.com/images/I/61mXCHVBJYL._AC_SL500_.jpg", "price": "$15.99", "original": "$25.99", "discount": "38%", "emoji": "👓", "cat": "Office"},
    {"name": "Anker Roav Dash Cam", "asin": "B06XHYZKGQ", "img": "https://m.media-amazon.com/images/I/61VZAOyerHL._AC_SL500_.jpg", "price": "$49.99", "original": "$79.99", "discount": "38%", "emoji": "🚗", "cat": "Auto"},
    {"name": "Portable Jump Starter", "asin": "B07FNTKSXS", "img": "https://m.media-amazon.com/images/I/81wPbLJd2NL._AC_SL500_.jpg", "price": "$49.99", "original": "$79.99", "discount": "38%", "emoji": "🔋", "cat": "Auto"},
    {"name": "Ray-Ban Aviator Sunglasses", "asin": "B001NK2ADK", "img": "https://m.media-amazon.com/images/I/71qoqSdB0BL._AC_SL500_.jpg", "price": "$104.00", "original": "$154.00", "discount": "32%", "emoji": "🕶️", "cat": "Fashion"},
    {"name": "Insulated Lunch Box Bag", "asin": "B076JBP9VC", "img": "https://m.media-amazon.com/images/I/71iLrVE2pSL._AC_SL500_.jpg", "price": "$19.99", "original": "$34.99", "discount": "43%", "emoji": "🍱", "cat": "Outdoor"},
    {"name": "Garmin Forerunner 255", "asin": "B09WK4FX7T", "img": "https://m.media-amazon.com/images/I/61VaJV0JDAL._AC_SL500_.jpg", "price": "$249.99", "original": "$349.99", "discount": "29%", "emoji": "⌚", "cat": "Sports"},
    {"name": "Purina Pro Plan Dog Food", "asin": "B0BDBNTVP5", "img": "https://m.media-amazon.com/images/I/81YBxSFg0nL._AC_SL500_.jpg", "price": "$59.98", "original": "$79.98", "discount": "25%", "emoji": "🐾", "cat": "Pets"},
]

TEMPLATES = [
    "🔥 *DEAL ALERT!* 🔥\n\n{emoji} *{name}*\n\n💰 ~~{original}~~ → *{price}*\n🏷️ Save *{discount} OFF* today!\n\n🛒 *Shop Now:*\n{link}\n\n⚡ Limited time offer!\n━━━━━━━━━━━━━━━\n📢 @SmartShopperUS\n#AmazonDeals #{cat} #Sale",
    "💥 *HOT DEAL OF THE HOUR!* 💥\n\n{emoji} *{name}*\n\n✅ Price: *{price}* (was {original})\n✅ Discount: *{discount} OFF*\n✅ Free Prime Shipping!\n\n👇 *BUY NOW:*\n{link}\n\n⏰ Hurry! Deal ends soon!\n━━━━━━━━━━━━━━━\n🛍️ @SmartShopperUS #Amazon #{cat}",
    "🛍️ *SMART PICK!*\n\n{emoji} *{name}*\n\n📊 Was: ~~{original}~~\n📊 Now: *{price}*\n📊 You Save: *{discount}*!\n\n🔗 *Buy here:*\n{link}\n\n💡 _Affiliate link — no extra cost to you!_\n━━━━━━━━━━━━━━━\n@SmartShopperUS 🛒 #{cat}",
    "⭐ *TODAY'S FEATURED DEAL!* ⭐\n\n{emoji} *{name}*\n\n💵 Regular: ~~{original}~~\n💵 Sale: *{price}*\n💵 You save: *{discount}*!\n\n🛒 *Get it now:*\n{link}\n\n🔔 Follow @SmartShopperUS!\n#AmazonDeals #{cat} #USADeals",
]

def make_affiliate_link(asin):
    return f"https://www.amazon.com/dp/{asin}?tag={AMAZON_ASSOCIATE_ID}"

def download_image(url):
    """Download image bytes from URL"""
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code == 200 and len(r.content) > 1000:
            return r.content
    except Exception as e:
        print(f"Download error: {e}")
    return None

def send_photo_upload(image_bytes, caption, filename="product.jpg"):
    """Upload image bytes directly to Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    try:
        files = {"photo": (filename, io.BytesIO(image_bytes), "image/jpeg")}
        data = {"chat_id": TELEGRAM_CHANNEL, "caption": caption, "parse_mode": "Markdown"}
        r = requests.post(url, files=files, data=data, timeout=30)
        result = r.json()
        if result.get("ok"):
            print("✅ Photo uploaded!")
            return True
        print(f"❌ Upload error: {result.get('description')}")
        return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def send_telegram_message(text):
    """Send text message"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        r = requests.post(url, json={"chat_id": TELEGRAM_CHANNEL, "text": text, "parse_mode": "Markdown"}, timeout=10)
        result = r.json()
        if result.get("ok"):
            print("✅ Text posted!")
            return True
        print(f"❌ Error: {result.get('description')}")
        return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def post_deal():
    product = random.choice(PRODUCTS)
    template = random.choice(TEMPLATES)
    link = make_affiliate_link(product["asin"])
    caption = template.format(
        emoji=product["emoji"], name=product["name"],
        price=product["price"], original=product["original"],
        discount=product["discount"], cat=product["cat"], link=link
    )
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] {product['name']}")

    # Download image and upload
    img_bytes = download_image(product["img"])
    if img_bytes:
        success = send_photo_upload(img_bytes, caption)
        if not success:
            send_telegram_message(caption)
    else:
        print("⚠️ Image download failed, sending text")
        send_telegram_message(caption)

def post_morning_intro():
    send_telegram_message("🌅 *Good Morning, Smart Shoppers!* 🌅\n\nToday's top Amazon deals coming your way! 🛒\n\n• 📱 Electronics  • 🏠 Home & Kitchen\n• 💄 Beauty & Health  • 💪 Sports\n• 🧸 Toys & Gaming & More!\n\n👆 Turn on notifications!\n━━━━━━━━━━━━━━━\n@SmartShopperUS 🔔 #AmazonDeals")

def post_evening_summary():
    send_telegram_message("🌙 *Evening Wrap-Up!* 🌙\n\n✅ Tons of deals posted today!\n✅ Savings up to *50% OFF*!\n\n🔔 Follow @SmartShopperUS for tomorrow!\n━━━━━━━━━━━━━━━\n💰 Saving you money, every single day!")

def run_agent():
    print("🤖 Smart Shopper Agent v4 - Image Upload Mode")
    print(f"📢 {TELEGRAM_CHANNEL} | 📦 {len(PRODUCTS)} products")
    print("🖼️  Images: DOWNLOAD + UPLOAD (most reliable!)")
    print("=" * 50)

    schedule.every().day.at("08:00").do(post_morning_intro)
    schedule.every(5).minutes.do(post_deal)
    schedule.every().day.at("23:55").do(post_evening_summary)

    print("✅ ~288 posts/day | Every 5 minutes")
    print("🚀 Running...\n")

    post_deal()  # First post immediately

    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == "__main__":
    run_agent()
