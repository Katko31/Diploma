from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.callback_datas import *


def keywords_buttons(keywords):
    button = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Retrieve 7 articles",
                                 callback_data=first_seven_articles_callback.new(keywords=keywords)),
        ],
        # [
        #     InlineKeyboardButton(text="Настроить временные рамки самостоятельно",
        #                          callback_data=time_callback.new(keywords=keywords)),
        # ],
        [
            InlineKeyboardButton(text="Set journal name",
                                 callback_data=journal_callback.new(keywords=keywords)),
        ],
        [
            InlineKeyboardButton(text="Set author's name",
                                 callback_data=author_callback.new(keywords=keywords)),
        ],
        [
            InlineKeyboardButton(text="Cancel",
                                 callback_data=cancel_callback.new()),
        ],
    ])
    return button


def keywords_buttons_2(keywords):
    button = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Первые 4 статьи за этот год",
                                 callback_data=first_seven_articles_callback.new(keywords=keywords)),
        ],
        [
            InlineKeyboardButton(text="Выбрать автора",
                                 callback_data=author_callback.new(keywords=keywords)),
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
            InlineKeyboardButton(text="Link to article", url=url),
        ],
        # [
        #     InlineKeyboardButton(text="Получить ссылку, оформленную по ГОСТу",
        #                          callback_data=gost_callback.new(article_id=article_id)),
        # ],
        [
            InlineKeyboardButton(text="Check access to sequences from the article",
                                 callback_data=check_access_to_sequences.new(article_id=article_id)),
        ],
    ])
    return button


def agree_buttons(keywords):
    button = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Yes",
                                 callback_data=first_seven_articles_callback.new(keywords=keywords)),
        ],
        [
            InlineKeyboardButton(text="No",
                                 callback_data=cancel_callback.new()),
        ],
    ])
    return button

