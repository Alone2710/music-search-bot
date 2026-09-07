import os
import logging
import threading

from flask import Flask
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# =========================
# Settings
# =========================

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

# Flask app برای Render
app = Flask(__name__)


@app.route("/")
def home():
    return "Music Search Bot is running! 🎵", 200


@app.route("/health")
def health():
    return "OK", 200


# =========================
# Telegram Bot
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🎵 <b>به ربات جستجوی موسیقی خوش آمدید!</b>\n\n"
        "می‌توانی یکی از این موارد را برای من بفرستی:\n\n"
        "🎵 اسم آهنگ\n"
        "🎤 اسم خواننده\n"
        "📝 بخشی از متن آهنگ\n"
        "🎧 فایل صوتی\n"
        "🎬 ویدئو\n\n"
        "🔎 به‌زودی جستجوی کامل آهنگ و متن فعال می‌شود."
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
    )


async def handle_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.message.text.strip()

    if not query:
        return

    await update.message.reply_text(
        "🔎 <b>درخواست شما دریافت شد.</b>\n\n"
        f"عبارت جستجو:\n<code>{query}</code>\n\n"
        "⏳ موتور جستجوی واقعی در مرحله بعد فعال می‌شود.",
        parse_mode="HTML",
    )


async def handle_audio(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "🎧 فایل صوتی دریافت شد.\n\n"
        "در مرحله بعد، ربات آهنگ را از روی صدا شناسایی می‌کند."
    )


async def handle_video(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "🎬 ویدئو دریافت شد.\n\n"
        "در مرحله بعد، صدای ویدئو استخراج و آهنگ شناسایی می‌شود."
    )


async def handle_voice(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "🎙️ پیام صوتی دریافت شد.\n\n"
        "در مرحله بعد، آهنگ داخل صدا شناسایی می‌شود."
    )


async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):
    logger.error(
        "Telegram error:",
        exc_info=context.error,
    )


def run_bot():
    """اجرای ربات تلگرام در یک Thread جداگانه."""

    if not TOKEN:
        logger.error("BOT_TOKEN is not set!")
        return

    telegram_app = (
        Application.builder()
        .token(TOKEN)
        .build()
    )

    # /start
    telegram_app.add_handler(
        CommandHandler("start", start)
    )

    # متن
    telegram_app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_text,
        )
    )

    # فایل صوتی
    telegram_app.add_handler(
        MessageHandler(
            filters.AUDIO,
            handle_audio,
        )
    )

    # Voice
    telegram_app.add_handler(
        MessageHandler(
            filters.VOICE,
            handle_voice,
        )
    )

    # Video
    telegram_app.add_handler(
        MessageHandler(
            filters.VIDEO,
            handle_video,
        )
    )

    telegram_app.add_error_handler(
        error_handler
    )

    logger.info("Telegram bot is starting...")

    telegram_app.run_polling(
        drop_pending_updates=True
    )


# =========================
# Start Telegram Bot
# =========================

if TOKEN:
    bot_thread = threading.Thread(
        target=run_bot,
        daemon=True,
    )

    bot_thread.start()

    logger.info("Bot thread started.")
else:
    logger.error(
        "BOT_TOKEN environment variable is missing."
    )


# =========================
# Local run
# =========================

if __name__ == "__main__":
    port = int(
        os.environ.get("PORT", 10000)
    )

    app.run(
        host="0.0.0.0",
        port=port,
)
