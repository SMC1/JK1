args<-commandArgs(trailingOnly=T)

matFile=args[1]
sid=args[2]
outName=args[3]

mat<-read.table(matFile,sep='\t', colClasses=c("character","character","numeric"))

colnames(mat)<-c('SID','Gene','RPKM')
mat$Grp<-'Control'
mat$Grp[ mat$SID == sid ]<-sid

library(ggplot2)
format<-substr(outName, nchar(outName)-2, nchar(outName))
if (format == 'png') {
	png(outName, width=1800)
} else {
	pdf(outName, width=20)
}
p<-ggplot(mat)
p+geom_boxplot(aes(x=Gene,y=RPKM,color=Grp))+theme(axis.text.x=element_text(angle=90,hjust=1))+ggtitle(sid)+scale_y_log10()
dev.off()
