
for cancer in ('BLCA','BRCA','HNSC','KIRC','KIRP','LUAD','LUSC','STAD','UCEC','ACC','CESC','COAD','LAML','DLBC','ESCA','LGG','GBM','LIHC','KICH','READ','SARC','SKCM','OV','PAAD','PRAD','THCA','UCS'):
        name2='/data/projects/bioxpress/'+str(cancer)+'_unpaireddata_Hiseq.txt'
        result_data=open(name2,'w')
        name1='/data/external/TCGA/'+str(cancer)+'__unc.edu__illuminahiseq_rnaseqv2__rsem.genes.results__Mar-25-2016.txt'
        rawdata=open(name1)
        print name1
        column=[]

        for line in rawdata:
                count1=1
                a=line.strip().split('\t')
                result_data.write(a[0]+'\t'+a[1])
                for i in a[2::]:
                    count1=count1+1
                    j=i.split('-')[3]
                    if int(j[0:2])<10:
                        result_data.write('\t'+i)
                        column.append(count1)
                break
        result_data.write('\n')

        for line in rawdata:
                a1=line.strip().split('\t')
                result_data.write(a1[0]+'\t'+a1[1])
                count2=1
                for i1 in a1[2::]:
                        count2=count2+1
                        if count2 in column:
                                result_data.write('\t'+i1.strip())                                
                result_data.write('\n')

        rawdata.close()
        result_data.close()


for cancer in ('COAD','LAML','READ','UCEC'):
        name2='/data/projects/bioxpress/'+str(cancer)+'_unpaireddata_GA.txt'
        result_data=open(name2,'w')
        name1='/data/external/TCGA/'+str(cancer)+'__unc.edu__illuminaga_rnaseqv2__rsem.genes.results__Mar-25-2016.txt'
        rawdata=open(name1)
        print name1
        column=[]

        for line in rawdata:
                count1=1
                a=line.strip().split('\t')
                result_data.write(a[0]+'\t'+a[1])
                for i in a[2::]:
                    count1=count1+1
                    j=i.split('-')[3]
                    if int(j[0:2])<10:
                        result_data.write('\t'+i)
                        column.append(count1)
                break
        result_data.write('\n')

        for line in rawdata:
                a1=line.strip().split('\t')
                result_data.write(a1[0]+'\t'+a1[1])
                count2=1
                for i1 in a1[2::]:
                        count2=count2+1
                        if count2 in column:
                                result_data.write('\t'+i1.strip())
                result_data.write('\n')

        rawdata.close()
        result_data.close()

