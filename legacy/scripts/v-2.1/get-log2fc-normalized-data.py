import csv
import glob
import os,sys
import string
import numpy
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

        dataDir = '/data/projects/bioxpress/generated/logs-step1/' + seqType + '/*_normalized_data.txt'
        outputDir = '/data/projects/bioxpress/generated/logs-step-normalized/' + seqType + '/'
        pattern = glob.glob(dataDir)

	for fileList in pattern:
		print fileList
		cancerType = fileList.split('/')[-1]
		platForm = cancerType.split('_')[2]
		cancerType = cancerType.split('_')[0]
		mainFile = open(outputDir + cancerType + '_' + platForm + '_log2fc_per_patient.txt', 'w')
		with open(fileList, 'rb') as tsvfile:
			tsvreader = csv.reader(tsvfile, delimiter='\t', quotechar='|')
			subjectLog2fc = {}
			geneIdList = set()
			heading = set()
			for row in tsvreader:
				if row[0] == 'gene_id' or row[0] == 'miRNA_ID':
					subject = {}
					for i in range(1, len(row)):
						vector = row[i].split('-')
						patientId = '-'.join(vector[0:3])
						heading.add(patientId)
						sampleId = int(''.join(list(vector[3])[:-1]))
						sample = 'cancer' if sampleId < 10 else 'normal'
						if patientId not in subject:
							subject[patientId] = {}
						subject[patientId].setdefault(sample, set()).add(str(i))
				else:
					for key in subject:
						cancer = list(subject[key]["cancer"])
						for i in range(0,len(cancer)):
							cancer[i] = float(row[int(cancer[i])])
						normal = list(subject[key]["normal"])
						for i in range(0, len(normal)):
							normal[i] = float(row[int(normal[i])])
						meanNormal = 0.000001 if sum(normal) == 0 else numpy.mean(normal)
						log2fc = numpy.log2(numpy.mean(cancer) / meanNormal)
						if row[0] not in subjectLog2fc:
							subjectLog2fc[row[0]] = {}
						subjectLog2fc[row[0]][key] = log2fc
					geneIdList.add(row[0])

		mainFile.write('transcriptId,' + ','.join(heading) + '\n')
		for geneId in geneIdList:
			row = geneId
			for patId in heading:
				if str(subjectLog2fc[geneId][patId]).find("inf") >= 0:
					subjectLog2fc[geneId][patId] = "0"
				row += ',' + str(subjectLog2fc[geneId][patId])
			mainFile.write(row + '\n')
		mainFile.close()

if __name__ == '__main__':
	main()

