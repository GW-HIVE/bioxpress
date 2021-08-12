import sys

data=open(sys.argv[1])
for line1 in data:
    line=line1.strip().split('\t')
    if not line[1].find('UniProt')>=0:
        patie1=line[2].split('/')
	allpa=patie1[1].split('(')[0]
        patie2=line[3]
	patie3=line[4]
        if float(patie2)>float(patie1[0]) or float(allpa)<(float(patie3)+float(patie1[0])):
            print line1.strip()
        
data.close()
