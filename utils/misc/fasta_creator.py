from pathlib import Path
from Bio import Entrez
from Bio import SeqIO


def fasta_creator(accession, database):
    with open(f'/home/kate/PycharmProjects/Diploma_bot/utils/misc/{accession}.fasta', 'w') as file:
        handle = Entrez.efetch(db=database, id=accession, rettype="fasta")
        record = SeqIO.read(handle, "fasta")
        reply = '>' + record.description + '\n' + str(record.seq)
        file.write(reply)

    path_to_download = Path().joinpath(f'/home/kate/PycharmProjects/Diploma_bot/utils/misc/{accession}.fasta')
    return path_to_download

    # doc2 = open(f'{value}.fasta', 'rb') надо подумать, где правильно открывать документ. Тут или в хэндлере
    # pass