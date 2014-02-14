args <- commandArgs(TRUE)

inFileName= args[1]
outDirName = args[2]
sId = args[3]

library("DNAcopy")

inFile = read.delim(inFileName)

CNA.object <- CNA(cbind(inFile$value),inFile$chrom, inFile$loc.start, data.type="binary",sampleid=sId)
segment.CNA.object <- segment(CNA.object,alpha=0.001, nperm=5000, verbose=1)
segment.output=segment.CNA.object$output

outFile = sprintf('%s/%s.dbaf.seg', outDirName,sId)

write.table(segment.output, file = outFile, row.names=F, col.names=T, quote=F, sep="\t")
