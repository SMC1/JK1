args<-commandArgs(trailingOnly=T) ## 1:inputfile, 2:outdir
inFileN<-args[1]
outDir<-args[2]

require(DNAcopy)

inFile<- read.delim(inFileN, skip=1)
for (i in 8:(ncol(inFile)-1))
{
	sId = colnames(inFile)[i]
	outFileN = sprintf('%s/%s.seg', outDir, sId)
	CNA.object <- CNA(cbind(inFile[,i]),inFile$ChrName, inFile$Start, data.type="logratio",sampleid=sId)
	smoothed.CNA.object <- smooth.CNA(CNA.object)
	segment.smoothed.CNA.object <- segment(smoothed.CNA.object, verbose=1)
	segment.output=segment.smoothed.CNA.object$output
	write.table(segment.output, file=outFileN, row.names=F, col.names=T, quote=F, sep="\t")
}
