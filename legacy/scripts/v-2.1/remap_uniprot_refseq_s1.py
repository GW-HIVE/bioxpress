refer=open('/data/projects/bioxpress/HUMAN_9606_idmapping_selected.tab')

dic={}

for line in refer:
	line=line.strip().split('\t')
	#a = line[3].split(' ')
	#b = ''.join(a[0::])
	dic[line[1].upper().split('_')[0]]=line[0]+'\t'+line[3]

refer.close()

refer2=open('/mnt/data/knowledgebases/bioxpress/BioXpress_differential_expression.tsv')

for line in refer2:
        line=line.strip().split('\t')
        if dic.has_key(line[2].upper()):
                continue
        else:
                dic[line[2].upper()]=line[0]+'\t'+line[1]
refer2.close()


#data=open('/data/knowledgebases/bioxpress/BioXpress_interface_perpatient_v2.0.txt')
data=open('/data/projects/bioxpress/gene_Hiseq_UniprotRefseq.txt')
#data=open('/mnt/data/knowledgebases/bioxpress/BioXpress_interface_overall_v2.0.txt')
res=open('/mnt/data/projects/bioxpress/BioXpress_v2_remap_s1.txt','w')

for line in data:
	if not line.startswith('UniProtKB_AC'):
		line1=line.strip().split('\t')
		if dic.has_key(line1[2].upper()):
			if len(dic[line1[2].upper()])>1:
				res.write(dic[line1[2].upper()]+'\t'+'\t'.join(line1[2::])+'\n')
			else:
				print line.strip()
		else:
			print line.strip()

data.close()

res.close()
			
