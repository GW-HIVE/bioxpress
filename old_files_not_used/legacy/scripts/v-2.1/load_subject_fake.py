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
	msg = "Input TSV file for BioXpress_cancer_final.ext"
	parser.add_option("-l","--tsvfile",action="store",dest="tsvfile",help=msg)
	(options,args) = parser.parse_args()
	for file in ([options.tsvfile]):
		if not (file):
			parser.print_help()
			sys.exit(0)

	tsvFile = options.tsvfile
	subjectDic = {"Manual":"MAN", "textMining":"TM"}
	queryObj = json.loads(open("externalDb/query.json").read())

	util.LoadParams("./../conf/database.txt", PHASH)
	DBH = MySQLdb.connect(host = PHASH['DBHOST'], user = PHASH['DBUSERID'],
		passwd = PHASH['DBPASSWORD'], db = PHASH['DBNAME'])
	cur = DBH.cursor()

	dataFile = open(tsvFile, 'rb')
	for row in dataFile:
		row = row.strip().split('\t')
		if row[-1] in subjectDic:
			cancerSynonId = row[2].split(' & ')[-1].split(' / ')[0]
			cancerSynonId = cancerSynonId.split(':')[1].strip()
			subjectCode = subjectDic[row[-1]] + '-' + cancerSynonId + '-?'

			sql = "SELECT cancerId FROM biox_cancertype WHERE cancerName = '-' AND cancerSynonymId = '%s'" % cancerSynonId
			cur.execute(sql)
			cancerId = cur.fetchone()[0]
			string = str(cancerId) + ",'" + subjectCode + "','" + "','".join(['']*15) + "'"
			sql = queryObj["insertQuery5"]["querystring"] + "(" + string + ')'
			cur.execute(sql)
			print sql

	DBH.commit()
	print "Finshed loading data"


if __name__ == '__main__':
	main()


