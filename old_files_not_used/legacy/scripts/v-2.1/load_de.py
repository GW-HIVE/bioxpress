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

        util.LoadParams("./conf/database.txt", PHASH)
        DBH = MySQLdb.connect(host = PHASH['DBHOST'], user = PHASH['DBUSERID'],
                    passwd = PHASH['DBPASSWORD'], db = PHASH['DBNAME'])


	for file in ([options.tsvfile]):
		if not (file):
			parser.print_help()
			sys.exit(0)

	cur = DBH.cursor()

	tsvFile = options.tsvfile

	try:
		FR = open(tsvFile, "r")
		lines = FR.readlines()
		for line in lines:
			line=line.strip().split('\t')
			sql = "SELECT featureId FROM biox_feature WHERE featureName = '%s' " % (line[1])
              		cur.execute(sql)
		        featureId = cur.fetchone()[0]
			sql = ("SELECT cancerId FROM biox_cancertype WHERE cancerName = '%s' AND cancerSynonymId = '%s'" % (line[2],line[3]))
			cur.execute(sql)
			cancerId = cur.fetchone()[0]
			string = "INSERT INTO biox_de (%s) VALUES "
			string += " (%s, %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s')"
			line[7] = "miRNAseq.HiSeq" if line[7] == "HiSeq.hg19.mirbase20" else line[7]
			line[7] = "miRNAseq.GA" if line[7] == "GA.hg19.mirbase20" else line[7]
			sql = (string % (PHASH["BIOXPRESS_FLIST"], featureId, cancerId, line[4], line[8], line[9], line[-1], line[5], line[10], line[11], line[7], line[-2]))
			cur.execute(sql)
			print sql
		FR.close()
		DBH.commit()
		print "Finshed loading data"
	except:
		print "there was some problem with the sqls"
		DBH.rollback()

	DBH.close()




if __name__ == '__main__':
	main()


