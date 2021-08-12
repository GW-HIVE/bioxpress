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
	(options,args) = parser.parse_args()

	util.LoadParams("./../conf/database.txt", PHASH)
	DBH = MySQLdb.connect(host = PHASH['DBHOST'], user = PHASH['DBUSERID'],
		passwd = PHASH['DBPASSWORD'], db = PHASH['DBNAME'])

	for file in ([options.tsvfile]):
		if not (file):
			parser.print_help()
			sys.exit(0)
	cur = DBH.cursor()
	tsvFile = options.tsvfile

	queryObj = json.loads(open("externalDb/query.json").read())

	subjectDic = {}
	FR = open(tsvFile, "r")
	for line in FR:
		line = line.strip().split('\t')
		subjectCode = line[1]
		sql = "SELECT cancerId FROM biox_cancertype WHERE cancerName = '%s' " % (line[1])
		cur.execute(sql)
		cancerId = cur.fetchone()[0]
		subjectDic[subjectCode] = cancerId
	FR.close()

	patList = "/data/projects/bioxpress/v-2.1/downloads/tcga/metadata/metadata.part*.tsv"
	fileList = glob.glob(patList)

	count = 0
	for patFile in fileList:
		print patFile
		FR = open(patFile, "r")
		for line in FR:
			if not line.startswith("summary") and not line.startswith("demographic"):
				line = line.split('\t')
				if patFile.find('part3') >= 0:
					line = [""] + line
				subjectCode = line[4]
				ethnicity = line[1]
				gender = line[7]
				if patFile.find('part1') >= 0:
					yearOfSmoke = line[6]
					ageAtDiagonoses = line[28]
					yearOfDeath = line[42]
					race = line[39]
					seqMethod = line[36] #strategy 0
					daysToDeath = line[43]
					height = line[44]
					weight = line[5]
					primaryDiagnosis = line[13]
					yearOfBorn = line[20]
					vitalStatus = line[23]
					alcoholHistory = line[26]
					tumorStage = line[32]
				if patFile.find('part2') >= 0:
					weight = line[5]
					yearOfSmoke = line[6]
					primaryDiagnosis = line[14]
					ageAtDiagonoses = line[29]
					daysToDeath = line[44]
					height = line[45]
					yearOfDeath = line[39]
					race = line[40]
					seqMethod = line[37]
					yearOfBorn = line[21]
					vitalStatus = line[25]
					alcoholHistory = line[27]
					tumorStage = line[33]
				elif patFile.find('part3') >= 0:
					weight = line[4]
					yearOfSmoke = line[5]
					primaryDiagnosis = line[12]
					ageAtDiagonoses = line[27]
					daysToDeath = line[42]
					height = line[43]
					yearOfDeath = line[41]
					race = line[38]
					seqMethod = line[35]
					yearOfBorn = line[19]
					vitalStatus = line[22]
					alcoholHistory = line[25]
					tumorStage = line[31]

				string = [subjectCode,seqMethod,yearOfBorn,gender,weight]
				string += [tumorStage,daysToDeath,height]
				string += [yearOfDeath,ageAtDiagonoses,ethnicity,yearOfSmoke]
				string += [race,primaryDiagnosis,alcoholHistory,vitalStatus]
				string = ",'" + "','".join(string) + "'"
				try:
					string = str(subjectDic[subjectCode]) + string
				except:
					string = 'NULL' + string
				count += 1

				sql = queryObj["insertQuery5"]["querystring"] + "(" + string + ')'
				cur.execute(sql)
				if count % 1000 == 0:
					print "LOAD:",count
		FR.close()

		string2 = ','.join(['NULL']*len(string.split(',')))
		sql = queryObj["insertQuery5"]["querystring"] + "(" + string + ')'
		cur.execute(sql)

	DBH.commit()
	print "Finshed loading data"


if __name__ == '__main__':
	main()


