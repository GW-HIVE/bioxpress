import requests
import json
import re
import csv
import os 
import sys

collector = {}

inputFile = sys.argv[1]
primary_site = []
rowcount=0
with open(inputFile) as csvfile:
    csvreader = csv.reader(csvfile, delimiter="\t", quotechar='"')
    for row in csvreader:
        rowcount +=1
        if rowcount ==1:
            continue
        else:
           #File ID File Name       Data Category   Data Type       Project ID      Case ID Sample ID       Sample Type
           #558c4654-1be9-4eb2-9322-af29c48035ad    026527d4-007c-4c4e-9bd5-855c44bbe7b0.htseq.counts.gz    Transcriptome Profiling Gene Expression Quantification  TCGA-GBM        TCGA-06-0681    TCGA-06-0681-11A      Solid Tissue Normal
 
            fil_id   = row[0]
            proj_id  = row[4]
            sam_type = row[7].replace(" ","-")

            #update collector data object 
            if not(proj_id in collector):
                collector[proj_id] = {}
            if not(sam_type in collector[proj_id]):
                collector[proj_id][sam_type] = []
           
            #add id
            collector[proj_id][sam_type].append(fil_id)
            




#download everything!
files_endpt = "https://api.gdc.cancer.gov/files"
data_endpt = "https://api.gdc.cancer.gov/data"

path0 = "/home/bfochtman/bioXpress/download/files_tcga/"
for proj_id in collector:
    path1 = os.path.join(path0,proj_id)
    if not(os.path.exists(path1)):
        os.mkdir(path1)
    for sam_type in collector[proj_id]:
        path2 = os.path.join(path1,sam_type)
        if not(os.path.exists(path2)):
            os.mkdir(path2)

        fil_list = collector[proj_id][sam_type]
        uniq_fil_list = list(set(fil_list))


        print proj_id, sam_type, len(fil_list), len(uniq_fil_list)  
        params = {"ids": uniq_fil_list}

        response = requests.post(data_endpt, data = json.dumps(params), headers = {"Content-Type":"application/json"})

        file_name = path2+"/results.tar.gz"

        with open(file_name, "wb") as output_file:
            output_file.write(response.content)
