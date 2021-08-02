import commands

cancerType = ['ESCA','LUAD','PAAD','LIHC','STAD', 'CHOL', 'COAD', 'THCA', 'KICH', 'KIRP', 'KIRC', 'PRAD', 'PCPG', 'HNSC', 'SARC', 'LUSC',
'SKCM', 'THYM', 'BLCA', 'BRCA', 'UCEC', 'READ', 'CESC']

for cancer in cancerType:
	cmd = "python biox-extractor-allsubjects.py -i ../conf/config-2.1.json -r tcga -c " + cancer
	x = commands.getoutput(cmd)
	print x	

