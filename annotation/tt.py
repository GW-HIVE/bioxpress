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

    study_list = []
    cat_dict = {}
    file_dict = {}
    caseid2studyid = {}
    fileid2cat = {}

    in_file = "generated/misc/studies.csv"
    data_frame = {}
    csvutil.load_sheet(data_frame,in_file, "\t")
    f_list = data_frame["fields"]
    for row in data_frame["data"]:
        study_list.append(row[0])


    in_file = "downloads/sample_list_from_gdc/gdc_sample_sheet.primary_tumor.tsv"
    data_frame = {}
    csvutil.load_sheet(data_frame,in_file, "\t")
    f_list = data_frame["fields"]
    for row in data_frame["data"]:
        study_id = row[f_list.index("Project ID")]
        file_id = row[f_list.index("File ID")]
        case_id = row[f_list.index("Case ID")]
        if case_id not in cat_dict:
            caseid2studyid[case_id] = study_id
            cat_dict[case_id] = []
            file_dict[case_id] = []
            fileid2cat[case_id] = {}

        cat_dict[case_id].append("Primary-Tumor")
        file_dict[case_id].append(file_id)
        fileid2cat[case_id][file_id] = "Primary-Tumor"


    in_file = "downloads/sample_list_from_gdc/gdc_sample_sheet.solid_tissue_normal.tsv"
    data_frame = {}
    csvutil.load_sheet(data_frame,in_file, "\t")
    f_list = data_frame["fields"]
    for row in data_frame["data"]:
        study_id = row[f_list.index("Project ID")]
        case_id = row[f_list.index("Case ID")]
        file_id, case_id = row[0], row[5]
        if case_id not in cat_dict:
            caseid2studyid[case_id] = study_id
            cat_dict[case_id] = []
            file_dict[case_id] = []
            fileid2cat[case_id] = {}
        cat_dict[case_id].append("Solid-Tissue-Normal")
        file_dict[case_id].append(file_id)
        fileid2cat[case_id][file_id] = "Solid-Tissue-Normal"



    for case_id in cat_dict:
        if len(sorted(set(cat_dict[case_id]))) == 2:
            study_id = caseid2studyid[case_id]
            if study_id not in study_list:
                continue
            print study_id, case_id



if __name__ == '__main__':
    main()


