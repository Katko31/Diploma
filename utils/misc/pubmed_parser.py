import logging

from Bio import Entrez
from Bio import Medline
from data.config import EMAIL, ARTICLES_NUMBER
from .url_article import create_doi_link_to_article
from aiogram.utils.markdown import hbold, hitalic
import html

Entrez.email = EMAIL
articles_number = ARTICLES_NUMBER


def get_article_id(keywords: str, exception_list=None, journal_name=None, author_name=None):
    logging.info(f"{keywords=}")

    if keywords and journal_name is None and author_name is None:
        query = keywords #+ '[keyword]'
    elif keywords and journal_name and author_name is None:
        # query = keywords + '[keyword]' + ' AND ' + journal_name + '[Journal]'
        query = keywords + ' AND ' + journal_name + '[Journal]'
    elif keywords and author_name and journal_name is None:
        # query = keywords + '[keyword]' + ' AND ' + author_name + '[AUTHOR]'
        query = keywords + ' AND ' + author_name + '[AUTHOR]'
    elif keywords and author_name and journal_name:
        # query = keywords + '[keyword]' + ' AND ' + author_name + '[AUTHOR]' + ' AND ' + journal_name + '[Journal]'
        query = keywords + '[keyword]' + ' AND ' + author_name + '[AUTHOR]' + ' AND ' + journal_name + '[Journal]'

    logging.info(f"{query=}")

    with Entrez.esearch(db="pubmed", term=query, usehistory='y') as handle:
        result = Entrez.read(handle)

    if exception_list is None:
        with Entrez.esummary(db='pubmed', webenv=result['WebEnv'], query_key=result['QueryKey'],
                             retmax=articles_number) as h:
            summary = Entrez.read(h)
    else:
        with Entrez.esummary(db='pubmed', webenv=result['WebEnv'], query_key=result['QueryKey'],
                             retstart=exception_list, retmax=articles_number) as h:
            summary = Entrez.read(h)

    article_id = [summary[i]['Id'] for i in range(articles_number)]
    return article_id


def get_article_info(article_id):
    with Entrez.efetch(db="pubmed", id=article_id, retmode="text", rettype="medLine") as handle:
        rt = Medline.read(handle)

        doi = create_doi_link_to_article(rt)

        if 'AB' in rt:
            reply = hbold('TITLE: ') + html.escape(rt['TI']) + '\n' + hbold('ABSTRACT: ') + \
                    hitalic(html.escape(rt['AB'])) + '\n' + html.escape(rt['SO']) + '\n' + '\n'
        else:
            reply = hbold('TITLE: ') + html.escape(rt['TI']) + '\n' + hbold('ABSTRACT: ') + '\n' + rt[
                'SO'] + '\n' + '\n'

    return reply, doi
