import logging

from Bio import Entrez
from Bio import Medline
from data.config import EMAIL
from .url_article import create_doi_link_to_article

Entrez.email = EMAIL


def get_article_id(keywords: str, exception_list=None):
    logging.info(f"{keywords=}")
    if exception_list:
        with Entrez.esearch(db="pubmed", term=keywords + '[keyword]', retmax=3, retstart=len(exception_list)) as handle:
            result = Entrez.read(handle)
    else:
        with Entrez.esearch(db="pubmed", term=keywords + '[keyword]', retmax=3) as handle:
            result = Entrez.read(handle)

    article_id = result["IdList"]
    return article_id


def get_article_info(article_id):
    with Entrez.efetch(db="pubmed", id=article_id, retmode="text", rettype="medLine") as handle:
        rt = Medline.read(handle)

        doi = create_doi_link_to_article(rt) #отдельно бы эту функцию прописать! сохранить отдельно rt

        if 'AB' in rt:
            reply = 'TITLE: ' + rt['TI'] + '\n' + 'ABSTRACT: ' + rt['AB'] + '\n' + rt[
                'SO'] + '\n' + '\n'
        else:
            reply = 'TITLE: ' + rt['TI'] + '\n' + 'ABSTRACT: ' + '\n' + rt[
                'SO'] + '\n' + '\n'

    return reply, doi


def get_articles_by_journal(keywords: str, journal_name: str):
    logging.info(f"{keywords=}")
    with Entrez.esearch(db="pubmed", term=keywords + '[keyword]' + ' AND ' + journal_name + '[Journal]', retmax=3) as handle:
        result = Entrez.read(handle)

    article_id = result["IdList"]
    return article_id

