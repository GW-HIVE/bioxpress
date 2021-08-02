import os,sys
import string
from optparse import OptionParser
from Bio import SeqIO

__version__="1.0"
__status__ = "Dev"



###############################
def main():

        genomeSeqFile = "/data/projects/biomuta/downloads/ucsc/genome/human-genome-hg19.fa"

	genomeSeq = {}
	for record in SeqIO.parse(genomeSeqFile, "fasta"):
		if record.id == "chr14":
			chrId = record.id.replace("chr", "")
			genomeSeq[chrId] = record.seq.upper()

	chrom = "14"	
	pos = "63174960" 

	i = int(pos) - 1
	if chrom in genomeSeq:
		ref2 = genomeSeq[chrom][i]	
		print chrom,pos,ref2

if __name__ == '__main__':
        main()








