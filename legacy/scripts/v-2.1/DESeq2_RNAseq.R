#source("http://bioconductor.org/biocLite.R")
#biocLite("DESeq2")

library(DESeq2)
for (cancerType in c('ESCA','LUAD','PAAD','LIHC','STAD', 'CHOL', 'COAD', 'THCA', 'KICH', 'KIRP', 'KIRC', 'PRAD', 'PCPG', 'HNSC', 'SARC', 'LUSC', 'SKCM', 'THYM', 'BLCA', 'BRCA', 'UCEC', 'READ', 'CESC')){

	type = "RNAseq"
		setwd(paste("/data/projects/bioxpress/generated/logs-step2/",type,sep=""))
		if (type == "RNAseq"){
			fileName = paste(cancerType,type,"RNAseq_DESeq2.txt",sep="_")
			subjectFile = paste(cancerType,"RNAseq_subject.txt",sep="_")
			treatFile = paste(cancerType,"RNAseq_treat.txt",sep="_")
			cate = "RNAseq"
		} else {
			fileName = paste(cancerType,"HiSeq.hg19.mirbase20_DESeq2.txt",sep="_")
			subjectFile = paste(cancerType,"HiSeq.hg19.mirbase20_subject.txt",sep="_")
			treatFile = paste(cancerType,"HiSeq.hg19.mirbase20_treat.txt",sep="_")
			cate = "HiSeq.hg19.mirbase20"
			if (!file.exists(fileName)){
				fileName = paste(cancerType,"GA.hg19.mirbase20_DESeq2.txt",sep="_")
				subjectFile = paste(cancerType,"GA.hg19.mirbase20_subject.txt",sep="_")
				treatFile = paste(cancerType,"GA.hg19.mirbase20_treat.txt",sep="_")
				cate = "GA.hg19.mirbase20"
			}
		}
		if(file.exists(fileName) && file.info(fileName)$size != 0){
		        data = read.table(fileName,sep='\t', header=TRUE, row.names=1)
        		subject = read.table(subjectFile)
	        	treat = read.table(treatFile)

	        	subject = as.character(unlist(subject))
			subject[2]
		        treat = as.character(unlist(treat))

        		#DESeq
		        subject <- factor(subject)
        		treat <- factor(treat, levels=c("cancer","normal"))

			setwd(paste("/data/projects/bioxpress/generated/logs-step4/",type,sep=""))
			for (j in subject){
				j = gsub('-','.',j)
				dataAna = data[,grep(as.character(j),colnames(data))]
				if (ncol(dataAna) > 1){
					samples <- data.frame(row.names=colnames(data), condition=treat,type=subject)
					data4 <- DESeqDataSetFromMatrix(countData = data, colData=samples,design=~condition+type)
					dds=DESeq(data4)
					res <- results(dds, contrast=c('condition','cancer','normal'))
					
					resOrdered <- res[order(res$padj),]
					head(resOrdered)
					summary(res,alpha=0.01)
					write.table(resOrdered,paste(cancerType,j,cate,"DESeq_results_new.csv",sep="_"),sep=",")
					foo = counts(dds, normalized = TRUE)
					write.table(foo, paste(cancerType,j,cate,"normailzed_dds.csv",sep="_"),sep=",")
					#pdf(paste(cancerType,j,cate,'plot.pdf',sep="_"))
					#plotMA(res, main=paste(cancerType,j,cate,"differential expression", sep=" "), ylim=c(-8,8), alpha = 0.05)
					#rld <- rlogTransformation(dds, blind=TRUE)
					#plotPCA(rld, intgroup = 'condition')
					#dev.off()
				}
			}
		}
}


