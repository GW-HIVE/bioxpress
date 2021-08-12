import os,sys
from optparse import OptionParser
import MySQLdb
import string
import commands
import glob
import util
import json

__version__="1.0"
__status__ = "Dev"


###############################
def main():

	global PHASH
	global DBH
	PHASH = {}

	usage = "\n%prog  [options]"
	parser = OptionParser(usage,version="%prog " + __version__)
	msg = "Input TSV file for BioXpress_cancer_addUberon.txt"
	parser.add_option("-l","--tsvfile",action="store",dest="tsvfile",help=msg)
	(options,args) = parser.parse_args()
	for file in ([options.tsvfile]):
		if not (file):
			parser.print_help()
			sys.exit(0)

	tsvFile = options.tsvfile
	subjectDic = {"Manual":"MAN", "textMining":"TM"}

	util.LoadParams("./../conf/database.txt", PHASH)
	DBH = MySQLdb.connect(host = PHASH['DBHOST'], user = PHASH['DBUSERID'],
		passwd = PHASH['DBPASSWORD'], db = PHASH['DBNAME'])
	cur = DBH.cursor()

	dataFile = open(tsvFile, 'rb')
	count = 0
	for row in dataFile:
		row = row.strip().split('\t')
		if row[1] == "-":
			count += 1
			cancerSynonId = row[2].split(' & ')[-1].split(' / ')[0]
			cancerSynonId = cancerSynonId.split(':')[1].strip()
			subjectCode = subjectDic[row[-2]] + '-' + cancerSynonId + '-?'
			sampleCode = subjectDic[row[-2]] + '-' + cancerSynonId + '-' + str(count)

			sql = "SELECT subjectId FROM biox_subject WHERE subjectCode = '%s'" % subjectCode
			cur.execute(sql)
			subjectId = cur.fetchone()[0]

			sql = "SELECT tissueId FROM biox_tissue WHERE tissueName = '%s'" % row[-1]
			cur.execute(sql)
			tissueId = cur.fetchone()[0]

			string = "INSERT INTO biox_sample (tissueId, subjectId, sampleName, sampleType) VALUES (%s, %s, '%s', '%s')"
			sql = string % (tissueId, subjectId, sampleCode, "cancer")
			cur.execute(sql)
			print sql

	DBH.commit()
	print "Finshed loading data"


if __name__ == '__main__':
	main()


