import os,sys
import MySQLdb
import string
import commands
from optparse import OptionParser
import glob
import util


__version__="1.0"
__status__ = "Dev"




global PHASH
PHASH = {}

util.LoadParams("./conf/database.txt", PHASH)
DBH = MySQLdb.connect(host = PHASH['DBHOST'], user = PHASH['DBUSERID'],
	passwd = PHASH['DBPASSWORD'], db = PHASH['DBNAME'])

cur = DBH.cursor()


sql = "select featureId, xrefId from Biox_xref where xrefSrc = 'uniProtAc'"
cur.execute(sql)

dic = {}

for row in cur.fetchall():
	dic.setdefault(row[1], set()).add(str(row[0]))

count = 0
for key,val in dic.items():
	if len(val) > 1 and key.find('-') == -1:
		count += len(val)
		for i in val:
			sql = "delete from Biox_boxplot where featureId = %s"
			string = (sql % (int(i)))
			print string
			#cur.execute(string)

			sql = "delete from Biox_level where featureId = %s"
			string = (sql % (int(i)))
			print string
			#cur.execute(string)

			sql = "set foreign_key_checks = 0"
			#cur.execute(sql)

			sql = "delete from Biox_feature where featureId = %s"
			string = (sql % (int(i)))
			print string
			#cur.execute(string)
	
			sql = "delete from Biox_xref where featureId = %s"
                        string = (sql % (int(i)))
                        print string
                        cur.execute(string)
print count

DBH.commit()

DBH.close()
