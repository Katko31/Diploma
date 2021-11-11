from aiogram.utils.callback_data import CallbackData

first_seven_articles_callback = CallbackData("first", "keywords")

set_time_callback = CallbackData("time", "keywords")

set_journal_callback = CallbackData("journal", "keywords")

# get_url_callback = CallbackData("url", "article_id")

get_gost_callback = CallbackData("gost", "article_id")
