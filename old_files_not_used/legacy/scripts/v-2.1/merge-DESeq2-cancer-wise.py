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

	oriDir = '/data/projects/bioxpress/generated/logs-step1/' + seqType + '/*_resultscreening.txt'
	dataDir = '/data/projects/bioxpress/generated/logs-step3/' + seqType + '/*_DESeq_results_new.csv'
	outputDir = '/data/projects/bioxpress/generated/logs-step10/'+seqType+'/'
	geneInfoFile = '/data/projects/bioxpress/generated/logs-step9/'+seqType
	geneInfoFile +='/' + seqType + '_transcript_information_final.txt'

	pattern = glob.glob(dataDir)
	oriPattern = glob.glob(oriDir)

	FW = open(outputDir + 'cancer_wise_DESeq2.txt', 'w')
	heading1 = "GeneID,refseqNuc,refseqProtein,ensembleGeneId,ensembleRNAId,ensembleProteinId,uniprotKB,geneName,log2FC,expression,cancerType,platForm,pValue,adjPValue\n"
	heading2 = "miRNAID,miRBaseAc,chrom,start,end,strand,hgncSymbl,ensemblID,log2FC,expression,cancerType,platForm,pValue,adjPValue\n"

	heading = heading1 if seqType == "RNAseq" else heading2
	FW.write(heading)

	referDic = {}
	with open(geneInfoFile, 'rb') as tsvfile:
		tsvreader = csv.reader(tsvfile, delimiter = '\t', quotechar="|")
		for row in tsvreader:
			referDic[row[0]] = ','.join(row)

	for fileList in oriPattern:
		print fileList
		categories = fileList.split('/')[-1].split('_')
		cancerType = categories[0]
		platForm = categories[2]

		for cancerList in pattern:
			patCancerType = cancerList.split('/')[-1].split('_')[0]
			#patPlatForm = cancerList.split('/')[-1].split('_')[1] #only for miRNA
			if patCancerType == cancerType:#and platForm == patPlatForm: #the latter one only for miRNA
				with open(cancerList, 'rb') as csvfile:
					csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
					for row in csvreader:
						if row[0] != '"baseMean"':
							geneId = row[0].split('"')[1].split("|")[-1]
							logFc = row[2]
							expre = "Up" if float(logFc) >= 1 else 'Down' if float(logFc) <= -1 else "-"
							pValue = row[5]
							adjPValue = row[6]
							if geneId in referDic:
								newRow = '%s,%s,%s,%s,%s,%s,%s\n' % (referDic[geneId],logFc,expre,patCancerType,platForm,pValue,adjPValue)
								FW.write(newRow)
							else:
								print geneId
	FW.close()

if __name__ == '__main__':
        main()


				


