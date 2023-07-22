import actions
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Audio
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler, CallbackQueryHandler
from gtts import gTTS
from constants import SCHOOL_PHOTO, SELF_PHOTO, WELCOME_MESSAGE, HOBBY_TEXT
from pydub import AudioSegment
import os
import whisper

model = whisper.load_model("base")


# увлечение
@actions.send_upload_audio_action
async def send_hobby_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tts = gTTS(text=HOBBY_TEXT, lang='ru', slow=False)
    audio_file = f'audio_{update.message.message_id}.mp3'
    tts.save(audio_file)
    await update.message.reply_voice(open(audio_file, 'rb'))


# распознавание речи
@actions.send_upload_audio_action
async def handle_voice_recognition(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_id = update.message.voice.file_id
    file = await context.bot.get_file(file_id)

    path = os.path.abspath(f'/home/anvar/IdeaProjects/TelegramProject/voice_{file_id}.ogg')
    await file.download_to_drive(path)

    audio = AudioSegment.from_file(path, format='ogg')
    audio.export(f'/home/anvar/IdeaProjects/TelegramProject/voice_{file_id}.wav', format='wav')

    # Recognize speech from the downloaded voice message
    transcriptions = model.transcribe(f'/home/anvar/IdeaProjects/TelegramProject/voice_{file_id}.wav')
    await update.message.reply_text(f"Recognized text: {transcriptions['text']}")


