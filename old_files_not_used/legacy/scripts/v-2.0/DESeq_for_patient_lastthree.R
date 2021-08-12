#setwd("~/Desktop/bioxpress")
source("http://bioconductor.org/biocLite.R")
biocLite("DESeq2")

library(DESeq2)

for (cancer_type in c('THCA','STAD','UCEC')){
dir.create(cancer_type)
data=read.table(paste(cancer_type,"_resultscreening.txt",sep=""),sep='\t') #the seconde row needs revise
names1=read.table(paste(cancer_type,"_orderednames.txt",sep=""))
names1=as.character(unlist(names1))
g=NA
names=as.character(unique(unlist(names1)))
list=data[1,1:c(ncol(data))-1]  #Lung and kidney do not need "-1"
for (i in names){
  a=grep(i,as.character(unlist(list)))
  g=c(g,a)
}
g=g[-1]
ordered=data[,c(1,g)]
colnames(ordered)=c("Hybridization",names1)
ordered=ordered[-1,]
a=ordered[,1]
ordered=ordered[,-1]
rownames(ordered)=a


#DEG

#BLCA,BRCA,ESCA,HNSC,KICH,KIRC,KIRP,LIHC,LUAD,LUSC,PRAD,STAD,UCEC
data=ordered
data_screened=NA
for (i in 1:ncol(data)) {
  if (data[1,i]==c("raw_count")) {
    data_screened=data.frame(data_screened,data[,i])
  }
}
data_screened=data_screened[,-1]
data_screened=data.frame(rownames(data),data_screened)
data_screened=data_screened[-1,]

name=read.table(paste(cancer_type,"_type.txt",sep=""))
name=unique(as.character(unlist(name)))
name=c("transcript_id",name)

colnames(data_screened)=name
data2=data_screened

#exclude miRNAs with no expression
express=NA
for (i in 1:nrow(data2)){
  if (sum(as.numeric(as.character(unlist(data2[i,2:ncol(data2)]))))>0){
    express=c(express,i)
  }
}
express=express[-1]
data2=data2[express,]

write.table(data2,"data2_patient.txt")
data2<- read.table("data2_patient.txt", header=TRUE, row.names=1)
rownames(data2)=data2[,1]
data2=data2[,-1]
for (i in 1:ncol(data2)){
	 data2[,i]=as.integer(data2[,i])
}

#filteration

#DEG--paired sample
conditions=function(x){
  con=c("NA")
  for (i in x){
    if (grepl("cancer",i)) {
      con=c(con,"cancer") 
    }
    else con=c(con,"normal")
  }
  con=con[-1]
  con
}

condition=read.table(paste(cancer_type,"_condition.txt",sep=""))
condition=as.character(unlist(condition[,1]))
condition=gsub("-",".",condition)

condition=unique(condition)
subject=condition
design <- model.matrix(~subject)

for (j in condition){
  data_analy=data2[,grep(j,colnames(data2))]
  if (length(grep(j,colnames(data2)))>1){
    samples <- data.frame(row.names=colnames(data2)[grep(j,colnames(data2))], condition=as.factor(conditions(colnames(data2)[grep(j,colnames(data2))])))
    data3 <- DESeqDataSetFromMatrix(countData = data_analy, colData=samples, design=~condition)
    dds=DESeq(data3)
    res <- results(dds) 
    write.csv(res,file=paste(cancer_type,"/",j,sep=""))
  }
}

}


