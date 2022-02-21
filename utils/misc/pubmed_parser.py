import logging

from Bio import Entrez
from Bio import Medline
from data.config import EMAIL, ARTICLES_NUMBER
from .url_article import create_doi_link_to_article
from aiogram.utils.markdown import hbold, hitalic
# import inspect
import html

Entrez.email = EMAIL
articles_number = ARTICLES_NUMBER


def get_article_id(keywords: str, exception_list=None, journal_name=None, author_name=None):
    logging.info(f"{keywords=}")
    # inspect.signature(get_article_id)

    if keywords and journal_name is None and author_name is None:
        query = keywords + '[keyword]'
    elif keywords and journal_name and author_name is None:
        query = keywords + '[keyword]' + ' AND ' + journal_name + '[Journal]'
    elif keywords and author_name and journal_name is None:
        query = keywords + '[keyword]' + ' AND ' + author_name + '[AUTHOR]'
    else:
        query = keywords + '[keyword]' + ' AND ' + author_name + '[AUTHOR]' + ' AND ' + journal_name + '[Journal]'

    if exception_list is None:
        with Entrez.esearch(db="pubmed", term=query, retmax=articles_number) as handle:
            result = Entrez.read(handle)
    else:
        with Entrez.esearch(db="pubmed", term=query, retstart=articles_number + len(exception_list),
                            retmax=articles_number + 2 * len(exception_list)) as handle:
            result = Entrez.read(handle)

    article_id = result["IdList"]
    return article_id

    # if exception_list:
    #     with Entrez.esearch(db="pubmed", term=keywords + '[keyword]', retmax=3, retstart=len(exception_list)) as handle:
    #         result = Entrez.read(handle)
    # else:
    #     with Entrez.esearch(db="pubmed", term=keywords + '[keyword]', retmax=3) as handle:
    #         result = Entrez.read(handle)
    #
    # article_id = result["IdList"]
    # return article_id


def get_article_info(article_id):
    with Entrez.efetch(db="pubmed", id=article_id, retmode="text", rettype="medLine") as handle:
        rt = Medline.read(handle)

        doi = create_doi_link_to_article(rt) #отдельно бы эту функцию прописать! сохранить отдельно rt

        if 'AB' in rt:
            reply = hbold('TITLE: ') + html.escape(rt['TI']) + '\n' + hbold('ABSTRACT: ') + \
                    hitalic(html.escape(rt['AB'])) + '\n' + html.escape(rt['SO']) + '\n' + '\n'
        else:
            reply = hbold('TITLE: ') + html.escape(rt['TI']) + '\n' + hbold('ABSTRACT: ') + '\n' + rt[
                'SO'] + '\n' + '\n'

    return reply, doi
