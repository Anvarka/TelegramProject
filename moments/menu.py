from telegram import ReplyKeyboardMarkup
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Audio


def main_menu_message():
    return 'Choose the option in main menu:'


def get_menu():
    menu = [
        ['Селфи', 'Фотка со школы'],
        ['Послушать увлечение', 'Рассказы'],
        ['Hide Menu']
    ]
    return ReplyKeyboardMarkup(menu, one_time_keyboard=True)


def get_inline_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("Отличие SQL/NoSQL", callback_data='sql'),
            InlineKeyboardButton("Что такое GPT", callback_data='gpt'),
            InlineKeyboardButton("Love story", callback_data='love'),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

