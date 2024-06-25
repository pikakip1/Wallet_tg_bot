from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def make_cancel_btn():
    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[KeyboardButton(text='Отмена')]])


def make_start_button():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='/menu')]], resize_keyboard=True)


def make_transaction_btn():
    types_transaction = ['Доход', 'Расход']

    row = [KeyboardButton(text=type_transaction) for type_transaction in types_transaction]
    row.append(KeyboardButton(text='Отмена'))
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


def make_menu_keyboard() -> ReplyKeyboardMarkup:
    chose_menu = ['Добавить запись', 'Баланс', 'Статистика', 'Добавить кошелек']
    cancel_button = 'Отмена'

    keyboard = [
        [KeyboardButton(text=chose_menu[0]), KeyboardButton(text=chose_menu[1]), KeyboardButton(text=chose_menu[2])],
        [KeyboardButton(text=chose_menu[3])],
        [KeyboardButton(text=cancel_button)]
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_category_inline_keyboard(categories: list[str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for category in categories:
        builder.add(InlineKeyboardButton(
            text=category,
            callback_data=f'category_{category}'
        ))

    return builder.as_markup()


def get_menu_statistic_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    categories_statistics = ['По категориям', 'Последние записи']
    for category_statistic in categories_statistics:
        builder.add(InlineKeyboardButton(
            text=category_statistic,
            callback_data=f'statistic_{category_statistic}'
        ))

    return builder.as_markup()
