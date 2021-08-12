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
	statsDir = '/data/projects/bioxpress/generated/logs-step1/' + seqType + '/logs-step1-stat-*.txt'
	oriDir = '/data/projects/bioxpress/generated/logs-step1/' + seqType + '/*_resultscreening.txt'
	dataDir = '/data/projects/bioxpress/generated/logs-step5/' + seqType + '/*_patient_DESeq2.txt'
	outputDir = '/data/projects/bioxpress/generated/logs-step6/'+seqType+'/'
	pattern = glob.glob(dataDir)
	oriPattern = glob.glob(oriDir)

	statsDic = {}
	for stats in glob.glob(statsDir):
		statsFile = open(stats, 'rb')
		for row in statsFile:
			if row.startswith("/home/yuhu/bioxpress/TCGA-Assembler/TCGA-Assembler"):
				row = row.split('/')[-1].split('_')
				cancerType = row[0]
				platForm = row[3]
				statsDic[cancerType + ',' + platForm] = str(0)
			elif row.split('\t')[0] == cancerType:
				statsDic[cancerType + ',' + platForm] = row.split('\t')[1]
			else:
				print row.strip()

		statsFile.close()

	for fileList in oriPattern:
		print fileList
		categories = fileList.split('/')[-1].split('_')
		cancerType = categories[0]
		platForm = categories[2]

		geneList = {}
		with open(fileList, 'rb') as tsvfile:
			tsvreader = csv.reader(tsvfile, delimiter = '\t', quotechar = '|')
			for row in tsvreader:
				if row[0] != "miRNA_ID" and row[0] != "gene_id":
					geneList[row[0]] = {}

		FW = open(outputDir + cancerType + '_' + platForm +'_patient_frequency.txt', 'w')
		totalCount = statsDic[cancerType + ',' + platForm]

		for patientList in pattern:
			patCancerType,patPlatForm = patientList.split('/')[-1].split('_')[0:2]
			if patCancerType == cancerType and patPlatForm == platForm:
				with open(patientList, 'rb') as csvfile:
					csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
					for row in csvreader:
						if row[0] != "geneName":
							geneName = row[0]
							expre = row[2]
							geneList[row[0]].setdefault(expre, set()).add(row[4])
		FW.write("geneName,up,down,total\n")
		for key in geneList:
			if "Up" in geneList[key] and "Down" in geneList[key]:
				FW.write(key + ',' + str(len(geneList[key]["Up"])) + ',' + str(len(geneList[key]["Down"])) + ',' + totalCount.strip() + '\n')
			elif "Up" not in geneList[key] and  "Down" in geneList[key]:
				FW.write(key + ',0,' + str(len(geneList[key]["Down"])) + ',' + totalCount.strip() + '\n')
			elif "Down" not in geneList[key] and "Up" in geneList[key]:
				FW.write(key + ',' + str(len(geneList[key]["Up"])) + ',0,' + totalCount.strip() + '\n')
			else:
				FW.write(key + ',0,0,' + totalCount.strip() + '\n')

		FW.close()
						

if __name__ == '__main__':
	main()
				


