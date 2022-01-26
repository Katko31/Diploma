from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.callback_datas import *


def keywords_buttons(keywords):
    button = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Первые 7 статей за этот год",
                                 callback_data=first_seven_articles_callback.new(keywords=keywords)),
        ],
        [
            InlineKeyboardButton(text="Настроить временные рамки самостоятельно",
                                 callback_data=time_callback.new(keywords=keywords)),
        ],
        [
            InlineKeyboardButton(text="Выбрать журнал",
                                 callback_data=journal_callback.new(keywords=keywords)),
        ]
    ])
    return button


def keywords_buttons_2(keywords):
    button = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Первые 7 статей за этот год",
                                 callback_data=first_seven_articles_callback.new(keywords=keywords)),
        ],
        [
            InlineKeyboardButton(text="Настроить временные рамки самостоятельно",
                                 callback_data=time_callback.new(keywords=keywords)),
        ],
    ])
    return button


def url_and_gost_buttons(article_id, url):
    button = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Получить ссылку на статью", url=url),
        ],
        [
            InlineKeyboardButton(text="Получить ссылку, оформленную по ГОСТу",
                                 callback_data=gost_callback.new(article_id=article_id)),
        ],
    ])
    return button


def agree_buttons(keywords):
    button = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Да",
                                 callback_data=first_seven_articles_callback.new(keywords=keywords)),
        ],
        [
            InlineKeyboardButton(text="Нет",
                                 callback_data=cancel_callback.new()),
        ],
    ])
    return button
