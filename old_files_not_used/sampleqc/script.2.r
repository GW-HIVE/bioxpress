cnt <- 0
for (cancerType in c('PAAD', 'CHOL', 'SARC', 'SKCM', 'THYM', 'UCEC', 'READ', 'CESC', 'PCPG')){
	cnt <- cnt+1
	cmd <- paste("Rscript --vanilla script.3.r ../conf/config-2.1.json tcga ",cancerType,sep="")
	try(system(cmd))
	print(cmd)
}
print(cnt)
#cmd <- paste("Rscript --vanilla script.3.r ../conf/config-2.1.json tcga ","BRCA",sep="")
#try(system(cmd))
