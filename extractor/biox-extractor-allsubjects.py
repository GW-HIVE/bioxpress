import os,sys
import string
import json
from optparse import OptionParser
import csv
import glob

__version__="1.0"
__status__ = "Dev"


###############################
def main():

	usage = "\n%prog  [options]"
        parser = OptionParser(usage,version="%prog " + __version__)
        parser.add_option("-i","--configfile",action="store",dest="configfile",help="Config file")
        parser.add_option("-r","--rsrcname",action="store",dest="rsrcname",help="Source name")
	parser.add_option("-c","--cancertype",action="store",dest="cancertype",help="Cancer type")



        (options,args) = parser.parse_args()
        for file in ([options.configfile, options.rsrcname, options.cancertype]):
                if not (file):
                        parser.print_help()
                        sys.exit(0)

        rsrcName = options.rsrcname
        cancerType = options.cancertype
	configJson = json.loads(open(options.configfile, "r").read())


        dataDir = configJson["extractor"]["inputdir"] + rsrcName + "/RNAseq/"
        outDir = configJson["extractor"]["outputdir"]
	
	pattern = dataDir + "*__gene_RNAseq__tissueTypeAll__*.txt"
	tsvFileList = glob.glob(pattern)
	for tsvFile in tsvFileList:
        	fileName = os.path.basename(tsvFile)
        	cancerType_Tmp = fileName.split("_")[0]
        	if cancerType==cancerType_Tmp:
                	break

	inFile = dataDir + fileName 
        pairingFile = outDir + rsrcName + "-" + cancerType + "-samplepairing.csv"
	outFile = outDir + rsrcName + "-" + cancerType + "-extract-all-even.csv"
	

	subjects = []
	subjects.append("")	
	sampleList = []

	with open(pairingFile, 'r') as csvfile:
                csvReader = csv.reader(csvfile, delimiter=',', quotechar='|')
		rowCount = 0
                seen = {}
                for row in csvReader:                 
			subjects.append(row[0]+"-normal")
			subjects.append(row[0]+"-tumor")
			sampleList.append([row[1],row[2]])
						

	dataGrid={}
	with open(inFile, 'r') as csvfile:
        	csvReader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        	rowCount = 0
		for row in csvReader:
			rowCount += 1
			if rowCount == 1:
				fieldList = row
			elif rowCount == 2:
				continue
			else:
				geneId = row[0]
				dataGrid[geneId] = {}
				for i in xrange(1,len(row)):
					if i%2 == 1:
						dataGrid[geneId][fieldList[i]]=row[i]
	
	firstRow = subjects
	with open(outFile, 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(firstRow)
		for geneId in dataGrid:
			row=[geneId]		
			for sample in sampleList:
				row.append(dataGrid[geneId][sample[0]])
				row.append(dataGrid[geneId][sample[1]])	
			writer.writerow(row)

	print "done!"

if __name__ == '__main__':
        main()


