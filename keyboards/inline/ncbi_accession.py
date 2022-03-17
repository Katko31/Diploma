from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.callback_datas import accession_callback, cancel_callback


def accession_buttons(accession):
    button = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Получить фаста файл с последовательностью",
                                 callback_data=accession_callback.new(accession=accession)),
        ],
        [
            InlineKeyboardButton(text="Придумать что-нибудь еще",
                                 callback_data=cancel_callback.new()),
        ],
    ])
    return button