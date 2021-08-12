
ref=open('/data/projects/bioxpress/reference.txt')
dic={}
for line in ref:
    line=line.strip().split('\t')
    dic[line[0]]=line[1]
ref.close()


data=open('/data/projects/bioxpress/totally_Hiseq.txt')
total=open('/data/projects/bioxpress/totally_Hiseq_mapped_DOID_gene.txt','w')
for line in data:
    line1=line.strip().split('\t')
    if len(line1)>3:
        total.write(dic[line1[0]]+'\t'+'\t'.join(line1[0:2])+'\t'+'\t'.join(line1[3::])+'\n')
total.close()
data.close()


data=open('/data/projects/bioxpress/totally_GA.txt')
total=open('/data/projects/bioxpress/totally_GA_mapped_DOID_gene.txt','w')
for line in data:
    line1=line.strip().split('\t')
    if len(line1)>3:
        total.write(dic[line1[0]]+'\t'+'\t'.join(line1[0:2])+'\t'+'\t'.join(line1[3::])+'\n')
total.close()
data.close()

