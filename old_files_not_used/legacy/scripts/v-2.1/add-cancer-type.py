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


	inputFile = '/data/projects/bioxpress/v-2.1/generated/logs-step10/' + seqType + '/cancer_wise_DESeq2.txt'
	outputDir = '/data/projects/bioxpress/v-2.1/generated/logs-step11/' + seqType + '/'
	referFile = open('/data/projects/bioxpress/v-2.1/generated/reference/reference.txt')
	patFreqDir = '/data/projects/bioxpress/v-2.1/generated/logs-step6/' + seqType + '/*_patient_frequency.txt'
	manualFile = open('/data/projects/bioxpress/v-2.1/generated/logs-step9/RNAseq_manually_transcript_information_final.txt')

	FW = open(outputDir + seqType + '_BioXpress_version_3.txt', 'w')
	patFreqPattern = glob.glob(patFreqDir)

	patFreqDic = {}
	for fileList1 in patFreqPattern:
		fileList = fileList1.split('/')[-1]
		categories = fileList.split('_')
		cancerType = categories[0]
		platForm = categories[1]

		with open(fileList1, 'rb') as csvfile:
			csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
			for row in csvreader:
				geneId = row[0].split('|')[-1] if seqType == "RNAseq" else row[0]
				expre = row[1] + '(Up)/' + row[2] + '(Down)'
				total = row[3]
				key = cancerType + ',' + platForm
			
				if geneId in patFreqDic:
					patFreqDic[geneId][key] = expre + ',' + total
				else:
					patFreqDic[geneId] = {}
					patFreqDic[geneId][key] = expre + ',' + total

	cancerDic = {}
	for row in referFile:
		row = row.strip().split('\t')
		cancerDic[row[0]] = row[1]
	referFile.close()
	
	with open(inputFile, 'rb') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in csvreader:
			if row[0] == "miRNAID" or row[0] == "GeneID":
				heading = ','.join(row) + ',patientFreq,totalPatient,doidCancerType,PMID'
				FW.write(heading + '\n')
			else:
				newLine = ",".join(row)
				geneId = row[0]
				cancerType = row[10]
				platForm = row[11]
				key = cancerType + ',' + platForm
				if geneId in patFreqDic:
					if key in patFreqDic[geneId]:
						newLine += ',' + patFreqDic[geneId][key] + ',' + cancerDic[row[10]]
						FW.write(newLine + ',-\n')
					else:
						print key
				else:
					print "geneId not match", geneId, cancerType,platForm

	if seqType == "RNAseq":
		for row in manualFile:
			if not row.startswith("GeneID"):
				row = row.strip().split(',')
				newRow = ','.join(row[0:6]) + ',' + row[7] +',' + row[6] + ',' + row[8] + ',' + row[12] + ',' + row[13] + ',' + row[16] + ',' + row[9] + ',' + row[10] + ',-,-,' + row[14] + ',' + row[-1]
				FW.write(newRow + '\n')

	FW.close()
	manualFile.close()

if __name__ == '__main__':
        main()


				


