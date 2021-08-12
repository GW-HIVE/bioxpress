import csv
import json


def load_sheet_as_dict(sheet_obj, in_file, separator, anchor_field):


    seen = {}
    
    if "fields" not in sheet_obj:
        sheet_obj["fields"] = []
    if "data" not in sheet_obj:
        sheet_obj["data"] = {}


    f_list = []
    with open(in_file, 'r') as FR:
        csv_grid = csv.reader(FR, delimiter=separator, quotechar='\"')
        row_count = 0
        for row in csv_grid:
            if json.dumps(row) in seen:
                continue
            seen[json.dumps(row)] = True
            row_count += 1
            if row_count == 1:
                f_list = row
                for j in xrange(0, len(row)):
                    if row[j] == anchor_field:
                        continue
                    sheet_obj["fields"].append(row[j].strip().replace("\"", ""))
            else:
                new_row = []
                for j in xrange(0, len(row)):
                    if f_list[j] == anchor_field:
                        continue
                    new_row.append(row[j].strip())
                main_id = row[f_list.index(anchor_field)]
                if main_id not in sheet_obj["data"]:
                    sheet_obj["data"][main_id] = [] 
                sheet_obj["data"][main_id].append(new_row)
    return



def load_sheet(sheet_obj, in_file, separator):

    seen = {}
    sheet_obj["fields"] = []
    sheet_obj["data"] = []
    with open(in_file, 'r') as FR:
        csv_grid = csv.reader(FR, delimiter=separator, quotechar='\"')
        row_count = 0
        for row in csv_grid:
            if json.dumps(row) in seen:
                continue
            seen[json.dumps(row)] = True
            row_count += 1
            if row_count == 1:
                for j in xrange(0, len(row)):
                    sheet_obj["fields"].append(row[j].strip().replace("\"", ""))
            else:
                new_row = []
                for j in xrange(0, len(row)):
                    new_row.append(row[j].strip())
                sheet_obj["data"].append(new_row)
    return


def load_workbook(workbook_obj, fileset_objlist, separator):

    for obj in fileset_objlist:
        for file_name in obj["filenamelist"]:
            in_file = obj["dir"] + file_name
            workbook_obj["sheets"][file_name] = {}
            load_sheet(workbook_obj["sheets"][file_name], in_file, ",")

    return

def left_join_tables(tbl_a, tbl_b):

    map_dict = {}
    for i in xrange(0, len(tbl_b)):
        if tbl_b[i][0] not in map_dict:
            map_dict[tbl_b[i][0]] = []
        map_dict[tbl_b[i][0]].append(i)

    empty_row = []
    for j in xrange(1, len(tbl_b[0])):
        empty_row.append("")

    tbl_c = [tbl_a[0] + tbl_b[0][1:]]
    for row in tbl_a[1:]:
        main_id_a = row[0]
        if main_id_a in map_dict:
            for i in map_dict[main_id_a]:
                tbl_c.append(row + tbl_b[i][1:])
        else:
            tbl_c.append(row + empty_row)

    return tbl_c


