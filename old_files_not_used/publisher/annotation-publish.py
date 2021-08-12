import os,sys
import string
import json
from optparse import OptionParser
import csv
import glob

sys.path.append('../lib/')
import csvutil



__version__="1.0"
__status__ = "Dev"



def main():


    do_dict = {}
    protein_info = {}
    ac2genename = {}

    map_file_list = [
        "downloads/ensembl/mart_export.txt",
        "downloads/ensembl/mart_export_remap_retired.txt",
        "downloads/ensembl/new_mappings.txt"
    ]

    gene_info = {"geneid":{}, "uniprotkb":{}, "refseq":{}}
    for map_file in map_file_list[0:-1]:
        data_frame = {}
        csvutil.load_sheet(data_frame,map_file, "\t")
        f_list = data_frame["fields"]
        for row in data_frame["data"]:
            gene_name = row[f_list.index("Gene name")]
            gene_id = row[f_list.index("Gene stable ID")]
            if gene_name not in gene_info["geneid"]:
                gene_info["geneid"][gene_name] = []
            gene_info["geneid"][gene_name].append(gene_id)

    
    in_file = "downloads/uniprotkb/human_protein_idmapping.csv"
    data_frame = {}
    csvutil.load_sheet(data_frame,in_file, ",")
    f_list = data_frame["fields"]
    for row in data_frame["data"]:
        ac = row[f_list.index("uniprotkb_canonical_ac")].split("-")[0]
        gene_name = row[f_list.index("gene_name")]
        if gene_name not in gene_info["uniprotkb"]:
            gene_info["uniprotkb"][gene_name] = []
        gene_info["uniprotkb"][gene_name].append(ac)


    in_file = "downloads/uniprotkb/human_protein_xref_refseq.csv"
    data_frame = {}
    csvutil.load_sheet(data_frame,in_file, ",")
    f_list = data_frame["fields"]
    uniprotkb2refseq = {}
    for row in data_frame["data"]:
        uniprotkb_ac = row[f_list.index("uniprotkb_canonical_ac")].split("-")[0]
        refseq_ac = row[f_list.index("database_id")]
        if uniprotkb_ac not in uniprotkb2refseq:
            uniprotkb2refseq[uniprotkb_ac] = []
        uniprotkb2refseq[uniprotkb_ac].append(refseq_ac)


    FW = open("generated/publisher/bioxpress-final.xref.csv", "w")
    newrow = ["gene_name", "xref_db", "xref_id"]
    FW.write("\"%s\"\n" % ("\",\"".join(newrow)))

    for gene_name in gene_info["geneid"]:
        #if len(gene_info["geneid"][gene_name]) != 1:
        #    continue
        newrow = [gene_name, "ensembl", gene_info["geneid"][gene_name][0]]
        FW.write("\"%s\"\n" % ("\",\"".join(newrow)))
        if gene_name in gene_info["uniprotkb"]:
            uniprotkb_ac = gene_info["uniprotkb"][gene_name][0]
            newrow = [gene_name, "uniprotkb", uniprotkb_ac]
            FW.write("\"%s\"\n" % ("\",\"".join(newrow)))
            if uniprotkb_ac in uniprotkb2refseq:
                refseq_ac = uniprotkb2refseq[uniprotkb_ac][0]
                newrow = [gene_name, "refseq", refseq_ac]
                FW.write("\"%s\"\n" % ("\",\"".join(newrow)))

    FW.close()


    FW = open("generated/publisher/bioxpress-final.domap.csv", "w")
    newrow = ["study_id", "do_id", "do_name", "uberon_id", "uberon_name"]
    FW.write("\"%s\"\n" % ("\",\"".join(newrow)))


    in_file = "downloads/do/domap.csv"
    data_frame = {}
    csvutil.load_sheet(data_frame,in_file, ",")
    f_list = data_frame["fields"]
    seen = {}

    for row in data_frame["data"]:
        study_id = row[f_list.index("study_id")].split("-")[1]
        do_id = row[f_list.index("do_id")]
        do_name = row[f_list.index("do_name")]
        uberon_id = row[f_list.index("uberon_id")]
        uberon_name = row[f_list.index("uberon_name")]
        if do_id not in seen:
            newrow = [study_id,do_id, do_name, uberon_id, uberon_name]

            FW.write("\"%s\"\n" % ("\",\"".join(newrow)))
            seen[do_id] = True

    FW.close()






if __name__ == '__main__':
    main()


