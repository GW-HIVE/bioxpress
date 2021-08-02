res=open('/data/knowledgebases/bioxpress/BioXpress_interface_tumor_Hiseq_final.txt','w')
#res=open('/data/knowledgebases/bioxpress/BioXpress_interface_overall_final.txt','w')



#data1=open('/data/knowledgebases/bioxpress/BioXpress_interface_overall_v2.0.txt')
#data1=open('/data/knowledgebases/bioxpress/BioXpress_interface_perpatient_v2.0.txt')
#for line in data1:
#	res.write(line.strip()+'\tCount\n')
#	break

#data1.close()

data2=open('/data/projects/bioxpress/BioXpress_v2_remap_s1.txt')
for line in data2:
	res.write(line)
data2.close()

data3=open('/data/projects/bioxpress/BioXpress_v2_remap_s4.txt')

for line in data3:
	res.write(line)
data3.close()

res.close()
