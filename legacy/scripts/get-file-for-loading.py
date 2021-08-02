import csv
import glob
import os,sys
import string
from optparse import OptionParser
import sys
import decimal as Decimal


__version__="1.0"
__status__ = "Dev"

###############################
def decimalChange(i):
	if i != "NA" and i != '-':
		a = format(float(i),'.500f')
		i = format(float(a),'.2e')
	return i


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

	inputDir = '/data/projects/bioxpress/v-2.1/generated/logs-step11/' + seqType + '/*'
	outputDir = '/data/projects/bioxpress/v-2.1/generated/logs-step13/'+seqType+'/'
	boxplotDir = '/data/projects/bioxpress/v-2.1/generated/logs-step12/' + seqType + '/*'
	referenceFile = open('/data/projects/bioxpress/v-2.1/generated/reference/reference.txt')
	geneInfoFile = open('/data/projects/bioxpress/v-2.1/generated/logs-step9/' + seqType + '/' + seqType + '_transcript_information_final.txt')
	pattern = glob.glob(inputDir)
	patternBoxplot = glob.glob(boxplotDir)

	res1 = open(outputDir + 'BioXpress_feature.txt','w')
	res2 = open(outputDir + 'BioXpress_xref.txt','w')
	res3 = open(outputDir + 'BioXpress_level','w')
	res4 = open(outputDir + 'BioXpress_sample.txt','w')
	res5 = open(outputDir + 'BioXpress_doid.txt', 'w')

	xrefSrc = ['refseqNuc','refseqProtein','ensembleGeneId','ensembleRNAId','ensembleProteinId','geneName','uniprotKB']
	xrefDic = {}
	for row in geneInfoFile:
		if not row.startswith('miRNAID') and not row.startswith('GeneID'):
			row = row.strip().split('\t')
			transcriptName = row[6] if seqType == "RNAseq" else row[0]
			if seqType == "RNAseq":
				for i in range(1,8):
					if i != 6:
						xrefLine = '-\t' + transcriptName + '\t'+xrefSrc[i-1]+'\t' + row[i]
						xrefDic[xrefLine + '\n'] = 1
			else:
				if len(row) <= 7:
					row += ['-']
				xrefLine = '-\t' + transcriptName + '\tmiRBaseAc\t' + row[1]
				xrefDic[xrefLine + '\n'] = 1
				xrefLine = '-\t' + transcriptName + '\thgncSymbl\t' + row[6]
				xrefDic[xrefLine + '\n'] = 1
				xrefLine = '-\t' + transcriptName + '\tensemblID\t' + row[7]
				xrefDic[xrefLine + '\n'] = 1

		
	sampleDic = {}
	doidDic = {}
	featureDic = {}
	levelDic = {}

	for fileList in pattern:
		print fileList
	        with open(fileList, 'rb') as csvfile:
			csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
			for row in csvreader:
				if not row[0] == "GeneID" and not row[0] == "miRNAID":
					transcriptName = row[6] if seqType == "RNAseq" else row[0]
					typeSource = "mrna" if seqType == "RNAseq" else "mirna"
					res1New = '-\t' + transcriptName + '\t' + typeSource
					featureDic[res1New + '\n'] = 1

					tcgaCancer = row[10]
					doidCancer = row[-2].split(' & ')
					for oneCan in range(0, len(doidCancer)):
						doId = doidCancer[oneCan].split()[0].split(":")[-1].strip()
						if not doId.isdigit():
							doId = str(0)
							doTerm = ' '.join(doidCancer[oneCan].split())
						else:
							doTerm = ' '.join(doidCancer[oneCan].split()[2::])
						if oneCan == 0:
							cancerName = doidCancer[oneCan].split()
						else:
							cancerName = doidCancer[oneCan-1].split()
						parentDoid = cancerName[0].split(':')[-1].strip()
						doidDic[doId + '\t' + parentDoid + '\t' + doTerm+'\n'] = 1
					
					sampleDic['-\t' + tcgaCancer.strip() +'\t'+' '.join(row[-2].strip().split())+'\n'] = 1
					if row[11] == "Manual":
						sig = "Yes"
					elif row[-5] == "NA":
						sig = "No"
					else:
						sig = "Yes" if float(row[-5]) <= 0.05/float(row[-3]) else "No"

					newLine = '-\t' + transcriptName + '\t' + tcgaCancer + '\t' + ' '.join(row[-2].strip().split()) + '\t'
					newLine += '\t'.join(row[8::]) + '\t' + sig

					levelDic[newLine + '\n'] = 1

	referCancer = {}
	for row in referenceFile:
		row = row.strip().split('\t')
		referCancer[row[0]] = row[1]

	for fileList in patternBoxplot:
		print fileList
		with open(fileList, 'rb') as csvfile:
			csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
			for row in csvreader:
				if row[0] != "geneName" and row[0] != "miRNAName":
					cancerType = row[1]
					sampleDic['-\t' + cancerType +'\t'+referCancer[cancerType]+'\n'] = 1
					transcriptName = row[0]
					typeSource = "mrna" if seqType == "RNAseq" else "mirna"
					res1New = '-\t' + transcriptName + '\t' + typeSource
					featureDic[res1New + '\n'] = 1

	for key in featureDic:
		res1.write(key)
	for key in xrefDic:
		res2.write(key)
	for key in levelDic:
		res3.write(key)
	for key in sampleDic:
		res4.write(key)
	for key in doidDic:
		res5.write(key)

	referenceFile.close()
	geneInfoFile.close()
	res1.close()
	res2.close()
	res3.close()
	res4.close()
	res5.close()



if __name__ == '__main__':
	main()
