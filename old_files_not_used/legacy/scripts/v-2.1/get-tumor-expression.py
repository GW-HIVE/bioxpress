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
	dataDir += seqType + '/*'
	outputDir = '/data/projects/bioxpress/v-2.1/generated/logs-step7/'+seqType+'/'
	pattern = glob.glob(dataDir)


	for fileList in pattern:
		print fileList
		cancerType = fileList.split('/')[-1]
		platForm = cancerType.split('__')[1]
		cancerType = cancerType.split('__')[0]
		FW = open(outputDir + cancerType + '_' + platForm +'_tumor_expression.txt', 'w')
		with open(fileList, 'rb') as tsvfile:
			tsvreader = csv.reader(tsvfile, delimiter='\t', quotechar='|')
			for row in tsvreader:
				if row[1].startswith("TCGA"):
					rowList = []
					headings = row
					patientList = set()
					for i in range(1,len(row)):
						patient = '-'.join(row[i].split('-')[0:3])
						sampleId = int(''.join(list(row[i].split('-')[3])[:-1]))
						if sampleId < 10:
							rowList += [i]
							patientList.add(patient)
	
				elif row[1].startswith("raw_count") or row[1].startswith("read_count"):
					rowList2 = [i for i in rowList if row[i] == "raw_count"]
					if len(rowList2) == 0:
						rowList2 = [i for i in rowList if row[i] == "read_count"]
					heading = [headings[i] for i in rowList2]
					heading = '\t'.join(heading)
					if len(heading) > 1:
						FW.write(headings[0] + '\t' + heading + '\n')
				else:
					newLine = [str(int(round(float(row[i])))) for i in rowList2]
					newLine = '\t'.join(newLine)
					if len(newLine) > 1:
						FW.write(row[0] + '\t' + newLine + '\n')
			print cancerType + '\t' + str(len(patientList))

						
		FW.close()

if __name__ == '__main__':
	main()
