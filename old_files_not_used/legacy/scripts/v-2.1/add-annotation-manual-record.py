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

	manualFile = open('/data/projects/bioxpress/generated/reference/BioXpress_manually.txt')
	referIdMapping = '/data/projects/bioxpress/generated/reference/HUMAN_9606_idmapping.dat'
	referFile = '/data/projects/bioxpress/generated/reference/gene2ensembl'
	inputDir = '/data/projects/bioxpress/generated/logs-step9/'
	FW = open(inputDir + seqType + '_manually_transcript_information_final.txt', 'w')

	wholeTranscript = {}
	for row in manualFile:
		row = row.strip().split(',')
		uniprotId = row[0]
		wholeTranscript.setdefault(uniprotId, set()).add(','.join(row[3::]))
	print len(wholeTranscript)

	geneIdDic = {}
	geneNameDic = {}
	with open(referIdMapping, 'rb') as tsvfile:
		tsvreader = csv.reader(tsvfile, delimiter='\t', quotechar='|')
		for row in tsvreader:
			if row[0].split('-')[0] in wholeTranscript and row[1] == "GeneID":
				geneIdDic[row[2]] = row[0]
			if row[0].split('-')[0] in wholeTranscript and row[1] == "Gene_Name":
				geneNameDic[row[0]] = row[2]

	i = 0
	transcriptName = {}
	with open(referFile, 'rb') as tsvfile:
		tsvreader = csv.reader(tsvfile, delimiter='\t', quotechar='|')
		for row in tsvreader:
			if row[0] == "9606" and row[1] in geneIdDic:
				if not row[1] in transcriptName:
					transcriptName[row[1]] = {}
				transcriptName[row[1]].setdefault("ensembleGeneId", set()).add(row[2])
				transcriptName[row[1]].setdefault("ensembleRNAId", set()).add(row[4])
				transcriptName[row[1]].setdefault("ensembleProteinId", set()).add(row[6])
				transcriptName[row[1]].setdefault("refseqNuc", set()).add(row[3])
				transcriptName[row[1]].setdefault("refseqProtein", set()).add(row[5])
				i += 1

	print i

	nameList = ['GeneID','refseqNuc','refseqProtein','ensembleGeneId','ensembleRNAId','ensembleProteinId','uniprotKB','geneName', 'log2FoldChange','p_value','adjusted_p_value','Significant','Expression','TCGACancer','Cancer_Ontology','#Patients','Data_Source','PMID']
	FW.write(','.join(nameList) + '\n')
	for key in transcriptName:
		newLine = key + ','
                for i in nameList[1:6]:
                        if i in transcriptName[key]:
                                newLine += ';'.join(transcriptName[key][i])
                        else:
                                newLine += '-'
                        newLine += ','

		allInfo = wholeTranscript[geneIdDic[key]]
		for j in allInfo:
			newLine1 = newLine + geneIdDic[key] + ',' + geneNameDic[geneIdDic[key]] + ',' + j
			FW.write(newLine1 + '\n')

	FW.close()


if __name__ == '__main__':
        main()


				


