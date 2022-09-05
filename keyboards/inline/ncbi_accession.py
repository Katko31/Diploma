from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.callback_datas import accession_callback, cancel_callback


def accession_buttons(accession):
    button = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Retrieve FASTA file with desired sequence",
                                 callback_data=accession_callback.new(accession=accession)),
        ],
    ])
    return button
