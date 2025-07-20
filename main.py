import asyncio
import nest_asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# 🔧 Your details
BOT_TOKEN = '7896100789:AAEjpR9QdgJ3DNT8UhxqH9NQgiQy6pp2s1M'
CHANNEL_ID = '@desiworld2025'
ADMIN_ID = 6875508116  # your user ID

waiting_for_message = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ You're not authorized to use this bot.")
        return
    waiting_for_message[update.effective_user.id] = True
    await update.message.reply_text("📝 Please tell the message to post to the channel.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        return

    if waiting_for_message.get(user_id):
        await context.bot.send_message(chat_id=CHANNEL_ID, text=update.message.text)
        await update.message.reply_text("✅ Message posted to the channel.")
        waiting_for_message[user_id] = False
    else:
        await update.message.reply_text("⚠️ Please type /start first to begin.")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    await app.run_polling()

# 👇 Fix for Replit event loop
if __name__ == '__main__':
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(main())
