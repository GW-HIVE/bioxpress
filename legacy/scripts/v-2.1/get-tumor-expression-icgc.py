import csv
import glob
import os,sys
import string
from optparse import OptionParser

__version__="1.0"
__status__ = "Dev"



###############################
def main():

	usage = "\n%prog  [options]"
	parser = OptionParser(usage,version="%prog " + __version__)
	parser.add_option("-t","--seqtype",action="store",dest="seqtype",help="sequencing type (RNAseq, miRNAseq)")


        (options,args) = parser.parse_args()
        for file in ([options.seqtype]):
                if not (file):
                        parser.print_help()
                        sys.exit(0)
	
        seqType = options.seqtype

	seqData = "mirna" if seqType == "miRNAseq" else "exp"

	dataFile = '/mnt/external-1/projects/bioxpress/downloads/icgc/' + seqData + '_seq.tsv'
	outputDir = '/data/projects/bioxpress/generated/logs-step7/'+seqType+'/'

	with open(dataFile, 'rb') as tsvfile:
		tsvreader = csv.reader(tsvfile, delimiter='\t', quotechar='|')
		geneList = {}
		patientList = {}
		for row in tsvreader:
			if not row[0].startswith("icgc_donor_id"):
				geneId = row[7].lower() #if seqType == "RNAseq" else row[7].split('mature')[0]
				cancerType = row[1].split('-')[0]
				if cancerType not in geneList:
					geneList[cancerType] = {}
				if geneId not in geneList[cancerType]:
					geneList[cancerType][geneId] = {}
				rawReads = row[9]

				if row[0] in geneList[cancerType][geneId] and len(geneList[cancerType][geneId][row[0]]) < len(rawReads):
					geneList[cancerType][geneId][row[0]] = rawReads
				if row[0] not in geneList[cancerType][geneId]:
					geneList[cancerType][geneId][row[0]] = rawReads

				patientList.setdefault(cancerType, set()).add(row[0])

	for cancerType in geneList:
		FW = open(outputDir + cancerType + '__icgc_tumor_expression.txt', 'w')
		FW.write('geneId\t' + '\t'.join(patientList[cancerType]) + '\n')

		for geneId in geneList[cancerType]:
			newLine = geneId
			for patId in patientList[cancerType]:
				if patId in geneList[cancerType][geneId]:
					newLine += '\t' + geneList[cancerType][geneId][patId]
				else:
					newLine += '\t0'
			FW.write(newLine + '\n')
				
		print cancerType + '\t' + str(len(patientList[cancerType]))

						
	FW.close()

if __name__ == '__main__':
	main()
