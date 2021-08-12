data=open('/data/knowledgebases/bioxpress/BioXpress_interface_overall_forsql.txt')
st=set()
st2=set()

for line in data:
	line=line.strip().split('\t')
	st2.add(line[10])
	a=line[10].split(' & ')
	for i in a:
		st.add(i)
data.close()
print len(st)
print len(st2)
