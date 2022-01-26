from loader import dp, bot
import logging
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery, ParseMode
from aiogram.dispatcher.storage import FSMContext
from utils.misc.pubmed_parser import *
from keyboards.inline.pubmed_keywords import *


@dp.message_handler(state='enter_keywords')
async def show_pubmed_items(message: types.Message, state: FSMContext):
    name = message.text
    await message.answer(text=f"{name}", reply_markup=keywords_buttons(name))

    await state.reset_state()


@dp.message_handler(Command("keywords"))
async def find_keywords_article(message: Message, state: FSMContext):
    await message.answer('Введите ключевое слово или слова через пробел для поиска статей')
    await state.set_state('enter_keywords')


# @dp.callback_query_handler(text_contains="default")
@dp.callback_query_handler(first_seven_articles_callback.filter())
async def show_first_seven_articles(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    logging.info(f" Что в колбэк{call.data=}")
    # keywords = list(call.data.split(":"))[1]
    keywords = callback_data.get("keywords")
    journal_name = None
    exception_list = None

    try:
        async with state.proxy() as data:
            journal_name = data['journal_name']
            # exception_list = data['exception_id_list'] #возможно надо разобщить
    except KeyError:
        print('dfjdk')

    try:
        async with state.proxy() as data:
            exception_list = data['exception_id_list']
    except KeyError:
        print('dfjdk')

    logging.info(f"{keywords=}")
    logging.info(f"{journal_name=}")
    logging.info(f"{exception_list=}")
    logging.info(f" Что отображается в хэндлере первых семи статей {journal_name}")
    # logging.info(f" Что же все-таки лежит в дэйта {dat=}")

    if journal_name is None and exception_list is None:
        article_id = get_article_id(keywords)
    elif journal_name is None and exception_list:
        article_id = get_article_id(keywords, exception_list)
    elif journal_name:
        article_id = get_articles_by_journal(keywords, journal_name)

    logging.info(f" Айдишники журналов {type(article_id)}")

    for i in article_id:
        logging.info(f" Тип ай {type(i)}")
        logging.info(f" Тип ай {i=}")
        info, url = get_article_info(i)
        # url = None
        logging.info(f"{info=}")
        logging.info(f"{url=}")
        await bot.send_message(chat_id=call.from_user.id,
                               text=info,
                               parse_mode=ParseMode.HTML, #еще одно гавно которое работает от раза к разу.
                               # Что-то парсится через маркдаун, а что-то только через хтмл, надо что-то делать
                               reply_markup=url_and_gost_buttons(i, url))

    async with state.proxy() as data: #надо добавить проверку, если data['exception_id_list'] уже существует
        # data['exception_id_list'] = article_id #вот так не работает, а код ниже работает
        data['exception_id_list'] = [str(i) for i in article_id]

    await bot.send_message(chat_id=call.from_user.id,
                           text='Продолжить поиск новых статей с заданными параметрами?',
                           reply_markup=agree_buttons(keywords))
    await state.reset_state(with_data=False)


@dp.message_handler(state='enter_journal')
async def articles_and_journal(message: types.Message, state: FSMContext):
    # journal_name = message.text
    async with state.proxy() as data:
        keywords = data['key']
        # data['article_by_journal'] = get_articles_by_journal(keywords, journal_name)
        data['journal_name'] = message.text
    logging.info(f"Проверка, что сохранилось на этапе введения журнала {data['journal_name']}")

    await message.answer(text=f"Ключевые слова для поиска: {keywords} в журнале: {data['journal_name']}",
                         reply_markup=keywords_buttons_2(keywords))

    await state.reset_state(with_data=False)


@dp.callback_query_handler(journal_callback.filter())
async def set_journal_name(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    async with state.proxy() as data:
        data['key'] = callback_data.get("keywords")
    # keywords = callback_data.get("keywords")
    logging.info(f"{data['key']}")
    await bot.send_message(chat_id=call.from_user.id, text="Введите название журнала", reply_markup=None)
    await state.set_state('enter_journal')


@dp.callback_query_handler(cancel_callback.filter())
async def reset_proxy(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await bot.send_message(chat_id=call.from_user.id, text="Спасибо за обращение, надеемся было полезно ",
                           reply_markup=None)
    await state.reset_state()
