import os,sys
import string
import json
from optparse import OptionParser
import csv

__version__="1.0"
__status__ = "Dev"


###############################
def main():

	usage = "\n%prog  [options]"
	parser = OptionParser(usage,version="%prog " + __version__)
	parser.add_option("-i","--configfile",action="store",dest="configfile",help="Config file")
        parser.add_option("-r","--rsrcname",action="store",dest="rsrcname",help="Resource name")
	parser.add_option("-c","--cancertype",action="store",dest="cancertype",help="Cancer type")
	parser.add_option("-s","--subjectid",action="store",dest="subjectid",help="Subject ID")





	(options,args) = parser.parse_args()
	for file in ([options.configfile,options.rsrcname, options.cancertype, options.subjectid]):
		if not (file):
			parser.print_help()
			sys.exit(0)

	rsrcName = options.rsrcname
	cancerType = options.cancertype
	subjectId = options.subjectid
	configJson = json.loads(open(options.configfile, "r").read())

	dataDir = configJson["extractor"]["inputdir"] + rsrcName + "/RNAseq/"
        outDir = configJson["extractor"]["outputdir"]

        

        inFile = dataDir + cancerType + "__gene_RNAseq__tissueTypeAll__20170615114021.txt"
        pairingFile = outDir + rsrcName + "-" + cancerType + "-samplepairing.csv"
        outFile = outDir + rsrcName + "-" + cancerType + "-extract-"+subjectId+".csv"

	
	sampleList = []
	with open(pairingFile, 'r') as csvfile:
                csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                rowCount = 0
                seen = {}
                for row in csvreader:                 
			if row[0] == subjectId:
				sampleList.append(row[1])
				sampleList.append(row[2])			


	FW = open(outFile, "w")

	with open(inFile, 'r') as csvfile:
        	csvreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        	rowCount = 0
        	seen = {}
		for row in csvreader:
			rowCount += 1
			if rowCount == 1:
				fieldList = row
			elif rowCount == 2:
				continue
			else:
				filteredRow = [row[0]]
				for i in xrange(0,len(row)):
					if i%2 == 1 and fieldList[i] in sampleList:
						filteredRow.append(row[i])
				FW.write("%s\n" % (",".join(filteredRow)))
	FW.close()



if __name__ == '__main__':
        main()


