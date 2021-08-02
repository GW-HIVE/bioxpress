import csv
refer = open('/data/projects/bioxpress/uniprot_bioxpress_reviewed.txt')
dic1={}
for line in refer:
	if not line.startswith('Entry'):
		line=line.strip().split('\t')
		try:
			geneName = line[2].upper().split(' ')
			dic1[line[0].upper()]=';'.join(geneName)
		except:
			dic1[line[0].upper()]=line[1].upper().split('_')[0]

refer.close()


data = open('/data/projects/bioxpress/gene_with_protein_product.txt')
data = csv.reader(data,delimiter = '\t')
dic = {}
for line in data:
	alias = line[8].upper()
	alias_pre = line[10].upper()
	if alias.startswith('"'):
		alias = alias.split('"')[1]

        if alias_pre.startswith('"'):
                alias_pre = alias_pre.split('"')[1]

	if len(line[25])>1 and len(line[1])>1 and dic1.has_key(line[25].upper()):
		dic[line[25].upper()+'\t'+line[1].upper()] = alias+'|'+alias_pre
	elif len(line[25])<1 and len(line[1])>1 and dic1.has_key(line[25].upper()):
		dic['-\t'+line[1].upper()] = alias+'|'+alias_pre
	elif len(line[25])>1 and len(line[1])<1 and dic1.has_key(line[25].upper()):
		dic[line[25].upper()+'\t-'] = alias+'|'+alias_pre
	else:
		dic['-\t-'] = alias+'|'+alias_pre


data = open('/data/projects/bioxpress/BioXpress_v2_remap_s2.txt')
res = open('/data/projects/bioxpress/BioXpress_v2_remap_s3.txt','w')

for line1 in data:
	line=line1.strip().split('\t')
	ids=''
	for a,b in dic.items():
		i = a.split('\t')
		if line[2].upper() == i[1] or line[2].upper() == b.upper() or b.find(line[2].upper()+'|')>=0 or b.find('|'+line[2].upper())>=0:
			ids = i[0] +'\t'+line[1] +'\t'+line[2]
#			break
				
	if ids != '':
		res.write(ids+'\t'+'\t'.join(line[3::])+'\n')
	else:

		ids2=''
		for key,val in dic1.items():
			val1=val.split(';')
			for i in val1:
				if i == line[2].upper():
					ids2 = key + '\t'+line[1]+'\t'+line[2]
		if ids2 != '':
			res.write(ids2+'\t'+'\t'.join(line[3::])+'\n')
		else:
			res.write(line1)
				
data.close()
res.close() 
	
