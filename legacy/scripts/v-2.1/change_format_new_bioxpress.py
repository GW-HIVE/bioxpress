import sys

data=open('/data/knowledgebases/bioxpress/BioXpress_interface_overall_forsql.txt')
res1=open('/data/knowledgebases/bioxpress/BioXpress_feature.txt','w')
res2=open('/data/knowledgebases/bioxpress/BioXpress_xref.txt','w')
res3=open('/data/knowledgebases/bioxpress/BioXpress_level','w')
res4=open('/data/knowledgebases/bioxpress/BioXpress_sample.txt','w')

st=set()
st2=set()

for line in data:
	line=line.strip().split('\t')
	st.add(line[3]+'\tprotein\n')
	st2.add(line[9]+'\t'+line[10]+'\n')
data.close()

data=open('/data/knowledgebases/bioxpress/BioXpress_interface_overall_forsql.txt')
for i in st:
	res1.write('-\t'+i)
for i in st2:
	res4.write('-\t'+i)

st3=set()
st4=set()
for line in data:
	line=line.strip().split('\t')
	st3.add('-\t'+line[3]+'\tuniProtAc\t'+line[1]+'\n')
	if len(line[2])<1:
		st3.add('-\t'+line[3]+'\trefSeqId\t-\n')
	else:
		st3.add('-\t'+line[3]+'\trefSeqId\t'+line[2]+'\n')
	st4.add('-\t'+line[3]+'\t'+line[9]+'\t'+line[10]+'\t'+'\t'.join(line[4:9])+'\t'+'\t'.join(line[11::])+'\n')

data.close()

for i in st3:
	res2.write(i)
for i in st4:
	res3.write(i)

res1.close()
res2.close()
res3.close()
