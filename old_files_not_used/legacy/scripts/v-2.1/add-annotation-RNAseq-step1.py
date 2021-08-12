import csv
import glob
import os,sys
import string
from optparse import OptionParser

__version__="1.0"
__status__ = "Dev"



###############################
def main():

	seqType = "RNAseq"

	oriDir = '/data/projects/bioxpress/generated/logs-step1/' + seqType + '/*.txt'
	outputDir = '/data/projects/bioxpress/generated/logs-step9/' + seqType + '/'
	referDir = '/data/projects/bioxpress/generated/reference/gene2ensembl'
	FW = open(outputDir + seqType + '_transcript_information.txt', 'w')
        oriPattern = glob.glob(oriDir)

	wholeTranscript = {}
	for fileList in oriPattern:
		print fileList
		with open(fileList, 'rb') as tsvfile:
			tsvreader = csv.reader(tsvfile, delimiter='\t', quotechar='|')
			for row in tsvreader:
				if row[0] != "gene_id":
					geneId = row[0].split('|')[1]
					wholeTranscript[geneId] = {}
					wholeTranscript[geneId]["geneName"] = row[0].split('|')[0]
	print len(wholeTranscript)

	with open(referDir, 'rb') as tsvfile:
		tsvreader = csv.reader(tsvfile, delimiter='\t', quotechar='|')
		for row in tsvreader:
			if row[0] == "9606" and row[1] in wholeTranscript:
				if row[2] != "-" and row[3] != "-" and row[4] != "-" and row[5] != "-" and row[6] != "-":
					wholeTranscript[row[1]].setdefault("ensembleGeneId", set()).add(row[2])
					wholeTranscript[row[1]].setdefault("ensembleRNAId", set()).add(row[4])
					wholeTranscript[row[1]].setdefault("ensembleProteinId", set()).add(row[6])
					wholeTranscript[row[1]].setdefault("refseqNuc", set()).add(row[3])
					wholeTranscript[row[1]].setdefault("refseqProtein", set()).add(row[5])

	nameList = ['GeneID','refseqNuc','refseqProtein','ensembleGeneId','ensembleRNAId','ensembleProteinId','geneName']
	FW.write('\t'.join(nameList) + '\n')
	for key in wholeTranscript:
		newLine = key + '\t'
		for i in nameList[1::]:
			if i in wholeTranscript[key]:
				if i == "geneName":
					newLine += wholeTranscript[key][i]
				else:
					newLine += ';'.join(wholeTranscript[key][i])
			else:
				newLine += '-'
			newLine += '\t'

		FW.write(newLine.strip() + '\n')

	FW.close()

if __name__ == '__main__':
        main()


				


