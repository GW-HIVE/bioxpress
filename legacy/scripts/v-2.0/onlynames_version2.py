for cancer in ('BLCA','BRCA','CESC','COAD','ESCA','HNSC','KICH','KIRC','KIRP','LIHC','LUAD','LUSC','PAAD','PRAD','READ','SARC','SKCM','THCA','STAD','UCEC'):
        name2=str(cancer)+'_type.txt'
        name1=str(cancer)+'_resultscreening.txt'
        name3=str(cancer)+'_orderednames.txt'
        name4=str(cancer)+'_condition.txt'
       
        rawdata=open(name1)
        screen1=list()
        screen3=list()
        screen2=list()
        condition2=list()
        
        for line in rawdata:
                a=line.split()
                for i in a:
                    b=i.split('-')
                    try:
                            serial=b[3:4]
                            serial=str(serial)
                            c=serial[2:4]
                            c=int(c)
                            if c==11:
                                    patient=b[0]+'-'+b[1]+'-'+b[2]
                                    screen1.append(str(patient))
                    except:
                            continue
                        
                break

        x=range(0,len(screen1),2)
        for i in x:
                screen3.append(screen1[int(i)])
        rawdata.close()
        
        rawdata=open(name1)
        conditions=open(name4,'w')
        type_s=open(name2,'w')
        condition=list()
        for line in rawdata:
                a=line.split()
                count3=0
                for j in screen3:
                        count3=count3+1
                        count4=-1
                        for i in a:
                                count4=count4+1
                                if i.startswith(j):
                                        b=i.split('-')
                                        serial=b[3:4]
                                        serial=str(serial)
                                        c=serial[2:4]
                                        c=int(c)
                                        if c==11:
                                                type_s.write(j+'-'+'normal'+'\t')
                                                conditions.write(j+'\n')
                                                condition.append(j+'\t')
                                                screen2.append(a[count4])
                                        else:
                                                type_s.write(j+'-'+'cancer'+'\t')
                                                screen2.append(a[count4])
                                                conditions.write(j+'\n')
                break
        type_s.close()
        
        ordered=open(name3,'w')
        for i in screen2:
                ordered.write(i+'       ')
        ordered.write('\n')

                
        ordered.close()
        rawdata.close()
        conditions.close()
