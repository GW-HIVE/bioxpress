import csv
import glob
import os
import string
import sys

__version__="1.0"
__status__ = "Dev"


###############################
def main():

	owlFile = open("/data/projects/bioxpress/v-2.1/downloads/do/ext.owl", 'rb')
	outputFile = open("/data/projects/bioxpress/v-2.1/generated/logs-step14/mappingTable-uberon-doid.csv", 'w')
	manualFile = open("/data/projects/bioxpress/v-2.1/downloads/do/manualAddedUberonId.csv", 'rb')

	for row in owlFile:
		row = row.strip().split('\n')
		if "Equivalent" in row[0]:
			splitRow = row[0].split('/')
			doidHighLevel = splitRow[4].split('>')[0]
			doidLowLevel = splitRow[8].split('>')[0]
			obo = splitRow[-5].split('>')[0]
			uberonId = splitRow[-1].split('>')[0]
			if "CL" not in uberonId and "HP" not in uberonId and "NCBIT" not in uberonId:
				newLine = "%s,%s,%s,%s\n" % (doidHighLevel, doidLowLevel, obo, uberonId)
				outputFile.write(newLine)
	owlFile.close()

	for row in manualFile:
		outputFile.write(row)
	outputFile.close()



if __name__ == '__main__':
	main()
