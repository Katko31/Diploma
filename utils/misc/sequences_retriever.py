from Bio import Entrez
from Bio import SeqIO
from data.config import PATH_TO_DOCS_FROM_NCBI


def sequences_from_article(id_article):

    spisok = []
    with Entrez.elink(dbfrom="pubmed", linkname='pubmed_nucleotide', retmax=100, id=id_article) as handle:
        rlt = Entrez.read(handle)

        if len(rlt[0]['LinkSetDb']) > 0 and len(rlt[0]['LinkSetDb'][0]['Link']) > 0: #посмотреть все линки!
            sequences_id_massiv = rlt[0]['LinkSetDb'][0]['Link']
            for number in sequences_id_massiv:
                spisok.append(number['Id'])

            path_to_fasta = f'{PATH_TO_DOCS_FROM_NCBI}/{id_article}.fasta'
            with open(path_to_fasta, 'w') as file:
                for i in spisok:
                    handle = Entrez.efetch(db="nucleotide", id=i, rettype="fasta")
                    record = SeqIO.read(handle, "fasta")
                    reply = '>' + record.description + '\n' + str(record.seq) + '\n'
                    file.write(reply)

            return path_to_fasta

        else:
            return 1
