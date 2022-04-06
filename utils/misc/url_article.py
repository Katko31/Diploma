from Bio import Entrez
from Bio import Medline
import re
from data.config import EMAIL
Entrez.email = EMAIL


def create_doi_link_to_article(result):
    doi_search_pattern = 'doi:\s[0-9.a-zA-Z-\/]+'
    if 'doi' in result['SO']:
        doi = (re.search(doi_search_pattern, result['SO'])).group(0).strip('doi: .')
        doi_link_to_article = f'https://doi.org/{doi}'
    else:
        doi_link_to_article = 'No DOI link'

    return doi_link_to_article


def create_gost_link(article_id):
    author_list = []

    with Entrez.efetch(db="pubmed", id=article_id, retmode="text", rettype="medLine") as handle:
        result = Medline.read(handle)

    for author in result['AU']:
        if len(result['AU']) > 2:
            surname = author.split()[0]
            initials = author.split()[1]

            if len(initials) > 1:
                author_list.append(f'{surname} {initials[0]}. {initials[1]}. et al.')

            else:
                author_list.append(f'{surname} {initials}. et al.')
            break

        else:
            surname = author.split()[0]
            initials = author.split()[1]

            if len(initials) > 1:
                author_list.append(f'{surname} {initials[0]}. {initials[1]}.')

            else:
                author_list.append(f'{surname} {initials}.')

    author_str = ", ".join(author_list)
    if 'TI' in result:
        article_name = result['TI'].rstrip('.')
    else:
        article_name = result['TT'].rstrip('.')
    journal_name = result['JT']
    year_pattern = '\s[0-9]{4}\s'
    year = (re.search(year_pattern, result['SO'])).group(0).strip()
    pages = None
    pages_pattern = ':[0-9-e]+.'
    pre_pages = re.search(pages_pattern, result['SO'])
    if pre_pages is not None:
        pages = pre_pages.group(0).strip(':.')
    tom = None
    number = None
    tom_only = None
    tom_and_number_pattern = ';[0-9()]+:'
    pre_tom_and_number = re.search(tom_and_number_pattern, result['SO'])
    if pre_tom_and_number is not None:
        tom_and_number = pre_tom_and_number.group(0).strip(';:')
        if '(' in tom_and_number:
            tom_pattern = '[0-9]+[$(]'
            tom = (re.search(tom_pattern, tom_and_number)).group(0).strip('(')
            number_pattern = '[^(]+[$)]'
            number = (re.search(number_pattern, tom_and_number)).group(0).strip(')')
        else:
            tom_only = tom_and_number

    if year and tom and number and pages:
        gost_link = f'{author_str} {article_name} //{journal_name}. - {year}. - T. {tom}. - №. {number}. - C. {pages}.\n'
    elif year and tom and number:
        gost_link = f'{author_str} {article_name} //{journal_name}. - {year}. - T. {tom}. - №. {number}.\n'
    elif year and tom_only and pages:
        gost_link = f'{author_str} {article_name} //{journal_name}. - {year}. - T. {tom_only}. - C. {pages}.\n'
    elif year and pages:
        gost_link = f'{author_str} {article_name} //{journal_name}. - {year}. - C. {pages}.\n'
    else:
        gost_link = f'{author_str} {article_name} //{journal_name}. - {year}.\n'

    return gost_link