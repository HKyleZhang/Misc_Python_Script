#!/anaconda3/envs/phylo/bin/python

from amas import AMAS
import os
import argparse

# Parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', metavar='alignment folder',
                    required=True, dest='alns_folder')
parser.add_argument('-f', metavar='alignment format',
                    required=True, dest='format')
parser.add_argument('-e', metavar='alignment extension',
                    required=True, dest='ext')
args = parser.parse_args()

alns_file = os.listdir(os.path.join(os.getcwd(), args.alns_folder))
alns_file_list = list()
for i in alns_file:
    if i.endswith(args.ext):
        file_path = os.path.join(os.getcwd(), args.alns_folder, i)
        alns_file_list.append(file_path)

alns = AMAS.MetaAlignment(
    in_files=alns_file_list, data_type='dna', in_format=args.format, cores=1)

summary = alns.get_summaries()
output_list = list()
for i in range(len(alns_file_list)):
    gene_name = summary[1][i][0]
    length = summary[1][i][2]
    output_item = gene_name + ' ' + length + '\n'
    output_list.append(output_item)

with open(os.path.join(os.getcwd(), 'alignment_length.txt'), 'w') as out:
    out.writelines(output_list)
    out.close
