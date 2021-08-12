refer=open('/data/projects/bioxpress/gene_refseq_uniprotkb_collab')

dic={}

for line in refer:
	line=line.strip().split('\t')
	if line[0].startswith('NP_'):
		if dic.has_key(line[1].upper()):
			dic[line[1].upper()]=dic[line[1].upper()]+'; '+line[0]
		else:
			dic[line[1].upper()]=line[0]
refer.close()

data=open('/data/projects/bioxpress/BioXpress_v2_remap_s3.txt')
ano_refer=open('/mnt/data/projects/bioxpress/LRG_RefSeqGene')
dic2={}
for line in ano_refer:
	line=line.strip().split('\t')
	if dic2.has_key(line[2].upper()):
		dic2[line[2].upper()]=dic2[line[2].upper()]+'; '+line[5]
	else:
		dic2[line[2].upper()]=line[5]
ano_refer.close()


res=open('/data/projects/bioxpress/BioXpress_v2_remap_s4.txt','w')
for line in data:
	line1=line.strip().split('\t')
	last=line1[1].split(';')
	if dic.has_key(line1[0].upper()):
		res.write(line1[0]+'\t'+dic[line1[0].upper()]+'\t'+'\t'.join(line1[2::])+'\n')
	else:
		if dic2.has_key(line1[2].upper()):
			res.write(line1[0]+'\t'+dic2[line1[2].upper()]+'\t'+'\t'.join(line1[2::])+'\n')
		else:
			res.write(line1[0]+'\t-\t'+'\t'.join(line1[2::])+'\n')


data.close()
res.close()
			
