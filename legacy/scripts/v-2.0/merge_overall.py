import os
refer=open('patientcount_percancer.txt')
dic={}
for line in refer:
    if not line.startswith('gene') and not line.startswith('\n'):
        line=line.split('\t')
        dic[line[0]+'\t'+line[1]]=line[2]+'\t'+line[3]+'\t'+line[4].strip()

print "Gene\tlog2FoldChange\tp_value\tadjusted p_value\tSignificant\tExpression\tCancer Type\t#Patients\tTotal\tData Source\tPMID"

for f in os.listdir('../RNASeqV2'):
    if f.find('_DESeq_results.csv')>=0:
         handle = open(f)
         cancer1=f.split('_')[0]
         for line in handle:
             ls=line.split(',')
             for i in dic.keys():
                 gene=i.split('\t')[0].strip()
                 cancer=i.split('\t')[1].strip()
                 patients=dic[i]
                 if (cancer==cancer1 and gene==ls[0]):
                     if (ls[-1].strip()!='NA' and float(ls[-1].strip())<0.05):
                         if (ls[2]!='NA' and float(ls[2])>0):
                             print ls[0]+'\t'+ls[2]+'\t'+ls[-2]+'\t'+ls[-1].strip()+"\tYes\tUp\t"+cancer+"\t"+patients.split('\t')[0]+'/'+patients.split('\t')[2]+'('+str(round(float(patients.split('\t')[0])*100/float(patients.split('\t')[2]),2))+")\t"+f+'\tRNASeqV2\t-'
                         elif (ls[2]!='NA' and float(ls[2])<=0):
                             print ls[0]+'\t'+ls[2]+'\t'+ls[-2]+'\t'+ls[-1].strip()+"\tYes\tDown\t"+cancer+"\t"+patients.split('\t')[1]+'/'+patients.split('\t')[2]+'('+str(round(float(patients.split('\t')[1])*100/float(patients.split('\t')[2]),2))+")\t"+f+'\tRNASeqV2\t-'
                     else:
                         if (ls[2]!='NA' and float(ls[2])>0):
                             print ls[0]+'\t'+ls[2]+'\t'+ls[-2]+'\t'+ls[-1].strip()+"\tNo\tUp\t"+cancer+"\t"+patients.split('\t')[0]+'/'+patients.split('\t')[2]+'('+str(round(float(patients.split('\t')[0])*100/float(patients.split('\t')[2]),2))+")\t"+f+'\tRNASeqV2\t-'
                         elif (ls[2]!='NA' and float(ls[2])<=0):
                             print ls[0]+'\t'+ls[2]+'\t'+ls[-2]+'\t'+ls[-1].strip()+"\tNo\tDown\t"+cancer+"\t"+patients.split('\t')[1]+'/'+patients.split('\t')[2]+'('+str(round(float(patients.split('\t')[1])*100/float(patients.split('\t')[2]),2))+")\t"+f+'\tRNASeqV2\t-'
                         else:
                             print ls[0]+'\t'+ls[2]+'\t'+ls[-2]+'\t'+ls[-1].strip()+"\tNo\t-\t"+cancer+"\t-\t"+f+'\tRNASeqV2\t-'
         handle.close()

    
