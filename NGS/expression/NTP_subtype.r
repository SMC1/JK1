input.features.filename="/EQL1/TCGA/GBM/subtype/TCGA_GBM_subtype_genelist.nsg" #1:P 2:N 3:C 4:M 5:U
input.exp.filename='/EQL1/NSL/RNASeq/results/expression/NSL_GBM_RPKM_118_lg2.gct'
norm.method="row.std" # "row.std",row.std.ref","ratio.ref"
temp.nn.wt="F"
dist.selection="cosine"
outFileName <-'/EQL1/NSL/RNASeq/NSL_GBM_RPKM_118_subtype.dat'

#  suppressWarnings()

# Advanced setting

ref.sample.file=NA
within.sig="F"
plot.nominal.p="F"
plot.distance="F"
dchip.output="F"
signature.heatmap="T"
FDR.sample.bar=0.05 # NA if not needed
plot.FDR="T"
col.range=3         # SD in heatmap
heatmap.legend=signature.heatmap
histgram.null.dist="F" # histgram of null dist for the distance
hist.br=30



features<-read.delim(input.features.filename,header=F,check.names=F)

## file format check
if (length(features[1,])!=3 & length(features[1,])!=4){
  stop("### Please use features file format! ###")
}

third.col<-rownames(table(features[,3]))
if (is.na(as.numeric(third.col[1]))){
  stop("### The 3rd column of feature file should be numerical! ###")
}

feat.col.names<-colnames(features)
feat.col.names[1:2]<-c("ProbeID","GeneName")
colnames(features)<-feat.col.names

num.features<-length(features[,1])
num.cls<-length(table(features[,3]))
feature.col.num <- length(features[1,])

ord<-seq(1:num.features)
features<-cbind(ord,features)  # add order column to "features"


# expression data
## file format check
if (regexpr(".gct$",input.exp.filename)==-1){
  stop("### Gene expression data should be .gct format! ###")
}
exp.dataset<-read.delim(input.exp.filename,header=T,skip=2,check.names=F)
exp.sd <- apply(exp.dataset[,-(1:2)],1,sd,na.rm=T)
exp.dataset<-exp.dataset[exp.sd!=0,]
colnames(exp.dataset)[1:2] <- c("ProbeID","GeneName")

## Other dataset's mean & SD for row normalization (optional)
if (!is.null(ref.sample.file)){
  ref.sample <- read.delim(ref.sample.file,header=T)
  if (dim(ref.sample)[2]!=4 & is.numeric(ref.sample[1,3]) & is.numeric(ref.sample[1,4])){
    stop("### mean & SD file format incorrect! ###")
  }
  colnames(ref.sample)[1:4] <- c("ProbeID","SomeName","mean","sd")
  merged.dataset <- merge(ref.sample,exp.dataset,sort=F)
  
  ref.sample <- merged.dataset[,1:4]
  exp.dataset <- merged.dataset[,c(1,5:dim(merged.dataset)[2])]
}


ProbeID<-exp.dataset[,1]
gene.names<-exp.dataset[,2]
num.samples<-(length(exp.dataset[1,])-2)
exp.dataset<-exp.dataset[-c(1:2)]

exp.for.sample.names<-read.delim(input.exp.filename,header=F,skip=2)  # read sample names
sample.names<-as.vector(as.matrix(exp.for.sample.names[1,3:length(exp.for.sample.names[1,])]))


# row normalize

normed.exp.dataset<-exp.dataset

if (norm.method=="row.std"){
  exp.mean <- apply(exp.dataset,1,mean,na.rm=T)
  exp.sd <- apply(exp.dataset,1,sd,na.rm=T)
  normed.exp.dataset<-(exp.dataset-exp.mean)/exp.sd   
}
if (norm.method=="row.std.ref"){
  if (is.null(ref.sample)){
    stop("### Provide reference sample data! ###")
  }
  exp.mean <- as.numeric(as.vector(ref.sample$mean))
  exp.sd <- as.numeric(as.vector(ref.sample$sd))
  normed.exp.dataset<-(exp.dataset-exp.mean)/exp.sd   
}
if (norm.method=="ratio.ref"){
  if (is.null(ref.sample)){
    stop("### Provide reference sample data! ###")
  }
  exp.mean <- as.numeric(as.vector(ref.sample$mean))
  normed.exp.dataset<- exp.dataset/exp.mean 
}    

normed.exp.dataset<-cbind(ProbeID,normed.exp.dataset)


# extract features from normed.exp.dataset

exp.dataset.extract<-merge(features,normed.exp.dataset,sort=F)
if (length(exp.dataset.extract[,1])<1){
  stop("### No matched probes! ###")
}

order.extract<-order(exp.dataset.extract[,2])
exp.dataset.extract<-exp.dataset.extract[order.extract,]
order.extract.after<-exp.dataset.extract[,2]
exp.dataset.extract<-exp.dataset.extract[-2]

