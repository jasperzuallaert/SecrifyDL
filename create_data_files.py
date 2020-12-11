from random import shuffle, seed
import sys
import os

seed(1337)
MIN_LENGTH = 50

output_dir = 'data/'
pos_file_pp = 'initial_data/Pp_resultstable_enriched.txt'
neg_file_pp = 'initial_data/Pp_resultstable_depleted.txt'
pos_file_sc = 'initial_data/Sc_resultstable_enriched.txt'
neg_file_sc = 'initial_data/Sc_resultstable_depleted.txt'
filenames = [pos_file_pp, neg_file_pp, pos_file_sc, neg_file_sc]
label_per_file = [1,0,1,0]
# pp_pos_proteins = []
# pp_neg_proteins = []
# sc_pos_proteins = []
# sc_neg_proteins = []
# protein_lists = [pp_pos_proteins, pp_neg_proteins, sc_pos_proteins, sc_neg_proteins]
pp_gene_id_to_proteins = {}
sc_gene_id_to_proteins = {}
gene_dicts = [pp_gene_id_to_proteins, sc_gene_id_to_proteins]


class Record:
    def __init__(self, id, sequence, label):
        self.id = id
        self.sequence = sequence
        self.label = label

gene_id_to_proteins = {}
for filename, label_for_file in zip(filenames, label_per_file):
# for filename, label_for_file, protein_list in zip(filenames, label_per_file, protein_lists):
    for i,line in enumerate(open(filename).readlines()[1:]):
        line = line.split('\t')
        id = line[0]
        gene_id = line[1]
        seq = line[10]
        if len(seq) >= MIN_LENGTH:
            # protein_list.append(id)
            # protein_list.append(id)
            gene_dicts[i//2][gene_id] = gene_dicts[i//2].setdefault(gene_id,set())|{Record(id,seq,label_for_file)}

pp_gene_ids = list(pp_gene_id_to_proteins.keys())
sc_gene_ids = list(sc_gene_id_to_proteins.keys())
shuffle(pp_gene_ids)
shuffle(sc_gene_ids)

for k in range(10):
    out_f = open(output_dir+f'pp_{k}.dat','w')
    gene_ids = pp_gene_ids[(k*len(pp_gene_ids))//10:((k+1)*len(pp_gene_ids))//10]
    for gene_id in gene_ids:
        proteins = gene_id_to_proteins[gene_id]
        for protein in proteins:
            print(f'{protein.id},{protein.sequence},{protein.label}',file=out_f)

for k in range(10):
    out_f = open(output_dir+f'sc_{k}.dat','w')
    gene_ids = sc_gene_ids[(k*len(sc_gene_ids))//10:((k+1)*len(sc_gene_ids))//10]
    for gene_id in gene_ids:
        proteins = gene_id_to_proteins[gene_id]
        for protein in proteins:
            print(f'{protein.id},{protein.sequence},{protein.label}',file=out_f)
