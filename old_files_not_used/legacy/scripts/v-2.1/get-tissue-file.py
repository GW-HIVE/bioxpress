import csv
import glob
import os
import string
from optparse import OptionParser
import sys
import decimal as Decimal


__version__="1.0"
__status__ = "Dev"


###############################
def main():

	resTissueFile = open("/data/projects/bioxpress/v-2.1/generated/logs-step14/BioXpress_tissue.txt", "w")
	resCancerFile = open("/data/projects/bioxpress/v-2.1/generated/logs-step14/BioXpress_cancer_addUberon.txt", "w")

	pathFile = open("/data/projects/bioxpress/v-2.1/generated/logs-step14/mappingTable-uberon-doid.csv", 'rb')
	
	uberonDic = {}
	uberonList = {}
	data = csv.reader(pathFile, delimiter=',')
	for row in data:
		uberonDic[row[0].replace('_', ':')] = row[3].replace('_', ':')
			uberonList.add(row[3].replace('_', ':'))

	data = open("/data/projects/bioxpress/v-2.1/generated/logs-step13/RNAseq/BioXpress_cancer_final.txt")
	dic2 = {}
	for line in data:
		line = line.strip().split('\t')
		doid = line[2]
		if line[1] != '-':
			doid = ''
		dic2[line[1] + '\t' + doid] = '\t'.join(line)
	data.close()

	for i in dic2:
		if i.split('\t')[1] in uberonDic:
			newLine = dic2[i] + '\t' + uberonDic[i]
		else:	
			newLine = dic2[i] + '\t-'
		resCancerFile.write(newLine + '\n')

	for i in uberonList:
		resTissueFile.write('-\t' + i + '\n')

	resTissueFile.close()
	resCancerFile.close()		


if __name__ == '__main__':
	main()
