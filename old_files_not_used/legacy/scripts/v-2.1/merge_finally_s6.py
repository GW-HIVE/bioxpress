res=open('/data/knowledgebases/bioxpress/BioXpress_interface_overall_forsql.txt','w')

dic={}
refer=open('/data/knowledgebases/bioxpress/for_figures_count.txt')
for line in refer:
	line=line.strip().split('\t')
	dic[line[0]+'\t'+line[1]+'\t'+line[2]]=line[3]+'\t'+line[4].strip()
refer.close()

data1=open('/data/knowledgebases/bioxpress/BioXpress_interface_overall_final.txt')
count=10000
for line1 in data1:
	count+=1
	line=line1.strip().split('\t')
	used = line[2]+'\t'+line[8]+'\t'+line[10]
	if not line1.startswith('UniProtKB_AC'):
		if dic.has_key(used):
			res.write(str(count)+'\t'+line1.strip()+'\t'+dic[used]+'\n')
		else:
			res.write(str(count)+'\t'+line1.strip()+'\t0\t0\n')

data1.close()

res.close()
