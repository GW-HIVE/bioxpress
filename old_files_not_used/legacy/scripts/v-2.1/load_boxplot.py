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
			if not line.startswith("geneName") and not line.startswith("miRNAName") and not line.startswith("?,"):
				line = line.strip().split(',')
				numbers = line[4::]
				sql = "SELECT featureId FROM biox_feature WHERE featureName = '%s' " % (line[0])
              			cur.execute(sql)
			        featureId = cur.fetchone()[0]
				sql = ("SELECT cancerId FROM biox_cancertype WHERE cancerName = '%s' " % (line[1]))
				cur.execute(sql)
				cancerId = cur.fetchone()[0]

				string = "INSERT INTO biox_boxplot (%s) VALUES "
				string += " (%s, %s, '%s', '%s', %s, %s, %s, %s, %s)"

				line[2] = "miRNAseq.HiSeq" if line[2] == "HiSeq.hg19.mirbase20" else line[2]
                        	line[2] = "miRNAseq.GA" if line[2] == "GA.hg19.mirbase20" else line[2]
			
				sql = (string % (PHASH["BIOXPRESS_BOXLIST"], featureId, cancerId, line[2], line[3], round(float(numbers[0]),2), round(float(numbers[1]),2), round(float(numbers[2]),2), round(float(numbers[3]),2), round(float(numbers[4]),2)))
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


