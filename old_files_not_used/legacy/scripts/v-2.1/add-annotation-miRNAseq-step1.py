import csv
import glob
import os,sys
import string
from optparse import OptionParser

__version__="1.0"
__status__ = "Dev"



###############################
def main():

	seqType = "miRNAseq"

	oriDir = '/data/projects/bioxpress/generated/logs-step1/' + seqType + '/*.txt'
	outputDir = '/data/projects/bioxpress/generated/logs-step9/' + seqType + '/'
	referDir = '/data/projects/bioxpress/generated/reference/hsa.gff3'
	FW = open(outputDir + seqType + '_transcript_information.txt', 'w')
        oriPattern = glob.glob(oriDir)

	wholeTranscript = {}
	for fileList in oriPattern:
		print fileList
		with open(fileList, 'rb') as tsvfile:
			tsvreader = csv.reader(tsvfile, delimiter='\t', quotechar='|')
			for row in tsvreader:
				if row[0] != "gene_id" and row[0] != "miRNA_ID":
					wholeTranscript[row[0].lower()] = set()
	print len(wholeTranscript)

	with open(referDir, 'rb') as tsvfile:
		tsvreader = csv.reader(tsvfile, delimiter='\t', quotechar='|')
		for row in tsvreader:
			if not row[0].startswith('#') and row[2] == "miRNA_primary_transcript":
				nameList = row[-1].split(';')
				miRNA = nameList[2].split('=')[1]
				mirbase = nameList[0].split('=')[1]
				pos = row[0] + '\t' + row[3] + '\t' + row[4] + '\t' + row[6]

				if miRNA in wholeTranscript:
					wholeTranscript.setdefault(miRNA, set()).add(mirbase + '\t' + pos)

	nameList = ['miRNAID','miRBaseAc','chrom','start','end']
	FW.write('\t'.join(nameList) + '\n')
	for key in wholeTranscript:
		newLine = key + '\t'
		if len(wholeTranscript[key]) > 1:
			print wholeTranscript[key]
		else:
			if len(wholeTranscript[key]) < 1:
				print key
				newLine += '-\t-\t-\t-\t-'
			else:
				newLine += list(wholeTranscript[key])[0]

		FW.write(newLine + '\n')

	FW.close()

if __name__ == '__main__':
        main()


				


