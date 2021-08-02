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


    in_file = "downloads/do/domap.csv"
    data_frame = {}
    csvutil.load_sheet(data_frame,in_file, ",")
    f_list = data_frame["fields"]
    for row in data_frame["data"]:
        study_id = row[f_list.index("study_id")]
        do_id = row[f_list.index("do_id")]
        do_name = row[f_list.index("do_name")]
        uberon_id = row[f_list.index("uberon_id")]
        uberon_name = row[f_list.index("uberon_name")]
        o = {"doid":do_id, "doname":do_name, "uberonid":uberon_id, "uberonname":uberon_name}
        do_dict[study_id] = o

    in_file = "downloads/uniprotkb/human_protein_idmapping.csv"
    data_frame = {}
    csvutil.load_sheet(data_frame,in_file, ",")
    f_list = data_frame["fields"]
    for row in data_frame["data"]:
        ac = row[f_list.index("uniprotkb_canonical_ac")].split("-")[0]
        gene_name = row[f_list.index("gene_name")]
        ac2genename[ac] = gene_name
        if gene_name not in protein_info:
            protein_info[gene_name] = {"ac":ac}
    
    in_file = "downloads/uniprotkb/human_protein_xref_refseq.csv"
    data_frame = {}
    csvutil.load_sheet(data_frame,in_file, ",")
    f_list = data_frame["fields"]
    for row in data_frame["data"]:
        ac = row[f_list.index("uniprotkb_canonical_ac")].split("-")[0]
        gene_name = ac2genename[ac] if ac in ac2genename else ""
        refseq_ac = row[f_list.index("database_id")]
        if gene_name not in protein_info:
            protein_info[gene_name] = {"refseqac":refseq_ac}
        else:
            protein_info[gene_name]["refseqac"] = refseq_ac


    padj_cutoff = 0.05
    log2fc_cutoff = 0.5
    upper_limit = log2fc_cutoff
    lower_limit = -1.0*log2fc_cutoff


    sbj_count = {}
    file_list = glob.glob("generated/deseq/per_case/*/results_significance.csv")
    i = 0
    for in_file in file_list:
        i += 1
        if i%10 == 0:
            print "%s of %s per_case files processed" % (i, len(file_list))
        study_id = in_file.split("/")[-2].split(".")[0]
        case_id = in_file.split("/")[-2].split(".")[1]
        data_frame = {}
        csvutil.load_sheet(data_frame,in_file, ",")
        f_list = data_frame["fields"]
        for row in data_frame["data"]:
            if row[f_list.index("log2FoldChange")] == "NA":
                continue
            gene_name = row[0]
            log2fc = float(row[f_list.index("log2FoldChange")])
            if study_id not in sbj_count:
                sbj_count[study_id] = {}
            if gene_name not in sbj_count:
                sbj_count[gene_name] = {}
            if study_id not in sbj_count[gene_name]:
                sbj_count[gene_name][study_id] = {"up":0, "down":0, "nochange":0, "total":0}
            sbj_count[gene_name][study_id]["total"] += 1
            flag = "nochange"
            flag = "up" if log2fc >= upper_limit else flag
            flag = "down" if log2fc <= lower_limit else flag
            sbj_count[gene_name][study_id][flag] += 1


    newrow = ["uniprot_ac","refseq_ac","gene_name","log2fc","pvalue",
        "adjpvalue","significance","direction","subjects_up","subjects_down", "subjects_nochange",
        "subjects_total","data_source",
        "study_id","pmid","doid","doname","uberon_id"
    ]
    FW1 = open("generated/publisher/bioxpress-final.de.csv", "w")
    FW1.write("\"%s\"\n" % ("\",\"".join(newrow) )) 

    for study_id in do_dict:
        in_file = "generated/deseq/per_study/%s/results_significance.csv" % (study_id)
        data_frame = {}
        csvutil.load_sheet(data_frame,in_file, ",")
        f_list = data_frame["fields"]
        for row in data_frame["data"]:
            gene_name = row[0]
            ac, refseq_ac = "", ""
            if gene_name in protein_info:
                ac = protein_info[gene_name]["ac"] if "ac" in protein_info[gene_name] else ""
                refseq_ac = protein_info[gene_name]["refseqac"] if "refseqac" in protein_info[gene_name] else ""
            pvalue = row[f_list.index("pvalue")]
            padj = row[f_list.index("padj")]
            log2fc = row[f_list.index("log2FoldChange")]
            if padj in ["NA"]:
                continue
            if log2fc in ["NA"]:
                continue
            if gene_name not in sbj_count:
                continue
            if study_id not in sbj_count[gene_name]:
                continue

            significance = "Yes" if float(padj) <= padj_cutoff else "No"

            direction = "up" if float(log2fc) > 0.0 else "down"
            subjects_up = sbj_count[gene_name][study_id]["up"]
            subjects_down = sbj_count[gene_name][study_id]["down"]
            subjects_nochange = sbj_count[gene_name][study_id]["nochange"]
            subjects_total = sbj_count[gene_name][study_id]["total"]

            ds = "TCGA"
            pmid = ""
            do_id = do_dict[study_id]["doid"]
            do_name = do_dict[study_id]["doname"]
            uberon_id = do_dict[study_id]["uberonid"]
            newrow = [ac,refseq_ac,gene_name,log2fc,pvalue,padj,significance,direction]
            newrow += [str(subjects_up), str(subjects_down),str(subjects_nochange),str(subjects_total)]
            newrow += [ds,study_id, pmid,do_id, do_name, uberon_id]
            FW1.write("\"%s\"\n" % ("\",\"".join(newrow) ))
    
    FW1.close()



if __name__ == '__main__':
    main()


