#!/usr/bin/env python

import telebot
from Bio import Entrez
import sys
from Bio import Medline
from Bio import SeqIO
from Bio.Align.Applications import ClustalwCommandline
from Bio import Phylo

TOKEN = "1792882826:AAER2czFvmc3qt7_gsH_BDOxqtI4Q3drIqc"
Entrez.email = "pardus_2000@rambler.ru"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Salve amice! Здравствуй друг! Для справки набери /help')


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, '1. Для того, чтобы получить список из 20 абстрактов введите число 1, поставьте '
                                      'пробел и введите ключевое слово или слова через пробелы.'+'\n'+'\n' +
                     'Пример команды:' + '\n' + '1 microbiota bacteria bacteriophage' + '\n' + '----------------------------------------------------'
                     + '\n' + '\n' +
                     '2. Для того, чтобы получить файл в формате fasta, введите число 2, поставьте пробел и '
                     'введите accession number искомой последовательности' + '\n' + '\n' +
                     'Пример команды:' + '\n' + '2 JX294734.1' + '\n' + '----------------------------------------------------'
                     + '\n' + '\n' +
                     '3. Для того, чтобы получить документ с построенным филогенетическим '
                     'деревом отправь мне документ в формате fasta, где сохранены твои последовательности для выравнивания' + '\n' + '\n' +
                     'Пример команды:' + '\n' + 'название_твоего_документа.fasta')


@bot.message_handler(content_types=['text', 'document'])
def handle_text_doc(message):
    if message.text:

        try:
            name = message.text
            key = name.split()[0]
            value = ' '.join(name.split()[1:])

            if key == '1':
                with Entrez.esearch(db="pubmed", term=value + '[keyword]') as handle:
                    result = Entrez.read(handle)

                id = result["IdList"]

                with open('abstract.txt', 'w') as file:
                    for i in id:
                        with Entrez.efetch(db="pubmed", id=i, retmode="text", rettype="medLine") as handle:
                            rt = Medline.read(handle)
                            
                            if 'AB' in rt:
                                reply = 'TITLE: '+rt['TI']+'\n'+'ABSTRACT: '+rt['AB']+'\n'+'SOURCE: '+rt['SO']+'\n'+'\n'
                            else:
                                continue

                        file.write(reply)

                doc1 = open('abstract.txt', 'rb')
                bot.send_document(message.chat.id, doc1)

            elif key == '2':

                with open('sequence.fasta', 'w') as file2:
                    handle = Entrez.efetch(db="nucleotide", id=value, rettype="fasta")
                    record = SeqIO.read(handle, "fasta")
                    reply = '>' + record.description + '\n' + str(record.seq)
                    file2.write(reply)

                doc2 = open('sequence.fasta', 'rb')
                bot.send_document(message.chat.id, doc2)

        except Exception as e:
            bot.reply_to(message, e)

    elif message.document:
        try:
            chat_id = message.chat.id
            message.document.file_name = 'myname.fasta'
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            src = '/home/kate/PycharmProjects/Homework/TelegramBot/.venv/' + message.document.file_name
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            
            cline = ClustalwCommandline("clustalw2", infile="/home/kate/PycharmProjects/Homework/TelegramBot/.venv/myname.fasta")
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
