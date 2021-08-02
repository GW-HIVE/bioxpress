import os,sys
import MySQLdb
import string
import commands
from optparse import OptionParser
import glob
import util
import json


__version__="1.0"
__status__ = "Dev"




###############################
def main():

	global PHASH
	PHASH = {}

	usage = "\n%prog  [options]"
	parser = OptionParser(usage,version="%prog " + __version__)
	msg = "Input TSV file for patient-sample-code list"
        
	parser.add_option("-l","--tsvfile",action="store",dest="tsvfile",help=msg)
	parser.add_option("-m","--metadatafile",action="store",dest="metadatafile",help="metadata file")
	(options,args) = parser.parse_args()

	util.LoadParams("./../conf/database.txt", PHASH)
	DBH = MySQLdb.connect(host = PHASH['DBHOST'], user = PHASH['DBUSERID'],
		passwd = PHASH['DBPASSWORD'], db = PHASH['DBNAME'])

	for file in ([options.tsvfile, options.metadatafile]):
		if not (file):
			parser.print_help()
			sys.exit(0)

	cur = DBH.cursor()
	tsvFile = options.tsvfile
	metadataFile = options.metadatafile

	queryObj = json.loads(open("externalDb/query.json").read())

	if True:
		subjectDic = {}
		FR = open(tsvFile, "r")
		for line in FR:
			line = line.strip().split('\t')
			subjectCode = line[1]
			sql = "SELECT cancerId FROM biox_cancertype WHERE cancerName = '%s' " % (line[0])
			cur.execute(sql)
			cancerId = cur.fetchone()[0]
			subjectDic[subjectCode] = cancerId
		FR.close()

		FR = open(metadataFile, "r")
		count = 0
		for line in FR:
			line = line.strip().split('\t')
			if line[5] != "submitter_id":
				subjectCode = line[5]
				seqMethod = line[12]
				yearOfBorn = line[16]
				gender = line[18]
				weight = line[22]
				tumorStage = line[23]
				daysToDeath = line[25]
				daysToLastFollow = line[27]
				height = line[29]
				yearOfDeath = line[30]
				ageAtDiagonoses = line[35]
				ethnicity = line[37]
				yearOfSmoke = line[38]
				race = line[39]
				primaryDiagnosis = line[8]
				alcoholHistory = line[13]
				vitalStatus = line[1]

				string = [subjectCode,seqMethod,yearOfBorn,gender,weight]
				string += [tumorStage,daysToDeath,daysToLastFollow,height]
				string += [yearOfDeath,ageAtDiagonoses,ethnicity,yearOfSmoke]
				string += [race,primaryDiagnosis,alcoholHistory,vitalStatus]
				string = ",'" + "','".join(string) + "'"
				string = str(subjectDic[subjectCode]) + string
			
				sql = queryObj["insertQuery5"]["querystring"] + "(" + string + ')'
				cur.execute(sql)
				count += 1
				print sql
		FR.close()

		DBH.commit()
		print "Finshed loading data"
	else:
		print "there was some problem with the sqls"
		DBH.rollback()

	DBH.close()
	print count


if __name__ == '__main__':
	main()

