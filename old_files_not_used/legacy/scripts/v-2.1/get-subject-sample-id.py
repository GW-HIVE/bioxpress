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

        dataDir = '/mnt/external-1/projects/bioxpress/downloads/tcga/'
        dataDir += seqType + '/*__*.txt'
	referenceFile = open('/data/projects/bioxpress/v-2.1/generated/logs-step14/BioXpress_cancer_addUberon.txt')
        outputDir = '/data/projects/bioxpress/v-2.1/generated/logs-step15/' + seqType + '/'
	outputFile = open(outputDir + 'sample_subject_tissue_list.txt', 'w')
        pattern = glob.glob(dataDir)

	cancerTissue = {}
	for row in referenceFile:
		row = row.strip().split('\t')
		if row[1] != '-':
			cancerTissue[row[1]] = row[-1]
	referenceFile.close()

	for fileList in pattern:
		print fileList
		cancerType = fileList.split('/')[-1]
		cancerType = cancerType.split('_')[0]
		with open(fileList, 'rb') as tsvfile:
			tsvreader = csv.reader(tsvfile, delimiter='\t', quotechar='|')
			for row in tsvreader:
				if row[1].find("TCGA") >= 0:
					subject = []
					patientName = []
					for i in row[1::]:
						sampleId = i
						i = i.split('-')
						subjectId = '-'.join(i[0:3])
		
						sampleNum = int(''.join(list(i[3])[:-1]))
						sampleType = 'cancer' if sampleNum < 10 else 'normal'
						newLine = cancerTissue[cancerType] + '\t' + cancerType + '\t'
						newLine += subjectId + '\t' + sampleId + '\t'
						newLine += sampleType + '\n'
						outputFile.write(newLine)
	outputFile.close()

if __name__ == '__main__':
	main()

