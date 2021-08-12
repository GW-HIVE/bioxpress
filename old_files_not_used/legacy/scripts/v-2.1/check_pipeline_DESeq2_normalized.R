

for (cancerType in c('ACC','DLBC','GBM','LGG','MESO','OV','TGCT','UCS','LAML','UVM','ESCA','LUAD','PAAD','LIHC','STAD', 'CHOL', 'COAD', 'THCA', 'KICH', 'KIRP', 'KIRC', 'PRAD', 'PCPG', 'HNSC', 'SARC', 'LUSC', 'SKCM', 'THYM', 'BLCA', 'BRCA', 'UCEC', 'READ', 'CESC')){
	type = "RNAseq"
	setwd(paste("/data/projects/bioxpress/v-2.1/generated/logs-step1/",type,sep=""))
	fileName = paste(cancerType,"gene", type, "resultscreening.txt",sep="_")
	data = read.table(fileName,sep='\t', header=TRUE)
	rownames(data) = data[,1]
	data = data[,-1]

	data.pca <- prcomp(as.matrix(data), center = TRUE, scale. = TRUE)
}


