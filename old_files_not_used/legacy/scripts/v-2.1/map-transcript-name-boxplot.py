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

	dataDir = '/data/projects/bioxpress/generated/logs-step8/' + seqType + '/*_tumor_boxplot.txt'
	outputDir = '/data/projects/bioxpress/generated/logs-step12/'+seqType+'/'
	geneInfoFile = '/data/projects/bioxpress/generated/logs-step9/'+seqType
	geneInfoFile +='/' + seqType + '_transcript_information_final.txt'

	pattern = glob.glob(dataDir)

	heading1 = "geneName,cancerType,platForm,min,25%,50%,75%,max\n"
	heading2 = "miRNAName,cancerType,platForm,min,25%,50%,75%,max\n"

	heading = heading1 if seqType == "RNAseq" else heading2

	referDic = {}
	with open(geneInfoFile, 'rb') as tsvfile:
		tsvreader = csv.reader(tsvfile, delimiter = '\t', quotechar="|")
		for row in tsvreader:
			referDic[row[0]] = row[-2] if seqType == "RNAseq" else row[0]

	FW = open(outputDir + 'Bioxpress_tumor_boxplot_mapped_transcript_name.txt', 'w')
	FW.write(heading)

	for fileList in pattern:
		if fileList.find("_icgc_") == -1:
			print fileList
			categories = fileList.split('/')[-1].split('_')
			cancerType = categories[0]
			platForm = categories[1]
			with open(fileList, 'rb') as csvfile:
				csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
				for row in csvreader:
					if not row[0].startswith('"TCGA'):
						geneId = row[0].split("|")[-1] if seqType == "RNAseq" else row[0]
						if geneId in referDic:
							newRow = '%s,%s\n' % (referDic[geneId],','.join(row[1::]))
							FW.write(newRow)
						else:
							print geneId
	FW.close()


if __name__ == '__main__':
        main()


				


