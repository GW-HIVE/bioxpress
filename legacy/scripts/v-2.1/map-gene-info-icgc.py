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

	oriDir = '/data/projects/bioxpress/generated/logs-step7/' + seqType + '/*_icgc_*.txt'
	outputDir = '/data/projects/bioxpress/generated/logs-step9/' + seqType + '/'
	referDir = '/data/projects/bioxpress/generated/reference/gene2ensembl'
	referUniprot = '/data/projects/bioxpress/generated/reference/HUMAN_9606_idmapping.dat'
	FW = open(outputDir + seqType + '_icgc_transcript_information.txt', 'w')
        oriPattern = glob.glob(oriDir)

	wholeTranscript = {}
	for fileList in oriPattern:
#		print fileList
		with open(fileList, 'rb') as tsvfile:
			tsvreader = csv.reader(tsvfile, delimiter='\t', quotechar='|')
			for row in tsvreader:
				if row[0] != "geneId":
					geneId = row[0].upper().split('.')[0]
					wholeTranscript[geneId] = ""
	print len(wholeTranscript)

	with open(referDir, 'rb') as tsvfile:
		tsvreader = csv.reader(tsvfile, delimiter='\t', quotechar='|')
		for row in tsvreader:
			if row[0] == "9606" and row[2].split('.')[0].upper() in wholeTranscript:
				wholeTranscript[row[2].split('.')[0].upper()] = '\t'.join(row[2::])

	with open(referUniprot, 'rb') as tsvfile:
		tsvreader = csv.reader(tsvfile, delimiter='\t', quotechar='|')
		for row in tsvreader:
			if row[1] == "Gene_Name" and row[2].upper() in wholeTranscript:
				wholeTranscript[row[2].upper()] = row[0]
			if row[1] == "UniProtKB-ID" and row[2].upper().split('_')[0] in wholeTranscript:
				wholeTranscript[row[2].upper().split('_')[0]] = row[0]
			if row[1] == "Ensembl" and row[2].upper().split('_')[0] in wholeTranscript:
				wholeTranscript[row[2].upper().split('_')[0]] = row[0].split('-')[0]


	nameList = ['GeneID','refseqNuc','refseqProtein','ensembleGeneId','ensembleRNAId','ensembleProteinId','geneName']
	FW.write('\t'.join(nameList) + '\n')
	for key in wholeTranscript:
		if wholeTranscript[key] != "":

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


				


