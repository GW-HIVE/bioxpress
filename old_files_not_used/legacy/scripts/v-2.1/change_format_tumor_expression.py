import sys

refer=open('/data/projects/bioxpress/reference.txt')
dic={}
for line in refer:
	line=line.strip().split('\t')
	dic[line[1]]=line[0]
refer.close()


res1=open('/data/knowledgebases/bioxpress/BioXpress_feature.txt','w')
res2=open('/data/knowledgebases/bioxpress/BioXpress_xref.txt','w')
res3=open('/data/knowledgebases/bioxpress/BioXpress_level','w')
res4=open('/data/knowledgebases/bioxpress/BioXpress_sample.txt','w')
res5=open('/data/knowledgebases/bioxpress/BioXpress_boxplot','w')

st=set()
st2=set()

data=open('/data/knowledgebases/bioxpress/BioXpress_interface_tumor_Hiseq_final.txt')
for line in data:
	line=line.strip().split('\t')
	st.add(line[2]+'\tmrna\n')
	st2.add(dic[line[3]]+'\t'+line[3]+'\n')
data.close()


data=open('/data/knowledgebases/bioxpress/BioXpress_interface_tumor_GA_final.txt')
for line in data:
        line=line.strip().split('\t')
        st.add(line[2]+'\tmrna\n')
        st2.add(dic[line[3]]+'\t'+line[3]+'\n')
data.close()

data=open('/data/knowledgebases/bioxpress/BioXpress_interface_overall_forsql.txt')
for line in data:
        line=line.strip().split('\t')
        st.add(line[3]+'\tmrna\n')
        st2.add(line[9]+'\t'+line[10]+'\n')
data.close()

for i in st:
	res1.write('-\t'+i)
for i in st2:
	res4.write('-\t'+i)

st3=set()
st4=set()
st5=set()

data=open('/data/knowledgebases/bioxpress/BioXpress_interface_tumor_GA_final.txt')
for line in data:
	line=line.strip().split('\t')
	st3.add('-\t'+line[2]+'\tuniProtAc\t'+line[0]+'\n')
	if len(line[1])<1:
		st3.add('-\t'+line[2]+'\trefSeqId\t-\n')
	else:
		st3.add('-\t'+line[2]+'\trefSeqId\t'+line[1]+'\n')
	st5.add('-\t'+line[2]+'\t'+dic[line[3]]+'\t'+line[3]+'\tGA\t'+'\t'.join(line[4::])+'\n')

data.close()

data=open('/data/knowledgebases/bioxpress/BioXpress_interface_tumor_Hiseq_final.txt')
for line in data:
        line=line.strip().split('\t')
        st3.add('-\t'+line[2]+'\tuniProtAc\t'+line[0]+'\n')
        if len(line[1])<1:
                st3.add('-\t'+line[2]+'\trefSeqId\t-\n')
        else:
                st3.add('-\t'+line[2]+'\trefSeqId\t'+line[1]+'\n')
        st5.add('-\t'+line[2]+'\t'+dic[line[3]]+'\t'+line[3]+'\tHISEQ\t'+'\t'.join(line[4::])+'\n')

data.close()


data=open('/data/knowledgebases/bioxpress/BioXpress_interface_overall_forsql.txt')
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
for i in st5:
	res5.write(i)

res1.close()
res2.close()
res3.close()
res4.close()
res5.close()
