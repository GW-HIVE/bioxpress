import os,sys
import string
import csv
import json
from optparse import OptionParser
import MySQLdb



__version__="1.0"
__status__ = "Dev"




#################################
def reportProgress(progressFile, msg, openNew=False):

	msg = msg.strip()
        if openNew == True:
                with open(progressFile, "w") as FW:
                        FW.write(msg + "\n")
        else:
                with open(progressFile, "a") as FA:
                        FA.write(msg + "\n")
        return



###############################
def main():

	usage = "\n%prog  [options]"
	parser = OptionParser(usage,version="%prog " + __version__)
	parser.add_option("-i","--configfile",action="store",dest="configfile",help="NT file")


	(options,args) = parser.parse_args()
	for file in ([options.configfile]):
		if not (file):
			parser.print_help()
			sys.exit(0)




	configJson = json.loads(open(options.configfile, "r").read())
 	DBH = MySQLdb.connect(host = configJson["dbinfo"]["host"], 
				user = configJson["dbinfo"]["userid"], 
				passwd = configJson["dbinfo"]["password"],
				db = configJson["dbinfo"]["dbname"])
        cur = DBH.cursor()

	out_dir =  configJson["publisher"]["outdir"]
	
	table_obj = json.loads(open("../conf/mysql-schema.json", "r").read())


	for t in table_obj:
		fields = ",".join(table_obj[t]["fields"]) 	
		main_id = table_obj[t]["mainid"]
	
		sql = "SELECT count(*) FROM %s  " % (t)
                cur.execute(sql)
                row = cur.fetchone()
		row_count = row[0]
              
		out_file = out_dir + t + ".csv"
		FW = open(out_file, "w")
		FW.write("%s\n" % (fields))

		start = 0
                end = 1000000
		while start <= row_count:
			sql = "SELECT %s FROM %s WHERE %s >= %s AND %s <= %s  " % (fields, t,main_id, start, main_id,end)
			cur.execute(sql)
			for row in cur.fetchall():
				line = json.dumps(row)
				FW.write("%s\n" % (line[1:-1]))
			start = end + 1
			end += 1000000
		FW.close()
	
				


if __name__ == '__main__':
        main()








