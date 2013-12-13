waterfall_IOD <- function(
  inFile,
  outFile
)
{
  dataT = read.delim(inFile)
  
  dataT = dataT[order(dataT[,2],decreasing=F),]
  
  pdf(outFile)
  barplot(dataT[,2], space=0,col="white", names.arg=dataT[,1], cex.names=0.7, las=3, ylim=c(-100,100),ylab="% IOD Chnage")
  dev.off()
  
}

#waterfall_IOD('EGFR_IOD_change.txt',"IHC_IOD_waterfall.pdf")
#waterfall_IOD('/EQL1/PrimRecur/paired/EGFR_IHC.txt',"/EQL1/PrimRecur/paired/EGFR_IHC.pdf")
waterfall_IOD('/EQL1/PrimRecur/paired/EGFR_IHC_xeno.txt',"/EQL1/PrimRecur/paired/EGFR_IHC_xeno.pdf")