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

	inputDir = '/data/projects/bioxpress/generated/logs-step9/' + seqType + '/'
	inputFile = inputDir + 'miRNAseq_transcript_information.txt'
	referHgnc = '/data/projects/bioxpress/generated/reference/RNA_micro.txt'
	FW = open(inputDir + seqType + '_transcript_information_final.txt', 'w')

	wholeTranscript = {}
	with open(inputFile, 'rb') as tsvfile:
		tsvreader = csv.reader(tsvfile, delimiter='\t', quotechar='|')
		for row in tsvreader:
			if row[0] != "miRNAID":
				geneId = row[0].lower()
				wholeTranscript[geneId] = '\t'.join(row)
	print len(wholeTranscript)

	hgncList = {}
	j = 0
	with open(referHgnc, 'rb') as tsvfile:
		tsvreader = csv.reader(tsvfile, delimiter='\t', quotechar='|')
		for row in tsvreader:
			if row[0] != "hgnc_id":
				symbo = row[8].lower().split('|')
				for i in symbo:
					if i in wholeTranscript and i not in hgncList:
						wholeTranscript[i] += '\t' + row[1] + '\t' + row[19]
						hgncList[i] = 1
						j += 1

	print len(hgncList)
	print j

	nameList = ['miRNAID','miRBaseAc','chrom','start','end','strand','hgncSymbl','ensemblID']
	FW.write('\t'.join(nameList) + '\n')
	for key in wholeTranscript:
		if len(wholeTranscript[key].split('\t')) <= 6:
			newLine = wholeTranscript[key] + '\t-\t-'
		else:
			newLine = wholeTranscript[key]
		FW.write(newLine + '\n')

	FW.close()


if __name__ == '__main__':
        main()


				


