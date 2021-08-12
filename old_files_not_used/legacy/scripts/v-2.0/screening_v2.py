import csv
for cancer in ('ACC','BLCA','BRCA','CESC','COAD','DLBC','GBM','ESCA','HNSC','KICH','KIRC','KIRP','LAML','OV','LGG','LIHC','LUAD','LUSC','PAAD','PRAD','READ','SARC','SKCM','THCA','STAD','UCEC','UCS'):
        name1=cancer+'__unc.edu__illuminahiseq_rnaseqv2__rsem.genes.results__Mar-25-2016.txt'
        name2=cancer+'_resultscreening.txt'
       
        rawdata=open(name1)
        result_data=open(name2,'w')

        for line in rawdata:
            name=[]
            line=line.split('\t')
            for i in line:
                if not i.startswith('Hybridization'):
                    a=i.split('-')
                    num=a[3][0:2]
                    num=int(num)
                    sr=a[0]+'-'+a[1]+'-'+a[2]
                    if num>10:
                        name.append(sr.strip())
            break
        refer=dict()
        for key in name:
            refer[key.strip()]=refer.get(key.strip(),0)+1
        lst=[]
        for key,val in refer.items():
            lst.append(key)
            
        rawdata.close()
        rawdata=open(name1)
        for line in rawdata:
            namev2=[]
            line=line.split('\t')
            for x in lst:
                indices = [a for a, y in enumerate(line) if y.find(x)>-1]
                c=0
                for e in indices:
                    each=line[e]
                    each=each.split('-')
                    num=each[3][0:2]
                    num=int(num)
                    if num<10:
                        c=1
                if c==1:
                    for final in indices:
                        namev2.append(final)
            break
        rawdata.close()
            
        rawdata=open(name1)
        rawdata=csv.reader(rawdata,delimiter='\t')
        for line in rawdata:
            result_data.write(line[0]+'\t')
            for x in namev2:
                result_data.write(line[x].strip()+'\t')
            result_data.write('\n')
        result_data.close()
