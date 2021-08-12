library(pheatmap)
args <- commandArgs(TRUE)
setwd(args[1])
assayFile <- args[2]
colFile <- args[3]
progressPath <- args[4]
progressFile <- file(progressPath)

#read in hit counts
write("Reading in hit counts (assayFile)",file = progressFile)
assay<-read.csv(assayFile, row.names=1)

#read in category table
write("Reading in category table (colFile)",file = progressFile, append = TRUE)
coldata<-read.csv(colFile)


#upload DESeq library
write("Loading DESeq libarary",file = progressFile, append = TRUE)
library(DESeq2)


#create deseq data set 
write("Creating deseq data set from matrix",file = progressFile, append = TRUE)
ddsMat <- DESeqDataSetFromMatrix(countData = assay,
                                  colData = coldata,
                                  design = ~status )

rld <- rlogTransformation( ddsMat )
res <- data.frame(
   assay(rld), 
   avgLogExpr = ( assay(rld)[,2] + assay(rld)[,1] ) / 2,
   rLogFC = assay(rld)[,2] - assay(rld)[,1] )


resOrdered <- res[ order(res$rLogFC), ]
write.csv(as.data.frame(resOrdered), file="results.csv")



