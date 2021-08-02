args <- commandArgs(trailingOnly=TRUE)

# test if there is at least one argument: if not, return an error
if (length(args)!= 3) {
  stop("Three arguments must be supplied.
       The First argument is Config File.
       The second argument is Source Name.
       The third argument is Cancer Type\n", call.=FALSE)

} else {
  # default output file
  library(jsonlite)
  configJson <- fromJSON(args[1], flatten=TRUE)
  rsrcName <- args[2]
  cancerType <- args[3]
}

#################################################################
library(cluster)
library(clusterSim)
library(ade4)
#################################################################

dataDir <- configJson$sampleqc$inputdir
outDir <- configJson$sampleqc$outputdir

inFile <- paste(dataDir,rsrcName,"-",cancerType,"-extract-all.csv",sep="")

#data <- read.table("/data/projects/metagenomics/enterotyping/MetaHIT_SangerSamples.genus.txt", header=T, row.names=1, dec=".", sep="\t")
#data=read.table("/data/projects/metagenomics/enterotyping/genus.csv", header=T, row.names=1, dec=".", sep=",")
data <- read.csv(file=inFile, header=TRUE, row.names=1, dec=".", sep=",")

data=data[-1,]

KLD <- function(x,y) sum(x * log(x/y))
JSD <- function(x,y) sqrt(0.5 * KLD(x, (x+y)/2) + 0.5 * KLD(y, (x+y)/2))

dist.JSD <- function(inMatrix, pseudocount=0.000001, ...) {
	KLD <- function(x,y) sum(x *log(x/y))
	JSD<- function(x,y) sqrt(0.5 * KLD(x, (x+y)/2) + 0.5 * KLD(y, (x+y)/2))
	matrixColSize <- length(colnames(inMatrix))
	matrixRowSize <- length(rownames(inMatrix))
	colnames <- colnames(inMatrix)
	resultsMatrix <- matrix(0, matrixColSize, matrixColSize)
        
	inMatrix = apply(inMatrix,1:2,function(x) ifelse (x==0,pseudocount,x))

	for(i in 1:matrixColSize) {
		for(j in 1:matrixColSize) { 
			resultsMatrix[i,j]=JSD(as.vector(inMatrix[,i]), as.vector(inMatrix[,j]))
		}
	}
	colnames -> colnames(resultsMatrix) -> rownames(resultsMatrix)
	as.dist(resultsMatrix)->resultsMatrix
	attr(resultsMatrix, "method") <- "dist"
	return(resultsMatrix) 
 }



#ALGORITHM
data.dist = dist.JSD(data)
pam.clustering = function(x,k) { # x is a distance matrix and k the number of clusters
	require(cluster)
	cluster = as.vector(pam(as.dist(x), k, diss=TRUE)$clustering)
	return(cluster)
}
#say we decided to cluster with cluster size=3
data.cluster=pam.clustering(data.dist, k=3)



#OPTIMAL NUMBER OF CLUSTERS
require(clusterSim)
nclusters = index.G1(t(data), data.cluster, d = data.dist, centrotypes = "medoids")

nclusters = NULL
for (k in 1:20) { 
	if (k==1) {
		nclusters[k]=NA 
	} else {
		data.cluster_temp=pam.clustering(data.dist, k)
		nclusters[k]=index.G1(t(data),data.cluster_temp,  d = data.dist, centrotypes = "medoids")
	}
}

png('clustersizes.png')
plot(nclusters, type="h", xlab="k clusters", ylab="CH index")
dev.off()




#CLUSTER VALIDATION
obs.silhouette=mean(silhouette(data.cluster, data.dist)[,3])




#BETWEEN-CLASS ANALYSIS (BCA)
#Prior to this analysis, in the Illumina dataset, genera with very low abundance were removed to decrease the noise, if their average abundance across all samples was below 0.01%. 

noise.removal <- function(dataframe, percent=0.01, top=NULL){
	dataframe->Matrix
	bigones <- rowSums(Matrix)*100/(sum(rowSums(Matrix))) > percent 
	Matrix_1 <- Matrix[bigones,]
	print(percent)
	return(Matrix_1)
}

#data=noise.removal(data, percent=0.01)

require(ade4)
## plot 1
obs.pca=dudi.pca(data.frame(t(data)), scannf=F, nf=10)
obs.bet=bca(obs.pca, fac=as.factor(data.cluster), scannf=F, nf=k-1) 
dev.new()
s.class(obs.bet$ls, fac=as.factor(data.cluster), grid=F,sub="Between-class analysis")

#plot 2
obs.pcoa=dudi.pco(data.dist, scannf=F, nf=3)
dev.new()
s.class(obs.pcoa$li, fac=as.factor(data.cluster), grid=F,sub="Principal coordiante analysis")