if (temp.nn.wt=="F"){
  features.extract<-exp.dataset.extract[,1:3]
  if (feature.col.num==4){
    exp.dataset.extract <- exp.dataset.extract[-4]
  }
  features.extract<-cbind(order.extract.after,features.extract) # order:ProbeID:gene name:cls:wt(if any)
  num.features.extract<-length(features.extract[,1])
  
  ProbeID.extract<-as.vector(exp.dataset.extract[,1])
  exp.dataset.extract<-exp.dataset.extract[-c(1:3)]
  rownames(exp.dataset.extract)<-ProbeID.extract
}

#  temp.nn.wt.vector <- rep(1,num.features)

if (temp.nn.wt=="T"){
  features.extract<-exp.dataset.extract[,1:4]
  features.extract<-cbind(order.extract.after,features.extract) # order:ProbeID:gene name:cls:wt(if any)
  
  #    if (is.numeric(features[,4])){
  temp.nn.wt.vector <- as.numeric(as.vector(features.extract[,5]))
  #    }else{
  if (is.numeric(temp.nn.wt.vector)==F){
    stop("# Please use numeric values in 4th column!#")
  }
  
  num.features.extract<-length(features.extract[,1])
  
  ProbeID.extract<-as.vector(exp.dataset.extract[,1])
  exp.dataset.extract<-exp.dataset.extract[-c(1:4)]
  rownames(exp.dataset.extract)<-ProbeID.extract
}

# make template

for (i in 1:num.cls){
  temp.temp<-as.numeric(as.vector(features.extract[,4]))
  temp.temp[temp.temp!=i]<-0 #-1 or 0
  temp.temp[temp.temp==i]<-1
  eval(parse(text=paste("temp.",i,"<-temp.temp",sep="")))
  #    eval(parse(text=paste("temp\.",i,"<-temp\.temp",sep="")))  ### for < R-2.4.0
}

# weighted template (only for 2cls)

if (temp.nn.wt=="T"){
  temp.1 <- temp.nn.wt.vector * temp.1
  temp.2 <- temp.nn.wt.vector * temp.2
  temp.3 <- temp.nn.wt.vector * temp.3
  temp.4 <- temp.nn.wt.vector * temp.4
}


### compute distance and p-value ###

predict.label<-vector(length=num.samples,mode="numeric")
dist.to.template<-vector(length=num.samples,mode="numeric")



outFile <- file(outFileName,'wt')
#writeLines(sprintf('sId%s\tclosest.temp',paste("\t",c(1:num.cls),collapse="",sep="")), outFile)

for (i in 1:num.samples){
  sId = sample.names[i]
  current.sample <- as.vector(exp.dataset.extract[,i])
  
  # compute original distance
  
  orig.dist.to.all.temp <- vector(length=num.cls,mode="numeric")
  
  if (temp.nn.wt=="T"){   # weight sample data
    current.sample <- current.sample*abs(temp.nn.wt.vector)
  }
  
  dist.to.all.template = orig.dist.to.all.temp
  
  if (dist.selection=="cosine"){
    for (o in 1:num.cls){      # compute distance to all templates
      eval(parse(text=paste("current.temp <- temp.",o,sep="")))
      #        eval(parse(text=paste("current\.temp <- temp\.",o,sep="")))  ### for < R-2.4.0
      orig.dist.to.all.temp[o]<-sum(current.temp*current.sample)/
        (sqrt(sum(current.temp^2))*sqrt(sum(current.sample^2)))
      dist.to.all.template[o]<-round(orig.dist.to.all.temp[o],4)
    }
  }
  if (dist.selection=="correlation"){
    for (o in 1:num.cls){      # compute distance to all templates
      eval(parse(text=paste("current.temp <- temp.",o,sep="")))
      #        eval(parse(text=paste("current\.temp <- temp\.",o,sep="")))  ### for < R-2.4.0
      orig.dist.to.all.temp[o] <- cor(current.temp,current.sample,method="pearson",use="complete.obs")
      dist.to.all.template[o]<-round(orig.dist.to.all.temp[o],4)
    }
  }
  
  
  if (num.cls>=2){
    for (o in 1:num.cls){       # find nearest neighbor (>2 classes)
      if (is.na(orig.dist.to.all.temp[o])!=T){
        if (orig.dist.to.all.temp[o]==max(orig.dist.to.all.temp,na.rm=T)){
          predict.label<-o
        }
      }
    }
  }
  
  predict.label = sub(1,"P",predict.label)
  predict.label = sub(2,"N",predict.label)
  predict.label = sub(3,"C",predict.label)
  predict.label = sub(4,"M",predict.label)
  predict.label = sub(5,"U",predict.label)
  
  sum = c(dist.to.all.template,predict.label)
  writeLines(sprintf('%s%s',sId,paste("\t",as.character(sum),collapse="",sep="")), outFile)
}

close(outFile)

