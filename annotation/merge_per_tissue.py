"""
This script takes all files created by the `merge_per_study.sh`
script and merges them based on the file `tissues.csv`, which
assigns TCGA studies to specific tissues terms. 

Input:
########
All inputs are currently hard-coded
    * `in_file`: tissues.csv
    * `out_file_one`: path for 1st output file. 
    * `out_file_two`: path for 2nd output file.
    * study_id.categories
    * study_id.htseq.counts

Output: 
########
    * Read count and category files are generated for each tissue specified
    in the tissues.csv file.

Usage: 
########
Currently no options available 

"""

import os,sys
import string
import json
from optparse import OptionParser
import csv


sys.path.append('../lib/')
import csvutil



__version__="1.0"
__status__ = "Dev"



def main():


    tissue_dict = {}

    in_file = "/data/projects/bioxpress/v-5.0/generated/misc/tissues.csv"
    data_frame = {}
    csvutil.load_sheet(data_frame,in_file, ",")
    f_list = data_frame["fields"]
    for row in data_frame["data"]:
        study_id = row[f_list.index("study")]
        tissue_id = row[f_list.index("tissue")]
        if tissue_id not in tissue_dict:
            tissue_dict[tissue_id] = []
        tissue_dict[tissue_id].append(study_id)


    for tissue_id in tissue_dict:
        out_file_one = "/data/projects/bioxpress/v-5.0/generated/annotation/per_tissue/%s.htseq.counts" % (tissue_id)
        out_file_two = "/data/projects/bioxpress/v-5.0/generated/annotation/per_tissue/%s.categories" % (tissue_id)
        FW1 = open(out_file_one, "w")
        FW2 = open(out_file_two, "w")
        FW2.write("%s,%s\n" % ("id","status"))

        grid = {}
        seen = {}
        for study_id in tissue_dict[tissue_id]:
            in_file = "/data/projects/bioxpress/v-5.0/generated/annotation/per_study/%s.categories" % (study_id)
            data_frame = {}
            csvutil.load_sheet(data_frame,in_file, ",")
            f_list = data_frame["fields"]
            for row in data_frame["data"]:
                FW2.write("%s\n" % (",".join(row) ))

            in_file = "/data/projects/bioxpress/v-5.0/generated/annotation/per_study/%s.htseq.counts" % (study_id)
            data_frame = {}
            csvutil.load_sheet(data_frame,in_file, ",")
            f_list = data_frame["fields"]
            for row in data_frame["data"]:
                gene_id =  row[f_list.index("gene")]
                if gene_id not in grid:
                    grid[gene_id] = {}
                for j in xrange(1, len(f_list)):
                    f = f_list[j]
                    grid[gene_id][f] = row[j]
                    seen[f] = True
        f_list = seen.keys()
        tmp_row =  ["gene"] + f_list
        FW1.write("%s\n" % (",".join(tmp_row) ))
        for gene_id in grid:
            tmp_row = [gene_id]
            for f in f_list:
                val = grid[gene_id][f] if f in grid[gene_id] else 0
                tmp_row.append(str(val))
            FW1.write("%s\n" % (",".join(tmp_row) ))
        FW1.close()
        FW2.close()


if __name__ == '__main__':
    main()


