import os,sys
import string
import json
from optparse import OptionParser
import csv
import glob
import commands

__version__="1.0"
__status__ = "Dev"


###############################
def main():

        usage = "\n%prog  [options]"
        parser = OptionParser(usage,version="%prog " + __version__)
        parser.add_option("-i","--configfile",action="store",dest="configfile",help="Config file")
        parser.add_option("-c","--cancertype",action="store",dest="cancertype",help="Cancer type")

        (options,args) = parser.parse_args()
        for file in ([options.configfile, options.cancertype]):
                if not (file):
                        parser.print_help()
                        sys.exit(0)

        cancerType = options.cancertype
        configJson = json.loads(open(options.configfile, "r").read())

	csvFile= configJson["sampleqc"]["inputdir"] + "/tcga-" + cancerType + "-extract-all-even.csv"
	pngFile= configJson["sampleqc"]["outputdir"] + "/tcga-" + cancerType + "-pca-even.png"
	logFile= configJson["sampleqc"]["outputdir"] + "/tcga-" + cancerType + "-log.txt"

	cmd = configJson["rscriptpath"]+ " --vanilla " + "script.1.r " + csvFile
	cmd += " " + pngFile + " > " + logFile
	print cmd	
	x = commands.getoutput(cmd)
        print x

if __name__ == '__main__':
        main()

