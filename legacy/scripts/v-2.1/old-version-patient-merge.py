
data = open('/data/projects/bioxpress/BioXpress_interface_perpatient_final_v2.0.txt')
res = open('/data/projects/bioxpress/BioXpress_interface_perpatient_final_v2.0_old_version.txt', 'w')

heading = 'geneName,log2FC,expression,cancerType,patientId,platForm,pValue,adjPValue'
res.write(heading + '\n')

for line in data:
	line = line.strip().split('\t')
	newLine = line[2] + ',' + line[3] + ',' + line[]
