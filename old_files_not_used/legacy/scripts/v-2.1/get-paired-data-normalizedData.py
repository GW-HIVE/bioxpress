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
	outputDir = '/home/yuhu/bioxpress/TCGA-Assembler/TCGA-Assembler/QuickStartExample/Part1_DownloadedData/pairedData'+seqType+'/'
	pattern = glob.glob(dataDir)


	for fileList in pattern:
		print fileList
		cancerType = fileList.split('/')[-1]
		platForm = cancerType.split('__')[1]
		cancerType = cancerType.split('__')[0]
		FW = open(outputDir + cancerType + '_' + platForm +'_normalized_data.txt', 'w')
		with open(fileList, 'rb') as tsvfile:
			tsvreader = csv.reader(tsvfile, delimiter='\t', quotechar='|')
			for row in tsvreader:
				if row[1].startswith("TCGA"):
					patientId = {}
					rowList = []
					headings = row
					patientCount = 0
					for i in row[1::]:
						patient = '-'.join(i.split('-')[0:3])
						sampleId = int(''.join(list(i.split('-')[3])[:-1]))
						patientId.setdefault(patient, set()).add(sampleId)
					for j in patientId:
						if not all(val >= 10 for val in patientId[j]) and not all(val < 10 for val in patientId[j]):
							rowList += [x for x, y in enumerate(row) if y.startswith(j)]
							patientCount += 1
	
				elif row[1].startswith("raw_count") or row[1].startswith("read_count"):
					rowList2 = [i for i in rowList if row[i] == "scaled_estimate"]
					if len(rowList2) == 0:
						rowList2 = [i for i in rowList if row[i] == "reads_per_million_miRNA_mapped"]
					heading = [headings[i] for i in rowList2]
					heading = '\t'.join(heading)
					if len(heading) > 1:
						FW.write(headings[0] + '\t' + heading + '\n')
				else:
					newLine = [row[i] for i in rowList2]
					newLine = '\t'.join(newLine)
					if len(newLine) > 1:
						FW.write(row[0] + '\t' + newLine + '\n')
			print cancerType + '\t' + str(patientCount)

						
		FW.close()

if __name__ == '__main__':
	main()
