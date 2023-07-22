import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Audio
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler, CallbackQueryHandler
import actions
import os
from constants import SCHOOL_PHOTO, SELF_PHOTO, WELCOME_MESSAGE, HOBBY_TEXT
from pydub import AudioSegment
from moments.commands import start, send_selfi_photo, send_school_photo, help_command, hobby_audio
import whisper
from gtts import gTTS

from moments.menu import get_menu

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


model = whisper.load_model("base")
TOKEN = ""


def error(update, context):
    print(f'Update {update} caused error {context.error}')


@actions.send_upload_audio_action
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_id = update.message.voice.file_id
    file = await context.bot.get_file(file_id)

    path = os.path.abspath(f'/home/anvar/IdeaProjects/TelegramProject/voice_{file_id}.ogg')
    await file.download_to_drive(path)

    audio = AudioSegment.from_file(path, format='ogg')
    audio.export(f'/home/anvar/IdeaProjects/TelegramProject/voice_{file_id}.wav', format='wav')

    # Recognize speech from the downloaded voice message
    transcriptions = model.transcribe(f'/home/anvar/IdeaProjects/TelegramProject/voice_{file_id}.wav')
    await update.message.reply_text(f"Recognized text: {transcriptions['text']}")


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    if query.data == "1":
        await send_selfi_photo(update, context)
    elif query.data == "2":
        await send_school_photo(update, context)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Sorry, I didn't understand that command.")


async def process_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if text == 'селфи':
        await send_selfi_photo(update, context)
    elif text == 'фотка со школы':
        await send_school_photo(update, context)
    elif text == 'послушать увлечения':
        await hobby_audio(update, context)
    elif text == 'hide menu':
        await update.message.reply_text("Menu hidden.", reply_markup=ReplyKeyboardRemove())
    else:
        await update.message.reply_text("Invalid option. Please choose one of the menu options.")


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    # commands
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('selfi', send_selfi_photo))
    application.add_handler(CommandHandler('school_photo', send_school_photo))
    application.add_handler(CommandHandler('hobby', hobby_audio))
    application.add_handler(CommandHandler('help', help_command))

    # messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_message))
    application.add_handler(MessageHandler(filters.VOICE & ~filters.COMMAND, handle_voice))

    # buttons
    application.add_handler(CallbackQueryHandler(button))

    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    application.run_polling()
