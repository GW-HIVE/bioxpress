import os
refer=open('patient_count.txt')
dic={}
for line in refer:
    line=line.split('\t')
    dic[line[0]]=line[1].strip()
    
for i in dic.keys():
    a=i
    try:
        os.chdir('../'+a)
    except:
        os.chdir(a)
    cancer=i
    patients=dic[i]

    print "Gene\tlog2FoldChange\tp_value\tadjusted p_value\tSignificant\tExpression\tCancer Type\t#Patients\tSample ID\tData Source\tPMID"

    for f in os.listdir('../'+a):
        if f.startswith('TCGA.'):
            handle = open(f)
            f=f.split('.')
            f="-".join(f[0::])
            for line in handle:
                ls = line.split(',')
                if ls[0] != '""':
                    if (ls[-1].strip()!='NA' and float(ls[-1].strip())<0.05):
                        if (ls[2]!='NA' and float(ls[2])>0):
                            print ls[0]+'\t'+ls[2]+'\t'+ls[-2]+'\t'+ls[-1].strip()+"\tYes\tUp\t"+cancer+"\t"+patients+"\t"+f+'\tRNASeqV2\t-'
                        elif (ls[2]!='NA' and float(ls[2])<=0):
                            print ls[0]+'\t'+ls[2]+'\t'+ls[-2]+'\t'+ls[-1].strip()+"\tYes\tDown\t"+cancer+"\t"+patients+"\t"+f+'\tRNASeqV2\t-'
                    elif (ls[-1].strip()!='NA' and float(ls[-1].strip())>=0.05):
                        if (ls[2]!='NA' and float(ls[2])>0):
                            print ls[0]+'\t'+ls[2]+'\t'+ls[-2]+'\t'+ls[-1].strip()+"\tNo\tUp\t"+cancer+"\t"+patients+"\t"+f+'\tRNASeqV2\t-'
                        elif (ls[2].strip()!='NA' and float(ls[2])<=0):
                            print ls[0]+'\t'+ls[2]+'\t'+ls[-2]+'\t'+ls[-1].strip()+"\tNo\tDown\t"+cancer+"\t"+patients+"\t"+f+'\tRNASeqV2\t-'
                        else:
                            print ls[0]+'\t'+ls[2]+'\t'+ls[-2]+'\t'+ls[-1].strip()+"\tNo\t-\t"+cancer+"\t"+patients+"\t"+f+'\tRNASeqV2\t-'
                    else:
                        if (ls[2]!='NA' and float(ls[2])>0):
                            print ls[0]+'\t'+ls[2]+'\t'+ls[-2]+'\t'+ls[-1].strip()+"\tNo\tUp\t"+cancer+"\t"+patients+"\t"+f+'\tRNASeqV2\t-'
                        elif (ls[2]!='NA' and float(ls[2])<=0):
                            print ls[0]+'\t'+ls[2]+'\t'+ls[-2]+'\t'+ls[-1].strip()+"\tNo\tDown\t"+cancer+"\t"+patients+"\t"+f+'\tRNASeqV2\t-'
                        else:
                            print ls[0]+'\t'+ls[2]+'\t'+ls[-2]+'\t'+ls[-1].strip()+"\tNo\t-\t"+cancer+"\t"+patients+"\t"+f+'\tRNASeqV2\t-'

                        
            handle.close()

    

