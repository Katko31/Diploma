import re


def create_doi_link_to_article(result):
    doi_search_pattern = 'doi:\s[0-9.a-z-\/]+' #не все нормально находит. Например вот такое 10.5603/CJ.a2021.0120. залажал
    if 'doi' in result['SO']:
        doi = (re.search(doi_search_pattern, result['SO'])).group(0).strip('doi: .')
        doi_link_to_article = f'https://doi.org/{doi}'
    else:
        doi_link_to_article = 'No DOI link'

    return doi_link_to_article