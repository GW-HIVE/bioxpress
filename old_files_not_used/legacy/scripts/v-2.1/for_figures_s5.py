import sys

overall=open(sys.argv[1])
perpatient=open(sys.argv[2])
dic={}

for line in overall:
    line=line.strip().split('\t')
    used=line[2]+'\t'+line[8]
    if line[3].find('NA')==-1:
        dic[used]=line[10]+'\t'+line[3]

overall.close()

dic2={}
for line1 in perpatient:
    line=line1.strip().split('\t')
    used=line[2]+'\t'+line[8]
    if line[0].find('UniProt')==-1:
        if dic.has_key(used):
            dic2[used+'+'+line[11]]=dic[used]+'\t'+line[3]
perpatient.close()

dic3={}
dic4={}
for key,val in dic2.items():
    key1=key.split('+')[0]
    val1=val.split('\t')
    if val1[2].find('NA')==-1 and float(val1[1])>0:
        if float(val1[2])>float(val1[1]):
            dic3[key1+'\t'+val1[0]]=dic3.get(key1+'\t'+val1[0],0)+1
    elif val1[2].find('NA')==-1 and float(val1[1])<0:
        if float(val1[2])<float(val1[1]):
            dic3[key1+'\t'+val1[0]]=dic3.get(key1+'\t'+val1[0],0)+1
    elif val1[2].find('NA') >=0:
	dic4[key1+'\t'+val1[0]]=dic4.get(key1+'\t'+val1[0],0)+1

for key,val in dic3.items():
    if dic4.has_key(key):
  	  print key+'\t'+str(val)+'\t'+str(dic4[key])
    else:
	  print key+'\t'+str(val)+'\t0'

