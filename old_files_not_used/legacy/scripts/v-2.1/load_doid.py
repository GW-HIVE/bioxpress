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
			sql = "SELECT cancerId FROM biox_cancertype WHERE cancerSynonymId = '%s' " % (line[-1])
			cur.execute(sql)
			contentAll = cur.fetchall()
			if len(contentAll) > 0:
				cancerId = [row[0] for row in contentAll]
	
				string = "INSERT INTO biox_do (%s) VALUES "
				string += " ('%s', '%s', '%s')"
				sql = (string % ("doId,parentId,doTerm", line[0], line[1], line[2]))
				cur.execute(sql)

				string = "UPDATE biox_cancertype SET cancerSynonymId = '%s' WHERE "
				string += " cancerId IN (%s)"
				sql = (string % (line[0], ','.join(map(str, cancerId))))
				cur.execute(sql)
				print sql
		FR.close()

		sql = "SELECT cancerId FROM biox_cancertype WHERE cancerSynonymId LIKE '%DOID%'"
		cur.execute(sql)
		contentAll = cur.fetchall()
		extraSample = [row[0] for row in contentAll]
		string = "DELETE FROM biox_cancertype WHERE cancerId IN (%s)" % (','.join(map(str, extraSample)))
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

