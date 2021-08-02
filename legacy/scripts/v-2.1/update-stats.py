import os,sys
import MySQLdb
import string
import commands
import util

from optparse import OptionParser

__version__="1.0"
__status__ = "Dev"


###############################
def main():

	usage = "\n%prog  [options]"
	parser = OptionParser(usage,version="%prog " + __version__)
	parser.add_option("-v","--versionName",action="store",dest="versionName",help="BioXpress version")
#	parser.add_option("-t","--tableName_prefix",action="store",dest="tableName_prefix",help="Table name Prefix")


	(options,args) = parser.parse_args()
	for file in ([options.versionName]):
		if not (file):
			parser.print_help()
			sys.exit(0)

	versionName = options.versionName

	 
	global PHASH
        PHASH = {}


	util.LoadParams("./conf/database.txt", PHASH)
	DBH = MySQLdb.connect(host = PHASH['DBHOST'], user = PHASH['DBUSERID'],
		passwd = PHASH['DBPASSWORD'], db = PHASH['DBNAME'])
	cur = DBH.cursor()
                	
	try:
		sql = ("DELETE FROM %s WHERE versionName = '%s'" % ("Biox_stats", versionName))
		print sql
		#cur.execute(sql)

                sql = ("SELECT COUNT(DISTINCT A.featureName) n FROM Biox_feature A WHERE A.featureType = 'mrna' ")
                cur.execute(sql)
                row = cur.fetchone()
                countValue = row[0]
                string = "INSERT INTO %s (versionName, countName, countValue) VALUES "
                string += "('%s', '%s', %s)"
                sql = (string % ("Biox_stats", versionName, 'UniProtKB/Swiss-Prot Accessions hit', countValue))
                print sql
                cur.execute(sql)

                sql = ("SELECT COUNT(DISTINCT sampleSynonym) n FROM Biox_sample ")
                cur.execute(sql)
                row = cur.fetchone()
                countValue = row[0]-41
                string = "INSERT INTO %s (versionName, countName, countValue) VALUES "
                string += "('%s', '%s', %s)"
                sql = (string % ("Biox_stats", versionName, 'Disease Ontology terms mapped', countValue))
                print sql
                #cur.execute(sql)

                sql = ("SELECT COUNT(DISTINCT A.featureName) n FROM Biox_feature A INNER JOIN Biox_level B ON A.featureId=B.featureId WHERE B.sigExp = 'Yes' AND A.featureType = 'mrna' ")
		cur.execute(sql)
                row = cur.fetchone()
                countValue = row[0]
                string = "INSERT INTO %s (versionName, countName, countValue) VALUES "
                string += "('%s', '%s', %s)"
                sql = (string % ("Biox_stats", versionName, 'Number of differentially expressed genes', countValue))
                print sql
                #cur.execute(sql)


                sql = ("SELECT COUNT(DISTINCT featureName) n FROM Biox_feature WHERE featureType = 'mrna'")
                #cur.execute(sql)
                #row = cur.fetchone()
                #countValue = row[0]
                string = "INSERT INTO %s (versionName, countName, countValue) VALUES "
                string += "('%s', '%s', %s)"
                #sql = (string % ("Biox_stats", versionName, 'Number of genes analyzed', countValue))
                #print sql
                #cur.execute(sql)

                sql = ("SELECT COUNT(DISTINCT A.featureName) n FROM Biox_feature A INNER JOIN Biox_level B ON A.featureId=B.featureId WHERE B.sigExp = 'Yes' AND A.featureType = 'mirna' ")
                cur.execute(sql)
                row = cur.fetchone()
                countValue = row[0]
                string = "INSERT INTO %s (versionName, countName, countValue) VALUES "
                string += "('%s', '%s', %s)"
                sql = (string % ("Biox_stats", versionName, 'Number of differentially expressed miRNAs', countValue))
                print sql
                #cur.execute(sql)


                #sql = ("SELECT COUNT(DISTINCT featureName) n FROM Biox_feature WHERE featureType = 'mirna'")
                #cur.execute(sql)
                #row = cur.fetchone()
                #countValue = row[0]
                #string = "INSERT INTO %s (versionName, countName, countValue) VALUES "
                #string += "('%s', '%s', %s)"
                #sql = (string % ("Biox_stats", versionName, 'Number of miRNAs analyzed', countValue))
                #print sql
                #cur.execute(sql)

		
		string = "INSERT INTO %s (versionName, countName, countValue) VALUES "
		string += "('%s', '%s', %s)"
		sql = (string % ("Biox_stats", versionName, 'Number of patients with paired data analyzed for gene', 667))
		print sql
		#cur.execute(sql)

		string = "INSERT INTO %s (versionName, countName, countValue) VALUES "
                string += "('%s', '%s', %s)"
                sql = (string % ("Biox_stats", versionName, 'Number of patients with paired data analyzed for miRNA', 575))
                print sql
                #cur.execute(sql)


                #sql = ("SELECT COUNT(DISTINCT sampleName) n FROM Biox_sample ")
		#cur.execute(sql)
		#row = cur.fetchone()
		#countValue = row[0]-1
		#string = "INSERT INTO %s (versionName, countName, countValue) VALUES "
		#string += "('%s', '%s', %s)"
		#sql = (string % ("Biox_stats", versionName, 'TCGA Cancer types', countValue))
		#print sql
		#cur.execute(sql)
		

		DBH.commit()
	except:
		DBH.rollback()


	DBH.close()
	print "Done loading"




if __name__ == '__main__':
	main()



