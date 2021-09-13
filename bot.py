#!/usr/bin/env python
"""
Написать телеграм-бот, который умеет: а) искать статьи в пабмеде, возвращает список из 20 статей с абстрактами,
можно просить загрузить еще. б) скачивать последовательности.
в) осуществлять выравнивание и построение филогении последовательностей из файла.
"""
import telebot
from Bio import Entrez
import sys
import re
from Bio import Medline
from Bio import SeqIO
from Bio.Align.Applications import ClustalwCommandline
from Bio import Phylo

TOKEN = " "
Entrez.email = "pardus_2000@rambler.ru"

bot = telebot.TeleBot(TOKEN)

def create_gost_link(result):

    author_list = []

    for author in result['AU']:
        if len(result['AU']) > 4:
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


def create_doi_link_to_article(result):
    doi_search_pattern = 'doi:\s[0-9.a-z-\/]+'
    if 'doi' in result['SO']:
        doi = (re.search(doi_search_pattern, result['SO'])).group(0).strip('doi: .')
        doi_link_to_article = f'https://doi.org/{doi}'
    else:
        doi_link_to_article = 'No DOI link'

    return doi_link_to_article


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Здравствуй друг! Для справки набери /help')


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, '1. Для того, чтобы получить список из 20 абстрактов введите число 1, поставьте '
                                      'пробел и введите ключевое слово или слова через пробелы.' + '\n' + '\n' +
                     'Пример команды:' + '\n' + '1 microbiota bacteria bacteriophage' + '\n' + '----------------------------------------------------'
                     + '\n' + '\n' +
                     '2. Для того, чтобы получить список из 20 абстрактов введите число 2, поставьте '
                     'пробел и введите фамилию автора.' + '\n' + '\n' +
                     'Пример команды:' + '\n' + '2 Hinton' + '\n' + '----------------------------------------------------'
                     + '\n' + '\n' +
                     '3. Для того, чтобы получить файл в формате fasta с последовательностью из базы данных "nucleotide", введите число 3, поставьте пробел и '
                     'введите accession number искомой последовательности' + '\n' + '\n' +
                     'Пример команды:' + '\n' + '3 JX294734.1' + '\n' + '----------------------------------------------------'
                     + '\n' + '\n' +
                     '4. Для того, чтобы получить файл в формате fasta с последовательностью из базы данных "protein", введите число 4, поставьте пробел и '
                     'введите accession number искомой последовательности' + '\n' + '\n' +
                     'Пример команды:' + '\n' + '4 AAA59172.1' + '\n' + '----------------------------------------------------'
                     + '\n' + '\n' +
                     '5. Для того, чтобы получить документ с построенным филогенетическим '
                     'деревом отправь мне документ в формате fasta, где сохранены ваши последовательности для выравнивания' + '\n' + '\n' +
                     'Пример команды:' + '\n' + 'название_твоего_документа.fasta')


@bot.message_handler(content_types=['text', 'document'])
def handle_text_doc(message):
    if message.text:

        try:
            name = message.text
            key = name.split()[0]
            value = ' '.join(name.split()[1:])

            if key == '1' or key == '2':
                if key == '1':
                    with Entrez.esearch(db="pubmed", term=value + '[keyword]') as handle:
                        result = Entrez.read(handle)
                else:
                    with Entrez.esearch(db="pubmed", term=value + "[AUTHOR]") as handle:
                        result = Entrez.read(handle)

                id = result["IdList"]

                with open(f'{value}.txt', 'w') as file:
                    for i in id:
                        with Entrez.efetch(db="pubmed", id=i, retmode="text", rettype="medLine") as handle:
                            rt = Medline.read(handle)

                            if 'AB' in rt:
                                # gost = create_gost_link(rt)
                                doi = create_doi_link_to_article(rt)
                                reply = 'TITLE: ' + rt['TI'] + '\n' + 'ABSTRACT: ' + rt['AB'] + '\n' + rt['SO'] + '\n' + doi + '\n' + '\n'
                            else:
                                continue

                        file.write(reply)

                doc1 = open(f'{value}.txt', 'rb')
                bot.send_document(message.chat.id, doc1)

            elif key == '3' or key == '4':

                with open(f'{value}.fasta', 'w') as file2:
                    if key == '3':
                        handle = Entrez.efetch(db="nucleotide", id=value, rettype="fasta")
                    else:
                        handle = Entrez.efetch(db="protein", id=value, rettype="fasta")
                    record = SeqIO.read(handle, "fasta")
                    reply = '>' + record.description + '\n' + str(record.seq)
                    file2.write(reply)

                doc2 = open(f'{value}.fasta', 'rb')
                bot.send_document(message.chat.id, doc2)

        except Exception as e:
            bot.reply_to(message, e)


    elif message.document:
        try:
            # chat_id = message.chat.id
            message.document.file_name = 'myname.fasta'
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            src = '/home/kate/PycharmProjects/Homework/TelegramBot/.venv/' + message.document.file_name
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)

            cline = ClustalwCommandline("clustalw2",
                                        infile="/home/kate/PycharmProjects/Homework/TelegramBot/.venv/myname.fasta")
            cline()

            with open("tree.txt", "w") as f:
                sys.stdout = f

                tree = Phylo.read("/home/kate/PycharmProjects/Homework/TelegramBot/.venv/myname.dnd", "newick")
                Phylo.draw_ascii(tree)

                sys.stdout.close()

            doc = open('tree.txt', 'rb')
            bot.send_document(message.chat.id, doc)

        except Exception as e:
            bot.reply_to(message, e)


bot.polling()
