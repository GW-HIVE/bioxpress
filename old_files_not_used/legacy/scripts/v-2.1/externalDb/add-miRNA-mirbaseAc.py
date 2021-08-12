#!/usr/bin/python
import os,sys
import string
import cgi,csv
import commands
import json
import util
import MySQLdb
from optparse import OptionParser

__version__="1.0"


#############################################
def main():

	usage = "\n%prog  [options]"
	parser = OptionParser(usage,version="%prog " + __version__)
	helpMsg = "input the file from text mining results with microRNA data"
	parser.add_option("-i","--inputFile",action="store",dest="inputFile",help=helpMsg)

	(options,args) = parser.parse_args()
	for file in ([options.inputFile]):
		if not (file):
			parser.print_help()
			sys.exit(0)

	inputFile = options.inputFile

	referDic = {}
	referenceFile = "/data/projects/bioxpress/v-2.1/generated/reference/hsa.gff3"
	outputFile = open("/data/projects/bioxpress/v-2.1/generated/logs-step16/mapped_mirna_records_from_textMining.txt", 'w')
	with open(referenceFile, 'rb') as tsvfile:
		tsvreader = csv.reader(tsvfile, delimiter='\t', quotechar='|')
		for row in tsvreader:
			if not row[0].startswith('#') and row[-1].find('Derives_from') == -1:
				infoRow = row[-1].split(';')

				mirnaName = infoRow[-1].split('=')[-1].lower()
				mirnaName = '-'.join(mirnaName.split('-')[0:3])
				mirnaId = infoRow[0].split('=')[-1]
				referDic[mirnaName.lower()] = mirnaId

	with open(inputFile, 'rb') as tsvfile:
		if True:
			tsvreader = csv.reader(tsvfile, delimiter='\t', quotechar='|')
			for row in tsvreader:
				mirnaId = ''
				if row[0] != 'mirNum':
					row[0] = row[0].strip().lower()
					mirnaName = 'hsa-mir-' + row[0] if row[0].find('let') == -1 else 'hsa-let-' + row[0].split('let')[-1]
					if mirnaName in referDic:
						newLine = referDic[mirnaName] + '\t' + "\t".join(row)
						outputFile.write(newLine + '\n')
					elif mirnaName in ['hsa-mir-5p', 'hsa-mir-3p', 'hsa-let-5p', 'hsa-let-3p']:
						mirnaName2 = row[1].strip().lower()
						mirna = mirnaName2.split('-')[0:2] if mirnaName2.find('hsa')  == -1 else mirnaName2.split('-')[1:3]
						mirnaName = 'hsa-' + '-'.join(mirna)
						if mirnaName in referDic:
							newLine = referDic[mirnaName] + '\t' + "\t".join(row)
							outputFile.write(newLine + '\n')
						else:
							print mirnaName
					elif mirnaName.find('-5p') >= 0 or mirnaName.find('-3p') >= 0:
						mirnaName2 = '-'.join(mirnaName.split('-')[:-1])
						if mirnaName2 in referDic:
							newLine = referDic[mirnaName2] + '\t' + "\t".join(row)
							outputFile.write(newLine + '\n')
						elif mirnaName2 + 'a' in referDic:
							newLine = referDic[mirnaName2+'a'] + '\t' + "\t".join(row)
							outputFile.write(newLine + '\n')
						elif mirnaName2 + 'b' in referDic:
							newLine = referDic[mirnaName2+'b'] + '\t' + "\t".join(row)
							outputFile.write(newLine + '\n')
						else:
							print mirnaName2, mirnaName
					else:
						print mirnaName
						

if __name__ == '__main__':
        main()



