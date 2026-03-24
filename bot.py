import telebot
import requests
import random
import os
from apscheduler.schedulers.background import BackgroundScheduler
from collections import defaultdict

TOKEN = os.getenv("BOT_TOKEN") or "8361512299:AAHpyGsmkMFRte2NZ92WAD2D9DaOB-tD2jc"   # ← Yahan apna token daal do (Railway pe env variable mein)
bot = telebot.TeleBot(TOKEN)

# ================== 80+ BEST HEART TOUCHING SHAYARI (No repeat until all used) ==================
shayari_list = [
    "दिल-ए-नादाँ तुझे हुआ क्या है\nआख़िर इस दर्द की दवा क्या है — ग़ालिब",
    "इश्क़ ने ग़ालिब निकम्मा कर दिया\nवरना हम भी आदमी बहुत क़ाबिल थे — ग़ालिब",
    "दिल न उम्मीद तो नहीं नाकाम ही तो है\nलंबी है ग़म की शाम मगर शाम ही तो है — फ़ैज़",
    "तेरे बिना ये चाँद भी अधूरा है\nतेरे बिना ये दिल भी अधूरा है",
    "हुस्न से भी ज़्यादा ख़ूबसूरत है वो इंतज़ार\nजिसमें तेरा नाम हो",
    "मोहब्बत में कभी हार मत मानना\nक्योंकि हारने वाला कभी जीतता नहीं",
    "जो तुझको देखकर मुस्कुरा दे\nवो तेरी मोहब्बत में मरता है",
    "कभी-कभी मेरे दिल में ख़याल आता है\nकि जैसे तू मेरे पास बैठी नहीं — ग़ालिब",
    "ज़िंदगी यूँ ही गुज़र जाएगी\nअगर तू मेरे साथ ना हो तो",
    "आज फिर दिल ने कहा है\nकि तू ही मेरा आराम है",
    "ग़मों का बोझ इतना है कि हँसते भी नहीं\nफिर भी तेरी याद में मुस्कुरा देते हैं",
    "प्यार वो नहीं जो हज़ार बार कहे\nप्यार वो है जो एक बार कहकर ज़िंदगी भर निभाए",
    "तुम्हारी यादों का सिलसिला ऐसा है\nकि भूलना चाहूँ तो भी भूल न पाऊँ",
    "ना था कुछ तो खुदा था, कुछ न होता तो खुदा होता\nडुबोया मुझको होने ने — ग़ालिब",
    "हज़ारों ख़्वाहिशें ऐसी कि हर ख़्वाहिश पे दम निकले — ग़ालिब",
    "ये इश्क़ नहीं आसान बस इतनी सी बात है\nएक आग का दरिया है और डूब के जाना है",
    "मैं अकेला ही चला था जानिब-ए-मंज़िल मगर\nलोग साथ आते गए और कारवाँ बनता गया",
    "बारिश की बूँदें भी शर्माती हैं\nजब तेरी याद में मेरी आँखें भर आती हैं",
    "मेरा तो बस एक ही गुनाह है\nकि मैं तुझे बहुत चाहता हूँ",
    "जो लोग कहते हैं समय सब ठीक कर देता है\nउन्हें कभी सचचा दर्द नहीं हुआ",
    "तेरी याद में रोते-रोते आँखें थक गईं\nफिर भी दिल कहता है एक बार और याद कर",
    # Agar aur chahiye toh bol dena, main 50-100 extra de dunga
]

used_shayari = set()

def get_fresh_shayari():
    available = [s for s in shayari_list if s not in used_shayari]
    if not available:
        used_shayari.clear()
        available = shayari_list[:]
    shayari = random.choice(available)
    used_shayari.add(shayari)
    return shayari

# Track active users for better tagging
active_users = defaultdict(list)

# ================== DAILY AUTOMATIC POST ==================
daily_chats = set()
def daily_job():
    if not daily_chats: return
    shayari = get_fresh_shayari()
    try:
        q = requests.get("https://zenquotes.io/api/random", timeout=5).json()[0]
        quote = f'"{q["q"]}"\n— {q["a"]}'
    except:
        quote = "Keep shining today ✨"
    msg = f"🌅 **Daily Inspiration** 🌅\n\n✨ Shayari of the Day:\n{shayari}\n\n📜 Quote of the Day:\n{quote}"
    for cid in list(daily_chats):
        try:
            bot.send_message(cid, msg, parse_mode="Markdown")
        except:
            pass

scheduler = BackgroundScheduler()
scheduler.add_job(daily_job, 'interval', hours=24)
scheduler.start()

# ================== SINGLE USER COMMANDS (Yeh tumne abhi poocha tha) ==================
@bot.message_handler(commands=['shayari'])
def single_shayari(message):
    shayari = get_fresh_shayari()
    bot.reply_to(message, f"✨ **Fresh Shayari** ✨\n\n{shayari}")

@bot.message_handler(commands=['quote'])
def single_quote(message):
    try:
        q = requests.get("https://zenquotes.io/api/random", timeout=5).json()[0]
        bot.reply_to(message, f'📜 **Fresh Quote** 📜\n\n"{q["q"]}"\n— {q["a"]}')
    except:
        bot.reply_to(message, "Quote abhi nahi aa raha, thodi der baad try karo 😔")

# Extra single commands (optional but useful)
@bot.message_handler(commands=['love', 'sad', 'motivation', 'ghalib'])
def category_shayari(message):
    cmd = message.text[1:].lower()
    #