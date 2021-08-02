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

	inputDir = '/data/projects/bioxpress/generated/logs-step9/' + seqType + '/'
	inputFile = inputDir + 'RNAseq_transcript_information.txt'
	referReviewed = '/data/projects/bioxpress/generated/reference/uniprot-organism:-Homo+sapiens+%5B9606%5D-+AND+reviewed:yes.list'
	referIdMapping = '/data/projects/bioxpress/generated/reference/HUMAN_9606_idmapping.dat'
	FW = open(inputDir + seqType + '_transcript_information_final.txt', 'w')

	wholeTranscript = {}
	stepOneLen = {}
	geneName = {}
	with open(inputFile, 'rb') as tsvfile:
		tsvreader = csv.reader(tsvfile, delimiter='\t', quotechar='|')
		for row in tsvreader:
			if row[1] != "GeneID":
				geneId = row[0]
				geneName[row[-1]] = 1
				stepOneLen[len(row)] = 1
				wholeTranscript[geneId] = '\t'.join(row)
	print len(wholeTranscript)
	print stepOneLen

	reviewedList = {}
	with open(referReviewed, 'rb') as tsvfile:
		tsvreader = csv.reader(tsvfile, delimiter='\t', quotechar='|')
		for row in tsvreader:
			reviewedList[row[0]] = 1

	uniprotList1 = {}
	uniprotList2 = {}
	uniprotList3 = {}

	with open(referIdMapping, 'rb') as tsvfile:
		tsvreader = csv.reader(tsvfile, delimiter='\t', quotechar='|')
		for row in tsvreader:
			row[0] = row[0].split('-')[0]
			if row[1] == "GeneID" and row[0] in reviewedList and row[2] in wholeTranscript:
				uniprotList1.setdefault(row[2], set()).add(row[0])
			if row[1] == "Gene_Name" and row[0] in reviewedList:
				uniprotList2[row[0]] = row[2]
			if row[1] == "UniProtKB-ID" and row[0] in reviewedList:
				uniprotList3[row[0]] = row[2].split('_')[0]

	stepTwoLen = {}
	nameList = ['GeneID','refseqNuc','refseqProtein','ensembleGeneId','ensembleRNAId','ensembleProteinId','geneName', 'uniprotKB']
	FW.write('\t'.join(nameList) + '\n')
	for key in wholeTranscript:
		if key not in uniprotList1:
			newLine = wholeTranscript[key] + '\t-'
			FW.write(newLine + '\n')
		else: #This part is very complicated due to the trade off from UniProt (multiple UniProt IDs map to one gene name, please read README for the steps of the trade off)
			uniprotAc = uniprotList1[key]
			count = 0
			uniprotId = []
			for i in uniprotAc:
				geneNameUniprot = uniprotList2[i] if i in uniprotList2 else uniprotList3[i]
				geneNameOri = wholeTranscript[key].split('\t')[-1]
				if geneNameOri == geneNameUniprot:
					uniprotId += [i]
					count += 1
			if count == 1:
				newLine = wholeTranscript[key] + '\t' + uniprotId[0]
				FW.write(newLine + '\n')
			elif count > 1:
				for j in uniprotId:
					if uniprotList3[j] == wholeTranscript[key].split('\t')[-1]:
						newLine = wholeTranscript[key] + '\t' + j
						FW.write(newLine + '\n')
						count = 1
				if count > 1:
					newLine = wholeTranscript[key] + '\t' + sorted(uniprotId)[0]
					FW.write(newLine + '\n')

			if count == 0 and len(uniprotAc) == 1:
				uniprotId = list(uniprotAc)[0]
				geneNameUniprot = uniprotList2[uniprotId] if uniprotId in uniprotList2 else uniprotList3[uniprotId]
				newLine = '\t'.join(wholeTranscript[key].split('\t')[:-1]) + '\t' + geneNameUniprot + '\t' + uniprotId
				FW.write(newLine + '\n')
			elif count == 0 and len(uniprotAc) > 1:
				newLine = '\t'.join(wholeTranscript[key].split('\t')[:-1]) + '\t' + uniprotList2[sorted(uniprotAc)[0]] + '\t' + sorted(uniprotAc)[0]
				FW.write(newLine + '\n')

	FW.close()


if __name__ == '__main__':
        main()


				


