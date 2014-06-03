setwd("/data1/IRCR/CGH")

inFile = read.delim("CGH_NSL_probe.txt",skip=1)

names(inFile)

for (i in 8:109) {

  sId = names(inFile)[i]
#  pId = regmatches(sId,regexpr("[0-9]{3}",sId))
  sId = gsub("X","",sId)
  
CNA.object <- CNA(cbind(inFile[,i]),inFile$ChrName, inFile$Start, data.type="logratio",sampleid=sId)

smoothed.CNA.object <- smooth.CNA(CNA.object)

segment.smoothed.CNA.object <- segment(smoothed.CNA.object, verbose=1)

  segment.output=segment.smoothed.CNA.object$output
  
  outFile = sprintf('/data1/IRCR/CGH/seg/%s_%s_copyNumber.seg', pId,sId)
  
  write.table(segment.output, file = outFile, row.names=F, col.names=T, quote=F, sep="\t")
}
