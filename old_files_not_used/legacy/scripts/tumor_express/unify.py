result=open('/data/projects/bioxpress/totally_Hiseq.txt','w')
reference=open('/data/projects/bioxpress/reference_Hiseq.txt','w')
st=set()
for name1 in ('BLCA','BRCA','HNSC','KIRC','KIRP','LUAD','LUSC','STAD','UCEC','ACC','CESC','COAD','LAML','DLBC','ESCA','LGG','GBM','LIHC','KICH','READ','SARC','SKCM','OV','PAAD','PRAD','THCA','UCS'):
    data=open('/data/projects/bioxpress/'+name1+'_unpaireddata_Hiseq.txt','r')

    for line in data:
        line=line.strip().split('\t')
        reference.write(name1+'\t'+str(len(set(line))-1)+'\n')
        break

    for line in data:
        line=line.strip().split('\t')
        pos= [a for a, x in enumerate(line) if x.find('raw_count')>=0]
        break

    for line in data:
        count=-1
        line=line.strip().split('\t')
        result.write(name1+'\t'+line[0]+'\t'+line[1])
        for i in line:
            count+=1
            if count in pos:
                result.write('\t'+line[count].strip())
        result.write('\n')
    data.close()
  
result.close()
reference.close()



result=open('/data/projects/bioxpress/totally_GA.txt','w')
reference=open('/data/projects/bioxpress/reference_GA.txt','w')
st=set()
for name1 in ('COAD','LAML','READ','UCEC'):
    data=open('/data/projects/bioxpress/'+name1+'_unpaireddata_GA.txt','r')

    for line in data:
        line=line.strip().split('\t')
        reference.write(name1+'\t'+str(len(set(line))-1)+'\n')
        break

    for line in data:
        line=line.strip().split('\t')
        pos= [a for a, x in enumerate(line) if x.find('raw_count')>=0]
        break

    for line in data:
        count=-1
        line=line.strip().split('\t')
        result.write(name1+'\t'+line[0]+'\t'+line[1])
        for i in line:
            count+=1
            if count in pos:
                result.write('\t'+line[count].strip())
        result.write('\n')
    data.close()

result.close()
reference.close()

