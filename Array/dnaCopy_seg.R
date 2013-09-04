inFile = read.delim("/EQL1/NSL/CGH/NSL_GBM_CGH_109_probe.txt",skip=1)

library("DNAcopy")

for (i in 8:ncol(inFile)) {

  sId = names(inFile)[i]
  #pId = regmatches(sId,regexpr("[0-9]{3}",sId))
  sId = gsub("X","",sId)
 
CNA.object <- CNA(cbind(inFile[,i]),inFile$ChrName, inFile$Start, data.type="logratio",sampleid=sId)

smoothed.CNA.object <- smooth.CNA(CNA.object)

segment.smoothed.CNA.object <- segment(smoothed.CNA.object, verbose=1)

  segment.output=segment.smoothed.CNA.object$output
  
  outFile = sprintf('/EQL1/NSL/CGH/seg/seg/%s_copyNumber.seg', sId)
  
  write.table(segment.output, file = outFile, row.names=F, col.names=T, quote=F, sep="\t")
}
