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
def main():

	resTissueFile = open("/data/projects/bioxpress/Biox_tissue.txt", "w")
	resSampleFile = open("/data/projects/bioxpress/Biox_sample_addUberon.txt", "w")

	pathFile = "/data/projects/biomuta/uberon/*MappedUberon*"
	fileList = glob.glob(pathFile)
	
	dic = {}
	uberonList = set()
	for i in fileList:
		if i.find("BioMuta3_MappedUberon.csv") == -1:
			data = open(i, 'rb')
			for row in data:
				if not row.startswith("HGNC_symbol") and not row.startswith("UniProtKB_AC") and not row.startswith("Index"):
					row = row.strip().split(',')
					if i.find("miRNA_final_MappedUberon.csv") >= 0:
						tcga = row[11]
						doid = row[12]
					elif i.find("BioXpress_overall_MappedUberon.csv") >= 0:
						tcga = row[8]
						doid = row[9]
					elif i.find("miRNA_tumor_MappedUberon.csv") >= 0:
						tcga = "-"
						doid = row[5]
					elif i.find("BioXpress_tumor_MappedUberon.csv") >= 0:
						tcga = "-"
						doid = row[3]
					uberon = row[-1]

					dic[tcga + '\t' + doid] = uberon
					uberonList.add(uberon)
			data.close()

	data = open("/data/projects/bioxpress/BioXpress_sample.txt")
	dic2 = {}
	for line in data:
		line = line.strip().split('\t')
		dic2[line[1] + '\t' + line[2]] = '\t'.join(line)
	data.close()

	for i in dic2:
		if i in dic:
			newLine = dic2[i] + '\t' + dic[i]
		else:
			newLine = dic2[i] + '\t-'
		resSampleFile.write(newLine + '\n')

	for i in dic:
		if i not in dic2:
			newLine = '\t' + i + '\t' + dic[i]
			resSampleFile.write(newLine + '\n')

	for i in uberonList:
		resTissueFile.write('-\t' + i + '\n')

	resTissueFile.close()
	resSampleFile.close()		


if __name__ == '__main__':
	main()
