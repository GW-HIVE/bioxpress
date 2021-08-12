library(pheatmap)
library(DESeq2)
library("RColorBrewer")

# for sorting the columns and rows of the count and category files
library(dplyr)

# take arguments 
args <- commandArgs(TRUE)
setwd(args[1])
out_dir <- args[1]
assayFile <- args[2]
colFile <- args[3]
progressPath <- args[4]
progressFile <- file(progressPath)

print(paste("Starting DESeq for ", assayFile))



# read in hit counts and disable automatic labeling of columns (check.names)
print("Reading hit counts")
write("Reading in hit counts (assayFile)",file = progressFile)
assay<-read.csv(assayFile, row.names=1, check.names=FALSE)
# sort the columns by alphabetical order
assay <- assay %>% select(order(colnames(assay)))

# read in category table
print("Reading categories table")
write("Reading in category table (colFile)",file = progressFile, append = TRUE)
coldata<-read.csv(colFile)
# sort the rows by alphabetical order
coldata <- coldata %>% arrange(id)

# create deseq data set
print("Creating DESeq dataset") 
write("Creating deseq data set from matrix",file = progressFile, append = TRUE)
ddsMat <- DESeqDataSetFromMatrix(countData = assay,
                                  colData = coldata,
                                  design = ~status )

# run DEseq
print("Running DESeq")
write("Beginning DESeq",file = progressFile, append = TRUE)
dds <- DESeq(ddsMat)


# save 
print("Saving counts.dds file")
saveRDS(dds,paste(assayFile,'.dds',sep=""))

# print normalized hit counts
print("printing normalized hit counts")
norm <- counts(dds, normalized = TRUE)
write.csv(norm,"deSeq_reads_normalized.csv", row.names = TRUE)

# results
print("Creating results and significance file")
res<-results(dds, contrast=c('status','Primary-Tumor','Solid-Tissue-Normal'))
resOrder <- res[order(res$padj),]
resSig <- subset(resOrder)
write.csv(as.data.frame(resSig),
          file="results_significance.csv")


# plotting
# get transformed values
print("Generating heat maps and PCA plots")
vsd <- vst(dds, blind=FALSE)

write("Plotting Distance Heatmap",file = progressFile, append = TRUE)
sampleDists <- dist(t(assay(vsd)))
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

print(paste("Finished DESeq and written to ", out_dir))


