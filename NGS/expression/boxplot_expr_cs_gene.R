args<-commandArgs(trailingOnly=T)

matFile=args[1]
sid=args[2]
outName=args[3]

mat<-read.table(matFile,sep='\t', colClasses=c("character","character","numeric"))

colnames(mat)<-c('SID','Gene','RPKM')
size_mbt=length(unique(grep(pattern="MBT", x=mat$SID, ignore.case=F, value=T, fixed=T)))
size_lc=length(unique(grep(pattern="LC", x=mat$SID, ignore.case=F, value=T, fixed=T)))
size_gbm=length(unique(mat$SID)) - size_mbt - size_lc

mat$Grp<-'Control'
mat$Panel<-paste('GBM:', size_gbm)
mat$Panel[ grep(pattern="MBT", x=mat$SID, ignore.case=F, value=F, fixed=T) ]<-paste('MBT:', size_mbt)
mat$Panel[ grep(pattern="LC", x=mat$SID, ignore.case=F, value=F, fixed=T) ]<-paste('LC:', size_lc)

sid_MBT<-mat[ mat$SID == sid, ]
sid_MBT$Grp<-sid
sid_MBT$Panel<-paste('MBT:',size_mbt)
sid_LC<-mat[ mat$SID == sid, ]
sid_LC$Grp<-sid
sid_LC$Panel<-paste('LC:',size_lc)
mat$Grp[ mat$SID == sid] <- sid
mat$Panel[ mat$SID == sid]<-paste('GBM:',size_gbm)
mat<-rbind(mat, sid_MBT)
mat<-rbind(mat, sid_LC)

library(ggplot2)
format<-substr(outName, nchar(outName)-2, nchar(outName))
if (format == 'png') {
	png(outName, width=2100, height=1200)
} else {
	pdf(outName, width=21, height=12)
}
p<-ggplot(mat)
p<-p+geom_boxplot(aes(x=Gene,y=RPKM,color=Grp))+theme(axis.text.x=element_text(angle=90,hjust=1))+ggtitle(sid)+scale_y_log10()
p+facet_grid( Panel ~ .)
dev.off()
