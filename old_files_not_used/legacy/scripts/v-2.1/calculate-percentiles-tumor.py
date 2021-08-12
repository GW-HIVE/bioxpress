import csv
import glob
import os,sys
import string
from optparse import OptionParser
import numpy as np

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
	seqPlatForm = "RNAseq" if seqType == "RNAseq" else ".hg19.mirbase20"

	dataDir = '/data/projects/bioxpress/generated/logs-step8/'+seqType+'/*'+seqPlatForm+'_normailzed_dds_tumor_expression.csv'
	outputDir = '/data/projects/bioxpress/generated/logs-step8/'+seqType+'/'
	pattern = glob.glob(dataDir)


	for fileList in pattern:
		print fileList
		cancerType = fileList.split('/')[-1]
		platForm = cancerType.split('_')[1]
		cancerType = cancerType.split('_')[0]
		FW = open(outputDir + cancerType + '_' + platForm +'_tumor_boxplot.txt', 'w')
		with open(fileList, 'rb') as csvfile:
			csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
			for row in csvreader:
				if not row[0].startswith('"TCGA.'):
					arrayList = map(float, row[1::])
					row[0] = row[0].split('"')[1]
					expreNum = [n for n,j in enumerate(arrayList) if j != 0]
					freq = str(len(expreNum)) + '/' + str(len(arrayList)) + '(' + str(round(len(expreNum)*100.0/len(arrayList),1)) + '%)'
					a = np.array(arrayList)
					minValue = min(a)
					p1 = np.percentile(a, 25)
					p2 = np.percentile(a, 50)
					p3 = np.percentile(a, 75)
					maxValue = max(a)
					FW.write(row[0] + ',' + cancerType + ',' + platForm + ',' + freq + ',' + str(minValue)  + ',' + str(p1) + ',' + str(p2) + ',' + str(p3) + ',' + str(maxValue) + '\n')
				else:
					FW.write(','.join(row) + '\n')

		FW.close()

if __name__ == '__main__':
	main()
