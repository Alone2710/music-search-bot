import os
import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "🎵 <b>به ربات جستجوی موسیقی خوش آمدید!</b>\n\n"
        "هر چیزی درباره آهنگ می‌دانید برای من بفرستید:\n\n"
        "🎵 اسم آهنگ\n"
        "🎤 اسم خواننده\n"
        "📝 بخشی از متن آهنگ\n"
        "🎧 فایل صوتی\n"
        "🎬 ویدئو\n\n"
        "🔎 موتور جستجوی کامل در نسخه‌های بعدی فعال می‌شود."
    )

    await update.message.reply_text(
        message,
        parse_mode="HTML",
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()

    if not query:
        return

    await update.message.reply_text(
        "🔎 <b>درخواست شما دریافت شد.</b>\n\n"
        f"جستجو:\n<code>{query}</code>\n\n"
        "⏳ موتور جستجوی آهنگ در مرحله بعد به ربات متصل می‌شود.",
        parse_mode="HTML",
    )


async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎧 فایل صوتی دریافت شد.\n\n"
        "در نسخه بعدی، ربات صدای فایل را بررسی می‌کند "
        "و تلاش می‌کند نام آهنگ و خواننده را پیدا کند."
    )


async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 ویدئو دریافت شد.\n\n"
        "در نسخه بعدی، صدای ویدئو استخراج می‌شود "
        "و برای شناسایی آهنگ بررسی خواهد شد."
    )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(
        "Exception while handling an update:",
        exc_info=context.error,
    )


def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable is not set.")

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_text
        )
    )

    application.add_handler(
        MessageHandler(
            filters.AUDIO | filters.VOICE,
            handle_audio
        )
    )

    application.add_handler(
        MessageHandler(
            filters.VIDEO,
            handle_video
        )
    )

    application.add_error_handler(error_handler)

    logger.info("Music Search Bot started.")

    application.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
