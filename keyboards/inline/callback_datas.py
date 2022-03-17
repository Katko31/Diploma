from aiogram.utils.callback_data import CallbackData

first_seven_articles_callback = CallbackData("default", "keywords")

# articles_journal_callback = CallbackData("default", "keywords", "journal_name")

time_callback = CallbackData("time", "keywords")

journal_callback = CallbackData("journal", "keywords")

author_callback = CallbackData("author", "keywords")

# get_url_callback = CallbackData("url", "article_id")

gost_callback = CallbackData("gost", "article_id")

cancel_callback = CallbackData("no")

accession_callback = CallbackData("acc", "accession")


