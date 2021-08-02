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

	dataDir = '/home/yuhu/bioxpress/TCGA-Assembler/TCGA-Assembler/QuickStartExample/Part1_DownloadedData/'
	dataDir += seqType + '/*'
	pattern = glob.glob(dataDir)


	for fileList in pattern:
		print fileList
		with open(fileList, 'rb') as tsvfile:
			tsvreader = csv.reader(tsvfile, delimiter='\t', quotechar='|')
			for row in tsvreader:
				if row[1].startswith("TCGA"):
					patientId = {}
					rowList = []
					headings = row
					for i in row[1::]:
						patient = '-'.join(i.split('-')[0:3])
						sampleId = int(''.join(list(i.split('-')[3])[:-1]))
						patientId.setdefault(patient, set()).add(sampleId)
					for j in patientId:
						if all(val >= 10 for val in patientId[j]) or all(val < 10 for val in patientId[j]):
							rowList += [x for x, y in enumerate(row) if y.startswith(j)]
	
				elif row[1].startswith("raw_count") or row[1].startswith("read_count"):
					rowList2 = [i for i in rowList if row[i] == "raw_count"]
					if len(rowList2) == 0:
						rowList2 = [i for i in rowList if row[i] == "read_count"]
					heading = [headings[i] for i in rowList2]
					experiment = [''.join(i.split('-')[0:3]) for i in heading if int(''.join(list(i.split('-')[3])[:-1])) < 10]
					control = [''.join(i.split('-')[0:3]) for i in heading if int(''.join(list(i.split('-')[3])[:-1])) >= 10]
					errors1 = [i for i in experiment if i in control]
					errors2 = [i for i in control if i in experiment]
						
					if len(errors1) > 0 or len(errors2) > 0:
						print errors1, errors2


if __name__ == '__main__':
	main()
