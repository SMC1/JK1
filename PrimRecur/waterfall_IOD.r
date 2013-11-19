waterfall_IOD <- function(
  inFile= 'EGFR_IOD_change.txt'
)
{
  dataT = read.delim(inFile)
  
  dataT = dataT[order(dataT[,2],decreasing=F),]
  
  pdf("IHC_IOD_waterfall.pdf")
  barplot(dataT[,2], space=0.6,col="black", names.arg=dataT[,1], cex.names=0.7, las=3, ylim=c(-40,10),ylab="% IOD Chnage")
  dev.off()
  
}
waterfall_IOD()