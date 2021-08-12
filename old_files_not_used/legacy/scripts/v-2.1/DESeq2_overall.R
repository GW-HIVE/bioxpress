#source("https://bioconductor.org/biocLite.R")
#biocLite("DESeq2")

library(DESeq2)
for (cancerType in c('ESCA','LUAD','PAAD','LIHC','STAD', 'CHOL', 'COAD', 'THCA', 'KICH', 'KIRP', 'KIRC', 'PRAD', 'PCPG', 'HNSC', 'SARC', 'LUSC', 'SKCM', 'THYM', 'BLCA', 'BRCA', 'UCEC', 'READ', 'CESC')){

	#for (type in c('miRNAseq', 'RNAseq')){
		type = "miRNAseq"
		setwd(paste("/data/projects/bioxpress/generated/logs-step2/",type,sep=""))

		if (type == "RNAseq"){
			fileName = paste(cancerType,type,"RNAseq_DESeq2.txt",sep="_")
			subjectFile = paste(cancerType,"RNAseq_subject.txt",sep="_")
			treatFile = paste(cancerType,"RNAseq_treat.txt",sep="_")
			cate = ""

		} else {
			fileName = paste(cancerType,"HiSeq.hg19.mirbase20_DESeq2.txt",sep="_")
			subjectFile = paste(cancerType,"HiSeq.hg19.mirbase20_subject.txt",sep="_")
			treatFile = paste(cancerType,"HiSeq.hg19.mirbase20_treat.txt",sep="_")
			cate = "HiSeq.hg19.mirbase20"
			if (!file.exists(fileName)) {
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
			treat = as.character(unlist(treat))

			#DESeq
			subject <- factor(subject)
			treat <- factor(treat, levels=c("cancer","normal"))
	
			samples <- data.frame(row.names=colnames(data), condition=treat,type=subject)
			data4 <- DESeqDataSetFromMatrix(countData = data, colData=samples,design=~condition+type)
			dds=DESeq(data4)
			res <- results(dds, contrast=c('condition','cancer','normal'))

			resOrdered <- res[order(res$padj),]
			head(resOrdered)
			summary(res,alpha=0.01)
	
			setwd(paste("/data/projects/bioxpress/generated/logs-step3/",type,sep=""))
			write.table(resOrdered,paste(cancerType,cate,"DESeq_results_new.csv",sep="_"),sep=",")
			foo = counts(dds, normalized = TRUE)
			write.table(foo, paste(cancerType,cate,"normailzed_dds.csv",sep="_"),sep=",")
			pdf(paste(cancerType,'_plot.pdf',sep=""))
			plotMA(res, main=paste(cancerType,cate," differential expression",sep=" "), ylim=c(-8,8), alpha = 0.05)
			rld <- rlogTransformation(dds, blind=TRUE)
			plotPCA(rld, intgroup = 'condition')
			dev.off()
		}
	#}
}

