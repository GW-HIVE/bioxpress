data=open('DESeq_perpatient_merged.txt')

for line in data:
    if not line.startswith("Gene"):
        line=line.strip().split('\t')
        if line[1]!="NA":
            line[1]=str(float(line[1])*(-1.0))
        line1="\t".join(line[0::])
        print line1
    else:
        print line.strip()

data.close()
