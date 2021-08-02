#!/usr/bin/env python
import string
import json
import commands
import MySQLdb

#######################################
def composeRetrieveSql(sqlObj, queryFieldList, queryValueList, operatorList, connectorList):

	condList = []
	queryValueList = map(json.dumps, queryValueList)
	condList.append(queryFieldList[0] + " " + operatorList[0] + " " + queryValueList[0]);
	for i in xrange(1, len(queryFieldList)):
		condList.append(connectorList[i-1] + " " + queryFieldList[i] + " " + operatorList[i] + " " + queryValueList[i])

	sql = sqlObj["querystring"] + " " + " ".join(condList)

	return sql


#######################################
def composeInsertSql1(sqlObj, insertValueList):

	insertValue = map(json.dumps, insertValueList)
	sql = sqlObj["querystring"] + " (" + ",".join(insertValue) + ") "

	return sql

#######################################
#this function is used in input data in json format
def composeInsertSql2(sqlObj, insertFieldList, insertValueList):

	insertFieldText = ','.join(insertFieldList)
        insertValue = map(json.dumps, insertValueList)
        sql = sqlObj["querystring"] % (insertFieldText)
	sql += " (" + ",".join(insertValue) + ") "

        return sql
	

#######################################
def getRecords(PHASH, sql, fieldLabelList):

	DBH = MySQLdb.connect(host = PHASH['DBHOST'], user = PHASH['DBUSERID'],
		passwd = PHASH['DBPASSWORD'], db = PHASH['DBNAME'])
	cur = DBH.cursor()
	#cur = DBH.cursor()
	cur.execute(sql)
	csvBuffer = ",".join(fieldLabelList) + '\n'

	jsonOutTable = []
	jsonOutTable.append(fieldLabelList)
	for row in cur.fetchall():
		jsonOutTable.append(row)
		row = map(str, row)
		csvBuffer += ",".join(row) + '\n'
	DBH.close()

	return jsonOutTable, csvBuffer


#######################################
def saveCsvData(csvBuffer, fileName, outputPath):

	outputFile = outputPath + fileName
	FW = open(outputFile, "w")
	FW.write("%s" % (csvBuffer))
	FW.close()
	cmd = "chmod 777 " + outputFile
	x = commands.getoutput(cmd)

	return



