#source("https://bioconductor.org/biocLite.R")
#biocLite("DESeq2")

library(DESeq2)
for (cancerType in c('ACC','DLBC','GBM','LGG','MESO','OV','TGCT','UCS','LAML','UVM','ESCA','LUAD','PAAD','LIHC','STAD', 'CHOL', 'COAD', 'THCA', 'KICH', 'KIRP', 'KIRC', 'PRAD', 'PCPG', 'HNSC', 'SARC', 'LUSC', 'SKCM', 'THYM', 'BLCA', 'BRCA', 'UCEC', 'READ', 'CESC')){

	for (type in c('miRNAseq', 'RNAseq')){
		setwd(paste("/data/projects/bioxpress/generated/logs-step7/",type,sep=""))

		if (type == "RNAseq"){
			fileName = paste(cancerType,'gene',type,"tumor_expression.txt",sep="_")
			cate = "RNAseq"

		} else {
			fileName = paste(cancerType,"mir_HiSeq.hg19.mirbase20_tumor_expression.txt",sep="_")
			cate = "HiSeq.hg19.mirbase20"
			if (!file.exists(fileName)) {
				fileName = paste(cancerType,"mir_GA.hg19.mirbase20_tumor_expression.txt",sep="_")
				cate = "GA.hg19.mirbase20"
			}
		}

		if(file.exists(fileName) && file.info(fileName)$size != 0){
			data = read.table(fileName,sep='\t', header=TRUE, row.names=1)

			subject = as.character(unlist(colnames(data)[1:ncol(data)]))

			#DESeq
			subject <- factor(subject)
	
			samples <- data.frame(row.names=colnames(data), condition=subject)
			data4 <- DESeqDataSetFromMatrix(countData = data, colData=samples,design=~condition)
			dds <- estimateSizeFactors(data4)
			
			#dds=DESeq(data4)
			setwd(paste("/data/projects/bioxpress/generated/logs-step8/",type,sep=""))
			foo = counts(dds, normalized = TRUE)
			write.table(foo, paste(cancerType,cate,"normailzed_dds_tumor_expression.csv",sep="_"),sep=",")
		}
	}
}

#########################################################################
#########This part is for ICGC, but the data format is not right. Need to 
#########change it later.
########################################################################

for (cancerType in c('MALY','CLLE','RECA','PAEN','LIRI','PACA','BRCA','OV')){

        for (type in c('miRNAseq', 'RNAseq')){
                setwd(paste("/data/projects/bioxpress/generated/logs-step7/",type,sep=""))
		fileName = paste(cancerType,"_icgc_tumor_expression.txt",sep="_")

                if (type == "RNAseq"){
                        cate = "RNAseq"

                } else {
                        cate = "miRNAseq"
                }

                if(file.exists(fileName) && file.info(fileName)$size != 0){
                        data = read.table(fileName,sep='\t', header=TRUE, row.names=1)

                        subject = as.character(unlist(colnames(data)[1:ncol(data)]))

                        #DESeq
                        subject <- factor(subject)

                        samples <- data.frame(row.names=colnames(data), condition=subject)
                        data4 <- DESeqDataSetFromMatrix(countData = data, colData=samples,design=~condition)
                        dds <- estimateSizeFactors(data4)

                        #dds=DESeq(data4)
                        setwd(paste("/data/projects/bioxpress/generated/logs-step8/",type,sep=""))
                        foo = counts(dds, normalized = TRUE)
                        write.table(foo, paste(cancerType,cate,"icgc_normailzed_dds_tumor_expression.csv",sep="_"),sep=",")
                }
        }
}



