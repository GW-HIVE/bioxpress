#packages <- c("HGNChelper", "httr", "RCurl", "rjson", "stringr")
#install.packages(packages, dependencies = T)

library(HGNChelper)
library(httr)
library(RCurl)
library(rjson)
library(stringr)


setwd("/home/yuhu/bioxpress/TCGA-Assembler/TCGA-Assembler/")
source("./Module_A.R")
source("./Module_B.R")
sPath1 <- "./QuickStartExample/Part1_DownloadedData/RNAseq"
sPath2 <- "./QuickStartExample/Part1_DownloadedData/miRNAseq"
sCancer <- c('ACC','BLCA','LGG','BRCA','CESC','CHOL','COAD','ESCA','FPPP','LAML', 'GBM','HNSC','KICH','KIRC','KIRP','LIHC','LUAD','LUSC','DLBC','MESO','OV','PAAD','PCPG','PRAD','READ','SARC','SKCM','STAD','TGCT','THYM','THCA','UCS','UCEC','UVM')


for (i in sCancer){
	path_geneExp <- DownloadRNASeqData(cancerType = i, assayPlatform = "gene_RNAseq", saveFolderName = sPath1)

	path_miRNAExp1 <- DownloadmiRNASeqData(cancerType = i, assayPlatform = "mir_GA.hg19.mirbase20", saveFolderName = sPath1)

	path_miRNAExp2 <- DownloadmiRNASeqData(cancerType = i, assayPlatform = "mir_HiSeq.hg19.mirbase20", saveFolderName = sPath1)
}
