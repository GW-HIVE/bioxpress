import os,sys
import MySQLdb
import string
import commands
import util

from optparse import OptionParser
import hashlib


__version__="1.0"
__status__ = "Dev"



#################
def EncryptString(string):
	m = hashlib.md5()
	m.update(string)
	return m.hexdigest()



###############################
def main():

	global PHASH
        PHASH = {}


	util.LoadParams("./conf/database.txt", PHASH)
	DBH = MySQLdb.connect(host = PHASH['DBHOST'], user = PHASH['DBUSERID'],
		passwd = PHASH['DBPASSWORD'], db = PHASH['DBNAME'])
	cur = DBH.cursor()
               
	fields = 'id,UniProt_AC, Gene_Name, Accession, Genome_Position, Position_N, Ref_N, Var_N, Position_A, Ref_A, Var_A, Polyphen_Pred, PMID, Cancer_Type, Source, function, Status' 
	try:
		sql = "SELECT "+fields+" FROM biomuta3"
		cur.execute(sql)
                cntHash = {}
		txtHash = {}
		for row in cur.fetchall():
			buffer = ''
			for i in range(1, len(row)):
				buffer += '|' + str(row[i])
			encr = EncryptString(buffer)
			
			cntHash[encr] = cntHash[encr] + 1 if encr in cntHash else 1
			txtHash[encr] = txtHash[encr] + ' ' + str(row[0]) if encr in txtHash else str(row[0])



		for encr in cntHash:
                        if cntHash[encr] > 1:
                                idList = txtHash[encr].split(" ")
				dList = idList.sort()
				for i in range(1, len(idList)):
					sql = 'DELETE FROM biomuta3 WHERE id = ' + str(idList[i])
					cur.execute(sql)	
		#FW = open("output.txt", "w")
		#for encr in cntHash:
			#FW.write("%s|%s|%s\n" %(cntHash[encr], encr, txtHash[encr]))
		#FW.close()
	except:
		print "Error"

	DBH.close()




if __name__ == '__main__':
	main()



