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

	oriDir = '/data/projects/bioxpress/generated/logs-step1/' + seqType + '/*_resultscreening.txt'
	dataDir = '/data/projects/bioxpress/generated/logs-step4/' + seqType + '/*_DESeq_results_new.csv'
	outputDir = '/data/projects/bioxpress/generated/logs-step5/'+seqType+'/'
	pattern = glob.glob(dataDir)
	oriPattern = glob.glob(oriDir)

	for fileList in oriPattern:
		print fileList
		categories = fileList.split('/')[-1].split('_')
		cancerType = categories[0]
		platForm = categories[2]

		FW = open(outputDir + cancerType + '_' + platForm +'_patient_DESeq2.txt', 'w')
		FW.write("geneName,log2FC,expression,cancerType,patientId,platForm,pValue,adjPValue\n")

		for patientList in pattern:
			patCancerType,patientId,patPlatForm = patientList.split('/')[-1].split('_')[0:3]
			if patCancerType == cancerType and patPlatForm == platForm:
				with open(patientList, 'rb') as csvfile:
					csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
					for row in csvreader:
						if row[0] != '"baseMean"':
							geneName = row[0].split('"')[1]
							logFc = row[2]
							if logFc != "NA":
								expre = "Up" if float(logFc) >= 0.5 else "Down" if float(logFc) <= -0.5 else "-"
							else:
								expre = "-"
							pValue = row[5]
							adjPValue = row[6]
							newRow = '%s,%s,%s,%s,%s,%s,%s,%s\n' % (geneName,logFc,expre,patCancerType,patientId,patPlatForm,pValue,adjPValue)
							FW.write(newRow)
		FW.close()

if __name__ == '__main__':
        main()


				


