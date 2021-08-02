import numpy as np
data=open('/data/projects/bioxpress/totally_Hiseq_mapped_DOID_gene.txt')
result=open('/data/projects/bioxpress/gene_Hiseq_for_heatmap.txt','w')
for line in data:
    line1=line.split('\t')
    gene=line1[2]+'\t'+line1[0]+'\t'
    total=len(line1[3::])
    lst=[]
    lst3=[]
    for i in line1[3::]:
        if i != '0.00':
            lst.append(i)
        lst3.append(float(i.strip()))
    expre=len(lst)
    if sum(lst3)==0:
        lower='NA'
        mid="NA"
        higher='NA'
        maxi='NA'
        mini='NA'
    else:
        a=np.array(lst3)
        lower=np.percentile(a,25)
        mid=np.percentile(a,50)
        higher=np.percentile(a,75)
        maxi=max(lst3)
        mini=min(lst3)
    try:
        percent=float(expre)*100/float(total)
    except:
        percent=0.00
	print gene
    percent=round(percent,2)
    result.write(gene+str(expre)+'/'+str(total)+'('+str(percent)+'%)'+'\t'+str(mini)+'\t'+str(lower)+'\t'+str(mid)+'\t'+str(higher)+'\t'+str(maxi)+'\n')

result.close()
data.close()


data=open('/data/projects/bioxpress/totally_GA_mapped_DOID_gene.txt')
result=open('/data/projects/bioxpress/gene_GA_for_heatmap.txt','w')
for line in data:
    line1=line.split('\t')
    gene=line1[2]+'\t'+line1[0]+'\t'
    total=len(line1[3::])
    lst=[]
    lst3=[]
    for i in line1[3::]:
        if i.find('.')>-1:
            lst.append(i)
        lst3.append(float(i.strip()))
    expre=len(lst)
    if sum(lst3)==0:
        lower='NA'
        mid="NA"
        higher='NA'
        maxi='NA'
        mini='NA'
    else:
        a=np.array(lst3)
        lower=np.percentile(a,25)
        mid=np.percentile(a,50)
        higher=np.percentile(a,75)
        maxi=max(lst3)
        mini=min(lst3)
    try:
        percent=float(expre)*100/float(total)
    except:
        percent=0.00
        print gene
    percent=round(percent,2)
    result.write(gene+str(expre)+'/'+str(total)+'('+str(percent)+'%)'+'\t'+str(mini)+'\t'+str(lower)+'\t'+str(mid)+'\t'+str(higher)+'\t'+str(maxi)+'\n')

result.close()
data.close()

