#!/usr/bin/python
import os,sys
import string
import commands
import json
import util
import searchQueryFormatting as sqf
import MySQLdb
from optparse import OptionParser

__version__="1.0"

#~~~~~~~~~~~~~~~~~~~~~
def main():

	usage = "\n%prog  [options]"
	parser = OptionParser(usage,version="%prog " + __version__)
	parser.add_option("-j","--inputJson",action="store",dest="inputJson",help="JSON format")

	(options,args) = parser.parse_args()
	for file in ([options.inputJson]):
		if not (file):
			parser.print_help()
			sys.exit(0)

	inputJson = options.inputJson
	global PHASH
	global AUTH
	PHASH = {}
	outJson = {}

	try:
		#Load search queries
		inJson = json.loads(open(inputJson).read())
		inJson = inJson["datasetsinfo"]

		#Link to database
		util.LoadParams("../conf/database.txt", PHASH)
        	DBH = MySQLdb.connect(host = PHASH['DBHOST'], user = PHASH['DBUSERID'], 
				passwd = PHASH['DBPASSWORD'], db = PHASH['DBNAME'])
		cur = DBH.cursor()

		#Construct and execute sql
		queryObj = json.loads(open("query.json").read())
		#seen = {}
		#sql = queryObj["retrieveQuery1"]["querystring"]
		#cur.execute(sql)
		#for row in cur.fetchall():
		#	seen[row[0]] = 1

		insertFieldList = []
		insertValueList = []
		for key,val in inJson.items():
			insertFieldList.append(key)
			insertValueList.append(val)
		
		sql = sqf.composeInsertSql2(queryObj["insertQuery2"], insertFieldList, insertValueList)
		cur.execute(sql)
		DBH.commit()
		outJson = {"sql": sql}
	except:
		DBH.rollback()
		outJson = {"errorMsg":"ERROR happened"}
	
	DBH.close()
	print json.dumps(outJson)


if __name__ == '__main__':
        main()



