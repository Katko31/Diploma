from pathlib import Path
from Bio import Entrez
from Bio import SeqIO
from io import BytesIO
from data.config import PATH_TO_DOCS_FROM_NCBI


def fasta_creator(accession, database):
    with open(f'{PATH_TO_DOCS_FROM_NCBI}{accession}.fasta', 'w') as file:
        handle = Entrez.efetch(db=database, id=accession, rettype="fasta")
        record = SeqIO.read(handle, "fasta")
        reply = '>' + record.description + '\n' + str(record.seq)
        file.write(reply)

    path_to_download = Path().joinpath(f'{PATH_TO_DOCS_FROM_NCBI}{accession}.fasta')
    return path_to_download

#
# def fasta_creator(accession, database):
#     with Entrez.efetch(db=database, id=accession, rettype="fasta") as handle:
#         record = SeqIO.read(handle, "fasta")
#         reply = '>' + record.description + '\n' + str(record.seq)
