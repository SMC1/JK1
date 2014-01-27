dnaCopy <- function(
	inFileName,
	outDirName

)

{
inFile = read.delim(inFileName)

library("DNAcopy")

sId = inFile[1,1]
 
CNA.object <- CNA(cbind(inFile$value),inFile$chrom, inFile$loc.start, data.type="logratio",sampleid=sId)

smoothed.CNA.object <- smooth.CNA(CNA.object)

segment.smoothed.CNA.object <- segment(smoothed.CNA.object, verbose=1)

segment.output=segment.smoothed.CNA.object$output
  
outFile = sprintf('%s/%s.copyNumber.seg', outDirName,sId)
  
write.table(segment.output, file = outFile, row.names=F, col.names=T, quote=F, sep="\t")
}

args <- commandArgs(TRUE)

dnaCopy(args[1],args[2])
