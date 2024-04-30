#!/anaconda3/envs/phylo/bin/python

from amas import AMAS
import argparse
import os
from Bio import SeqIO

# Parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', metavar='alignment folder',
                    required=True, dest='alns_folder')
parser.add_argument('-f', metavar='alignment format',
                    required=True, dest='format')
parser.add_argument('-e', metavar='extension name',
                    required=True, dest='ext')
args = parser.parse_args()

# Tidy the alignment file
alns_file = os.listdir(os.path.join(os.getcwd(), args.alns_folder))
for i in alns_file:
    if i.endswith(args.ext):
        file_path = os.path.join(os.getcwd(), args.alns_folder, i)
        name = file_path.replace('.' + args.ext, '.' + args.ext + '.seqio')
        SeqIO.convert(file_path, 'fasta', name, 'fasta')

# Concatenate the alignment
aln = list()
alns_file = os.listdir(os.path.join(os.getcwd(), args.alns_folder))
for i in alns_file:
    if i.endswith('seqio'):
        path = os.path.join(os.getcwd(), args.alns_folder, i)
        aln.append(path)

alns = AMAS.MetaAlignment(in_files=aln, data_type='dna',
                          in_format=args.format, cores=1)
par_aln = alns.get_parsed_alignments()
concat = alns.get_concatenated(par_aln)
concatenated_alignments = concat[0]
concat_fasta = alns.print_fasta(concatenated_alignments)
with open(os.path.join(os.getcwd(), 'concatenation.fasta'), 'w') as out:
    out.writelines(concat_fasta)
    out.close()
SeqIO.convert('concatenation.fasta', 'fasta', 'concatenation.phy', 'phylip-relaxed')

