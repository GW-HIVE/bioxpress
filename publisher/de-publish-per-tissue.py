"""
This script takes the output from running DESeq in the previous step for each tissue and combines
it into one master file.

Input:
########
All inputs are currently hard-coded
    * disease ontology mapping file (~line 37)
    * uniprot accession ID (protein ID) mapping file (~line 57)
    * refseq mapping file (~line 72)
    * list of tissues to include in the final output (~line 83)
    * folder containing all deseq output (~line 105)
    * path to write the output (~line 172)

Usage: 
########
Currently no options available
"""

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

    tissue2studylist = {}
    studyid2tissueid = {}
    in_file = "/data/projects/bioxpress/v-5.0/generated/misc/tissues.csv"
    data_frame = {}
    csvutil.load_sheet(data_frame,in_file, ",")
    for row in data_frame["data"]:
        tissue_id = row[0]
        if tissue_id[0] == "#":
            tissue_id = tissue_id[1:]
        study_id = row[1]
        if tissue_id not in tissue2studylist:
            tissue2studylist[tissue_id] = []
        tissue2studylist[tissue_id].append(study_id)
        studyid2tissueid[study_id]  = tissue_id
    tissue_list = tissue2studylist.keys()



    do_dict = {}
    protein_info = {}
    ac2genename = {}

    in_file = "/data/projects/bioxpress/v-5.0/downloads/do/domap.csv"
    data_frame = {}
    csvutil.load_sheet(data_frame,in_file, ",")
    f_list = data_frame["fields"]
    for row in data_frame["data"]:
        study_id = row[f_list.index("study_id")]
        tissue_id = studyid2tissueid[study_id]
        do_id = row[f_list.index("do_id")]
        do_name = row[f_list.index("do_name")]
        uberon_id = row[f_list.index("uberon_id")]
        uberon_name = row[f_list.index("uberon_name")]
        o = {"doid":do_id, "doname":do_name, "uberonid":uberon_id, "uberonname":uberon_name}
        do_dict[tissue_id] = o


    in_file = "/data/projects/bioxpress/v-5.0/downloads/uniprotkb/human_protein_idmapping.csv"
    data_frame = {}
    csvutil.load_sheet(data_frame,in_file, ",")
    f_list = data_frame["fields"]
    for row in data_frame["data"]:
        ac = row[f_list.index("uniprotkb_canonical_ac")].split("-")[0]
        gene_name = row[f_list.index("gene_name")]
        ac2genename[ac] = gene_name
        if gene_name not in protein_info:
            protein_info[gene_name] = {"ac":ac}
    
    in_file = "/data/projects/bioxpress/v-5.0/downloads/uniprotkb/human_protein_xref_refseq.csv"
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
    sbj_count_total = {}
    deseq_dir = "/data/projects/bioxpress/v-5.0/generated/deseq/"
    
    # Gather subject counts total by checking for log file per case 
    #for tissue_id in tissue_list:
        #for study_id in tissue2studylist[tissue_id]:
            #pattern = deseq_dir + "per_case/%s.*/*.log" % (study_id)
            #file_list = glob.glob(pattern)
            #i = 0
            #for in_file in file_list:
                #i += 1
                #if i%10 == 0:
                #    print "%s of %s cases for %s-%s " % (i, len(file_list),study_id,tissue_id)
                #case_id = in_file.split("/")[-2].split(".")[1]
        
                #if tissue_id not in sbj_count_total:
                #    sbj_count_total[tissue_id] = 0
                #sbj_count_total[tissue_id] += 1


    #for tissue_id in tissue_list:
        #for study_id in tissue2studylist[tissue_id]:
            #pattern = deseq_dir + "per_case/%s.*/results_significance.csv" % (study_id)
            #file_list = glob.glob(pattern)
            #i = 0
            #for in_file in file_list:
                #i += 1
                #if i%10 == 0:
                    #print "%s of %s cases for %s-%s " % (i, len(file_list),study_id,tissue_id)
                #case_id = in_file.split("/")[-2].split(".")[1]

                # Removed because error in DESEQ will not generate a results file for all cases
                # The error create an incorrect total subject count 
                #if tissue_id not in sbj_count_total:
                #    sbj_count_total[tissue_id] = 0
                #sbj_count_total[tissue_id] += 1

                #data_frame = {}
                #csvutil.load_sheet(data_frame,in_file, ",")
                #f_list = data_frame["fields"]
                #for row in data_frame["data"]:
                    #gene_name = row[0]
                    #if gene_name not in sbj_count:
                        #sbj_count[gene_name] = {}
                    #if tissue_id not in sbj_count[gene_name]:
                        #obj = {"up":0, "down":0, "nochange":0, "nocoverage":0}
                        #sbj_count[gene_name][tissue_id] = obj
                
                    #if row[f_list.index("log2FoldChange")] == "NA":
                        #flag = "nocoverage"
                    #else:
                        #log2fc = float(row[f_list.index("log2FoldChange")])
                        #flag = "nochange"
                        #flag = "up" if log2fc >= upper_limit else flag
                        #flag = "down" if log2fc <= lower_limit else flag
                    #sbj_count[gene_name][tissue_id][flag] += 1

    
    #newrow = ["uniprot_ac","refseq_ac","gene_name","log2fc","pvalue",
        #"adjpvalue","significance","direction","subjects_up","subjects_down", "subjects_nochange",
        #"subjects_nocoverage","subjects_total","data_source",
        #"cancer_type","doid","doname","uberon_id"
    #]
    newrow = ["uniprot_ac","refseq_ac","gene_name","log2fc","pvalue",
        "adjpvalue","significance","direction","data_source",
        "cancer_type","doid","doname","uberon_id"
    ]

    FW1 = open("/data/projects/bioxpress/v-5.0/generated/publisher/de_per_tissue.csv", "w")
    FW1.write("\"%s\"\n" % ("\",\"".join(newrow) )) 

    for tissue_id in tissue_list:
        in_file = deseq_dir + "per_tissue/%s/results_significance.csv" % (tissue_id)
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
            #if gene_name not in sbj_count:
                #continue
            #if tissue_id not in sbj_count[gene_name]:
                #continue

            significance = "Yes" if float(padj) <= padj_cutoff else "No"
            
            direction = "up" if float(log2fc) > 0.0 else "down"
            #subjects_up = sbj_count[gene_name][tissue_id]["up"]
            #subjects_down = sbj_count[gene_name][tissue_id]["down"]
            #subjects_nochange = sbj_count[gene_name][tissue_id]["nochange"]
            #subjects_nocoverage = sbj_count[gene_name][tissue_id]["nocoverage"]
            subjects_total = sbj_count_total[tissue_id]

            ds = "TCGA"
            do_id = do_dict[tissue_id]["doid"]
            do_name = do_dict[tissue_id]["doname"]
            uberon_id = do_dict[tissue_id]["uberonid"]
            cancer_type = "%s cancer" % (tissue_id)
            newrow = [ac,refseq_ac,gene_name,log2fc,pvalue,padj,significance,direction]
            #newrow += [str(subjects_up), str(subjects_down),str(subjects_nochange),
                        #str(subjects_nocoverage), str(subjects_total)]
            newrow += [str(subjects_total)]
            newrow += [ds,cancer_type, do_id, do_name, uberon_id]
            

            FW1.write("\"%s\"\n" % ("\",\"".join(newrow) ))
    
    FW1.close()



if __name__ == '__main__':
    main()


