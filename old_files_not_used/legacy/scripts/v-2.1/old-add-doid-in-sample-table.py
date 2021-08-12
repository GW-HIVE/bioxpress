import os,sys
import MySQLdb
import string
import commands
from optparse import OptionParser
import glob
import util


__version__="1.0"
__status__ = "Dev"




###############################
def main():

        global PHASH
        PHASH = {}

	usage = "\n%prog  [options]"
	parser = OptionParser(usage,version="%prog " + __version__)
	msg = "Input TSV file"
        
	parser.add_option("-i","--tsvfile",action="store",dest="tsvfile",help=msg)
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

	if True:
		FR = open(tsvFile, "r")
		lines = FR.readlines()
		for line in lines:
			line = line.strip().split('\t')
			if line[-1] != '-':
				try:
					sql = "SELECT sampleId FROM biox_sample WHERE sampleSynonymId = '%s' " % (line[-1])
					cur.execute(sql)
					contentAll = cur.fetchall()
					sampleId = [row[0] for row in contentAll]
	
					string = "UPDATE biox_sample SET sampleSynonymId = '%s' WHERE "
					string += " sampleId IN (%s)"
					sql = (string % (line[0], map(str, sampleId)))
					cur.execute(sql)
					print sql
				except:
					continue
		FR.close()
		sql = "SELECT sampleId FROM biox_sample WHERE sampleSynonymId LIKE '%DOID%'"
		cur.execute(sql)
		contentAll = cur.fetchall()
		extraSample = [row[0] for row in contentAll]
		string = "DELETE FROM biox_sample WHERE sampleId IN (%s)" % (','.join(map(str, extraSample)))
#		cur.execute(string)
		print string

		DBH.commit()
		print "Finshed loading data"
	else:
		print "there was some problem with the sqls"
		DBH.rollback()

	DBH.close()




if __name__ == '__main__':
	main()


