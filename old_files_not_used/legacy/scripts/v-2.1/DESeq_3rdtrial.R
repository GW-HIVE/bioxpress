#BLCA,BRCA,ESCA,HNSC,KICH,KIRC,KIRP,LIHC,LUAD,LUSC,PRAD,STAD,UCEC
setwd("/data/projects/bioxpress/")
source("http://bioconductor.org/biocLite.R")
biocLite("DESeq2")

library(DESeq2)
for (cancer_type in c('BLCA','BRCA','ESCA','HNSC','KICH','KIRC','KIRP','LIHC','LUAD','LUSC','PRAD','STAD','UCEC','THCA')){
  data=read.table(paste(cancer_type,"_unpaired.txt",sep=""),sep='\t') #the seconde row needs revise
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
rownames(ordered)=ordered[,1]
ordered=ordered[,-1]
ordered=ordered[-1,]


#DEG
library(DESeq2)
#BLCA,BRCA,ESCA,HNSC,KICH,KIRC,KIRP,LIHC,LUAD,LUSC,PRAD,STAD,UCEC
data=ordered
data_screened=NA
for (i in 1:ncol(data)) {
  if (data[1,i]==c("read_count")) {
    data_screened=data.frame(data_screened,data[,i])
  }
}
data_screened=data_screened[,-1]
data_screened=data.frame(rownames(data),data_screened)
data_screened=data_screened[-1,]

name=read.table(paste(cancer_type,"_type.txt",sep=""))
x=seq(2,length(name),2)
name=as.character(unlist(name))[-x]
name=c("miRNA",name)

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

write.table(data2,"data2.txt")
data2<- read.table("data2.txt", header=TRUE, row.names=1)
rownames(data2)=data2[,1]
data2=data2[,-1]

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

x=seq(2,length(condition),2)
condition=condition[-x]
subject=condition

#change the position of cancer and normal
data3=NA
for (i in 1:length(unique(subject))){
  pos=grep(unique(subject)[i],colnames(data2))
  order_pos=NA
  for (j in pos){
    inter=paste(colnames(data2)[j],as.character(j),sep="-")
    order_pos=c(order_pos,inter)
  }
  order_pos=order_pos[-1]
  order_pos=order_pos[order(order_pos,decreasing = TRUE)]
  after_sort=NA
  for (a in order_pos){
    inter=unlist(strsplit(a,"-"))
    after_sort=c(after_sort,as.numeric(inter[2]))
  }
  after_sort=after_sort[-1]
  data3=data.frame(data3,data2[,after_sort])
}
data3=data3[,-1]

treatment=conditions(colnames(data3))
#DESeq
subject <- factor(subject)
treat <- factor(treatment, levels=c("cancer","normal"))
design <- model.matrix(~subject+treat)

samples <- data.frame(row.names=colnames(data2), condition=treat,type=subject)
data4 <- DESeqDataSetFromMatrix(countData = data2, colData=samples,design=~condition+type)
dds=DESeq(data4)
ddsMF=dds
design(ddsMF)=formula(~type+condition)
ddsMF=DESeq(ddsMF)
res <- results(ddsMF) 
resOrdered <- res[order(res$padj),]
head(resOrdered)
summary(res,alpha=0.01)
write.table(resOrdered,paste(cancer_type,"_DESeq_results.csv",sep=""),sep=",")
}
#plotMA(res,ylim=c(-8,8),alpha=0.01,main="BLCA Differential Expression miRNA")
