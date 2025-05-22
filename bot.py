import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "7517455172:AAHTHMHSvqIvgvjlgg1B-ncWC9_Lj4DPf_s"
CHANNEL_ID = -1744686998
CHECK_CHANNEL = "@kinolarningudari"

bot = telebot.TeleBot(BOT_TOKEN)

films = {
    "K001": 7,
}

def check_subscription(user_id):
    try:
        member = bot.get_chat_member(CHECK_CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception:
        return False

@bot.message_handler(commands=["start"])
def start_handler(message):
    user_id = message.from_user.id
    if not check_subscription(user_id):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("✅ Obuna bo'lish", url=f"https://t.me/{CHECK_CHANNEL[1:]}"))
        bot.send_message(message.chat.id, "🎬 Davom etish uchun kanalga obuna bo‘ling:", reply_markup=markup)
        return
    bot.send_message(message.chat.id, "🎬 Salom! Film kodini yuboring (masalan: K001):")

@bot.message_handler(func=lambda m: True)
def film_handler(message):
    code = message.text.strip().upper()
    if code in films:
        try:
            bot.copy_message(
                chat_id=message.chat.id,
                from_chat_id=CHANNEL_ID,
                message_id=films[code]
            )
        except Exception as e:
            bot.send_message(message.chat.id, f"⚠️ Filmni yuborib bo‘lmadi: {e}")
    else:
        bot.send_message(message.chat.id, "❌ Bunday koddagi film topilmadi.")

bot.infinity_polling()
