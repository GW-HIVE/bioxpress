import csv
import glob
import os,sys
import string
import json
from optparse import OptionParser

__version__="1.0"
__status__ = "Dev"

###############################
def main():

	usage = "\n%prog  [options]"
	parser = OptionParser(usage,version="%prog " + __version__)
	parser.add_option("-t","--seqtype",action="store",dest="seqtype",help="sequencing type (RNAseq, miRNAseq)")
        parser.add_option("-i","--configfile",action="store",dest="configfile",help="Config file")


	(options,args) = parser.parse_args()
	for file in ([options.configfile,options.seqtype]):
		if not (file):
			parser.print_help()
			sys.exit(0)
	
	configJson = json.loads(open(options.configfile, "r").read())
	seqType = options.seqtype

	dataDir = configJson["deseq"]["inputdir"] + "/logs-step1/" + seqType + "/*"
        outDir = configJson["deseq"]["outputdir"] + "/logs-step2/" + seqType + "/"
	
        pattern = glob.glob(dataDir)

	for fileList in pattern:
	
		cancerType = fileList.split('/')[-1]
		if "resultscreening" in cancerType:
			platForm = cancerType.split('_')[2]
			cancerType = cancerType.split('_')[0]
			subjectFile = open(outDir + cancerType + '_' + platForm + '_subject.txt', 'w')
			treatFile = open(outDir + cancerType + '_' + platForm + '_treat.txt', 'w')
			mainFile = open(outDir + cancerType + '_' + platForm + '_DESeq2.txt', 'w')
			with open(fileList, 'rb') as tsvfile:
				tsvreader = csv.reader(tsvfile, delimiter='\t', quotechar='|')
				for row in tsvreader:
					if row[0] == 'gene_id' or row[0] == 'miRNA_ID':
						subject = []
						treat = []
						patientName = []
						for i in row[1::]:
							i = i.split('-')
							patientId = '-'.join(i[0:3])
							subject.append(patientId)
		
							sampleId = int(''.join(list(i[3])[:-1]))
							patientId += '-cancer' if sampleId < 10 else '-normal'
							treatId = 'cancer' if sampleId < 10 else 'normal'
							patientName.append(patientId)
							treat.append(treatId)
						subjectFile.write('\n'.join(subject))
						treatFile.write('\n'.join(treat))
						mainFile.write(row[0] + '\t' + '\t'.join(patientName) + '\n')
					else:
						total = 0
						for i in range(1, len(row)):
							row[i] = int(round(float(row[i])))
							total += row[i]
						if total != 0:
							newLine = row[0] + '\t' + '\t'.join(map(str,row[1::]))
							mainFile.write(newLine + '\n')
				mainFile.close()
				subjectFile.close()
				treatFile.close()

if __name__ == '__main__':
	main()

