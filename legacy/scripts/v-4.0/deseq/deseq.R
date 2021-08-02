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


#upload DESeq2 library
write("Loading DESeq2 libarary",file = progressFile, append = TRUE)
library(DESeq2)

#create deseq data set 
write("Creating deseq data set from matrix",file = progressFile, append = TRUE)
ddsMat <- DESeqDataSetFromMatrix(countData = assay,
                                  colData = coldata,
                                  design = ~status )

#run DEseq
write("Beginning DESeq",file = progressFile, append = TRUE)
dds <- DESeq(ddsMat)

#save 
saveRDS(dds,paste(assayFile,'.dds',sep=""))

#write output
write("Completed DESeq starting output",file = progressFile, append = TRUE)
#print normalized hit counts
norm <- counts(dds, normalized = TRUE)
write.csv(norm,"deSeq_reads_normalized.csv", row.names = TRUE)

#results
res<-results(dds)
resOrdered <- res[order(res$padj),]
resSig <- subset(resOrdered)
write.csv(as.data.frame(resSig),
          file="results_significance.csv")


#plotting
#get transformed values
vsd <- vst(dds, blind=FALSE)

write("Plotting Distance Heatmap",file = progressFile, append = TRUE)
sampleDists <- dist(t(assay(vsd)))
library("RColorBrewer")
sampleDistMatrix <- as.matrix(sampleDists)
rownames(sampleDistMatrix) <- paste(vsd$condition, vsd$type, sep="-")
colnames(sampleDistMatrix) <- NULL
colors <- colorRampPalette( rev(brewer.pal(9, "Blues")) )(255)

write("Plotting Distance Heatmap",file = progressFile, append = TRUE)
png("pca.png")
plotPCA(vsd, intgroup="status")
dev.off()

write("Plotting Dispersion Plot",file = progressFile, append = TRUE)
png("dispersion.png")
plotDispEsts(dds)
dev.off()
png("distance_heatmap.png")
pheatmap(sampleDistMatrix,
         clustering_distance_rows=sampleDists,
         clustering_distance_cols=sampleDists,
         col=colors)
dev.off()


