#!/usr/bin/python
import os,sys
import string
import cgi,csv
import commands
import json
import util
import searchQueryFormatting as sqf
import MySQLdb
from optparse import OptionParser

__version__="1.0"

#############################################
def isNumeric(value):
	try:
		float(value)
		return True
	except ValueError:
		return False


#############################################
def main():

	usage = "\n%prog  [options]"
	parser = OptionParser(usage,version="%prog " + __version__)
	parser.add_option("-j","--inputJson",action="store",dest="inputJson",help="JSON format")
	parser.add_option("-i","--inputFile",action="store",dest="inputFile",help="tst/tsv format")

	(options,args) = parser.parse_args()
	for file in ([options.inputJson, options.inputFile]):
		if not (file):
			parser.print_help()
			sys.exit(0)

	inputJson = options.inputJson
	inputFile = options.inputFile
        global PHASH
        global AUTH
        PHASH = {}
        outJson = {}

	if True:
		#Load search queries
		inJson = json.loads(open(inputJson).read())
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

		fieldIdList = []
		count = 0
		with open(inputFile, 'rb') as tsvfile:
			tsvreader = csv.reader(tsvfile, delimiter='\t', quotechar='|')
			for row in tsvreader:
				count += 1
				if row[0] == 'uniprotAC':
					for i in row:
						sql = sqf.composeRetrieveSql(queryObj["retrieveQuery3"], ["name", "datasetId"], [i, datasetId], ["=", "="], ["AND"])
						cur.execute(sql)
						fieldIdList += [cur.fetchone()[0]]
				else:
					for i in range(0, len(row)):
						if isNumeric(row[i]):
							insertValueList = [fieldIdList[i], datasetId, float(row[i])]
							sql = sqf.composeInsertSql1(queryObj["insertQuery1"], insertValueList)
							cur.execute(sql)
						else:
							insertValueList = [fieldIdList[i], datasetId, row[i]]
							sql = sqf.composeInsertSql1(queryObj["insertQuery4"], insertValueList)
							cur.execute(sql)
				if count % 100000 == 0:
					print count
					
		outJson = {"taskStatus": "1", "insertMsg": "Data loaded"}
		DBH.commit()
	else:
		DBH.rollback()
		outJson = {"taskStatus": "0", "errorMsg": "ERROR happened"}
	
	DBH.close()
	print json.dumps(outJson)


if __name__ == '__main__':
        main()



