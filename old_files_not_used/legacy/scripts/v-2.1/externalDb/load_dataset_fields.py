#!/usr/bin/python
import os,sys
import string
import cgi
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
		fieldsList = inJson["fieldsinfo"]
		datasetsInfo = inJson["datasetsinfo"]

		#Link to database
		util.LoadParams("../conf/database.txt", PHASH)
        	DBH = MySQLdb.connect(host = PHASH['DBHOST'], user = PHASH['DBUSERID'], 
				passwd = PHASH['DBPASSWORD'], db = PHASH['DBNAME'])
		cur = DBH.cursor()

		#Construct and execute sql
		queryObj = json.loads(open("query.json").read())
		queryFieldList = []
		queryValueList = []
		connectorList = []
		operatorList = []
		for key,val in datasetsInfo.items():
			queryFieldList.append(key)
			queryValueList.append(val)
			connectorList.append('AND')
			operatorList.append("=")

		sql = sqf.composeRetrieveSql(queryObj["retrieveQuery2"], queryFieldList, queryValueList, operatorList, connectorList)
		cur.execute(sql)
		datasetId = cur.fetchone()[0]
		foreignKey = queryObj["insertQuery3"]["foreignkey"][0]

		for i in fieldsList:
			insertFieldList = [foreignKey]
			insertValueList = [datasetId]
			for key,val in i.items():
				insertFieldList.append(key)
				insertValueList.append(val)

			sql = sqf.composeInsertSql2(queryObj["insertQuery3"], insertFieldList, insertValueList)
			cur.execute(sql)
			print sql
		outJson = {"taskStatus": "1", "insertMsg": "Data loaded"}
		DBH.commit()
	except:
		DBH.rollback()
		outJson = {"taskStatus": "0", "errorMsg": "ERROR happened"}
	
	DBH.close()
	print json.dumps(outJson)


if __name__ == '__main__':
        main()



