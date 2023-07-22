from telegram import ReplyKeyboardMarkup


def main_menu_message():
    return 'Choose the option in main menu:'


def get_menu():
    menu = [
        ['Селфи', 'Фотка со школы'],
        ['Послушать увлечения'],
        ['Hide Menu']
    ]
    return ReplyKeyboardMarkup(menu, one_time_keyboard=True)
