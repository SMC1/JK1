setwd('/EQL3/pipeline/identity/')
#setwd('/EQL5/pipeline/CRC_identity')
files = dir(pattern="signature$", path="/EQL3/pipeline/identity")
#files = dir(pattern="signature$", path="/EQL5/pipeline/CRC_identity")
dat<-data.frame(0)
for (file in files)
{
  sid=gsub(pattern=".snp_signature", replacement="", x=file, fixed=T)
  print(sprintf("%s %s", sid, file))
  tmp<-read.table(file, header=F, sep="\t", colClasses=c("NULL","NULL","numeric"))
  colnames(tmp)<-c(sid)
  if (file == files[1])
  {
    dat<-tmp
  } else {
    dat<-cbind(dat, tmp)
  }
}

cr<-cor(dat, use='pairwise.complete.obs')

#pdf(file="/EQL3/pipeline/identity/clustering_20140617.pdf",width=40)
#pdf(file="/EQL3/pipeline/identity/clustering_20140625.pdf", width=45)
#pdf(file="/EQL3/pipeline/identity/clustering_20140903.pdf", width=50)
#pdf(file="/EQL3/pipeline/identity/clustering_20140918.pdf", width=50)
#pdf(file="/EQL3/pipeline/identity/clustering_20141006.pdf", width=50)
#pdf(file="/EQL3/pipeline/identity/clustering_20141014.pdf", width=50)
#pdf(file="/EQL3/pipeline/identity/clustering_20141118.pdf", width=60)
#pdf(file="/EQL3/pipeline/identity/clustering_20141209.pdf", width=70)
pdf(file="/EQL3/pipeline/identity/clustering_20150123.pdf", width=70)
#pdf(file="/EQL5/pipeline/CRC_identity/clustering_CRC.pdf", width=40)
plot(hclust(dist(cr)))
dev.off()

#write.table(cr, file='/EQL3/pipeline/identity/corr_matrix_20140617.txt', sep="\t", row.names=T, col.names=T, quote=F)

#plot(density(cr[upper.tri(cr,diag=F)]))

##
#IDs<-colnames(dat)
#for (i in 1:(length(IDs)-1))
#{
#  for (j in (i+1):length(IDs))
#  {
#    tmp<-c(IDs[i], IDs[j],cr[IDs[i],IDs[j]], "Diff")
#    write.table(t(tmp), append=T, file="haha", sep="\t", quote=F, row.names=F, col.names=F)
#  }
#}
#
#tab<-read.table('/EQL3/pipeline/identity/pairwise_20140605',header=F,sep="\t",colClasses=c("character","character","numeric","character"))
#colnames(tab)<-c('X1','X2','cor','grp')
#p<-ggplot(tab)
#p+geom_boxplot(aes(x=grp,y=cor))


