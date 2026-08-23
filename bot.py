import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ⚠️ መረጃዎችህን እዚህ አስተካክል
BOT_TOKEN = "8301746478:AAG8NBsjPtuZvia-9Ai8UG4WGEYXyJO6yw8"
WEBAPP_URL = "https://sami37-cpu.github.io/my-bingo-bot/" 

# 6 ቻናሎች (1-5 ግዴታ፤ 6ኛው አማራጭ)
CHANNELS = [
    "@safariicomgift",  # 1. ግዴታ
    "@safarigiftti",  # 2. ግዴታ
    "@safariicom_gift",  # 3. ግዴታ
    "@Big_Tech_sami",  # 4. ግዴታ
    "@proofofpaymenty",  # 5. ግዴታ
    "@alpha_bet_12"   # 6. አማራጭ (ያለቀላቀለም ያሳልፈዋል)
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_join_channels(update, context)

async def show_join_channels(update, context):
    keyboard = []
    for i, ch in enumerate(CHANNELS, start=1):
        clean_ch = ch.replace("@", "")
        label = f"📢 ቻናል {i} ይቀላቀሉ" if i <= 5 else f"📢 ቻናል {i} (አማራጭ)"
        keyboard.append([InlineKeyboardButton(label, url=f"https://t.me/{clean_ch}")])
        
    keyboard.append([InlineKeyboardButton("✅ ተቀላቅያለሁ (Check)", callback_data="verify_join")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    msg_text = "👋 **እንኳን ወደ SAFARI BINGO በደህና መጡ!**\n\nጨዋታውን ለመጀመር እባክዎን ከታች ያሉትን ቻናሎች ይቀላቀሉ፦"
    
    if update.message:
        await update.message.reply_text(msg_text, reply_markup=reply_markup, parse_mode="Markdown")
    elif update.callback_query:
        await update.callback_query.message.edit_text(msg_text, reply_markup=reply_markup, parse_mode="Markdown")

async def verify_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    not_joined = []
    
    # የመጀመሪያዎቹን 5 ቻናሎች ብቻ ይፈትሻል
    for ch in CHANNELS[:5]:
        try:
            member = await context.bot.get_chat_member(chat_id=ch, user_id=user_id)
            if member.status in ['left', 'kicked']:
                not_joined.append(ch)
        except Exception:
            pass

    if not_joined:
        await query.message.reply_text(
            f"⚠️ **እባክዎን ሁሉንም 5 ግዴታ ቻናሎች መቀላቀልዎን ያረጋግጡ!**\n\nያልተቀላቀሏቸው፦ {', '.join(not_joined)}"
        )
    else:
        webapp_btn = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎮 SAFARI BINGO ክፈት", web_app=WebAppInfo(url=WEBAPP_URL))]
        ])
        await query.message.edit_text(
            "🎉 **እንኳን ደስ አለዎት!**\n\nበመመዝገብዎ የ **20 ብር** ጅምር ቦነስ አግኝተዋል። ከታች ያለውን ቁልፍ ተጭነው ይጫወቱ!",
            reply_markup=webapp_btn,
            parse_mode="Markdown"
        )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(verify_join, pattern="^verify_join$"))
    print("Safari Bingo Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
