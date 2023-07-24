from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Audio
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler, CallbackQueryHandler
from constants import WELCOME_MESSAGE, INSTRUCTION
from moments.menu import main_menu_message, get_menu, get_inline_menu
import actions
from gtts import gTTS
from constants import SCHOOL_PHOTO, SELF_PHOTO, WELCOME_MESSAGE, HOBBY_TEXT


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    await update.message.reply_text(WELCOME_MESSAGE)
    await update.message.reply_text(main_menu_message(), reply_markup=get_menu())


# /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    await update.message.reply_text(text=INSTRUCTION,
                                    reply_markup=get_menu())


# /selfi
@actions.send_upload_photo_action
async def send_selfi_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_photo(chat_id=update.effective_chat.id,
                                 photo=SELF_PHOTO)
    await update.message.reply_text(text="Моя самая удачная фотография",
                                    reply_markup=get_menu())


# /school_photo
@actions.send_upload_photo_action
async def send_school_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_photo(chat_id=update.effective_chat.id,
                                 photo=SCHOOL_PHOTO)
    await update.message.reply_text(text="Со своими братьями. Я слева",
                                    reply_markup=get_menu())


# /hobby
@actions.send_upload_audio_action
async def hobby_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text="Пожалуйста, подождите, идет генерация войса...")
    tts = gTTS(text=HOBBY_TEXT, lang='ru', slow=False)
    audio_file = f'audio_{update.message.message_id}.mp3'
    tts.save(audio_file)
    await update.message.reply_voice(open(audio_file, 'rb'))


async def some_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text="Выбери про что ты хотел бы послушать:", reply_markup=get_inline_menu())


async def send_github(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text="https://github.com/Anvarka/TelegramProject",
                                    reply_markup=get_menu())
