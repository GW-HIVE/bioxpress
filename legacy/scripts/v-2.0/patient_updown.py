import sys
refer=open('patient_count.txt')
dic={}
for line in refer:
    line=line.split('\t')
    dic[line[0]]=line[1].strip()

dic_up={}
dic_down={}
data=open(sys.argv[1])
for line in data:
    line=line.split('\t')
    try:
        if float(line[1])>0:
            dic_up[line[0]+'\t'+line[6]]=dic_up.get(line[0]+'\t'+line[6],0)+1
        elif float(line[1])<0:
            dic_down[line[0]+'\t'+line[6]]=dic_down.get(line[0]+'\t'+line[6],0)+1
    except:
        continue
data.close()

print "gene\tcancer_type\tup\tdown\ttotal\n"

for key,val in dic_up.items():
    ai=key.split('\t')[1]
    if dic_down.has_key(key):
        print key+'\t'+str(val)+'\t'+str(dic_down[key])+'\t'+str(dic[ai])
    else:
       print key+'\t'+str(val)+'\t0\t'+str(dic[ai])

for key,val in dic_down.items():
    ai=key.split('\t')[1]
    if not dic_up.has_key(key): 
        print  key+'\t0\t'+str(dic_down[key])+'\t'+str(dic[ai])
