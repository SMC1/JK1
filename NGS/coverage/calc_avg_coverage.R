# Coverage calculation

coverageCalc <- function(
  inDirName,
  sId,
  total_base
  ){
  

inFileName = sprintf('%s/%s.recal.depth_hash.txt',inDirName,sId)
inFile = read.table(inFileName,header=F,sep=" ")

inFile$V2[1] <- inFile$V2[1]+ (total_base-sum(inFile$V2))

xrange <- 250
pdf(sprintf("%s/%s.recal.coverage.pdf",inDirName,sId))
barplot(rev(cumsum(rev(inFile$V2[-1])))[1:xrange]/total_base,xlab='coverage',ylab='fraction covered', space=0, xlim=c(1,xrange), ylim=c(0,1),col='white')
axis(1, at=seq(0, xrange, 50), labels = seq(0, xrange, 50))

coverage = sum(inFile$V1*inFile$V2)/total_base
title(sprintf('%s: average coverage = %.1f',sId, coverage))
dev.off()

outFileName <- sprintf('%s/%s.recal.avg_coverage.txt', inDirName,sId)
outFile <- file(outFileName,'wt')
writeLines(sprintf('%s\t%s',sId, coverage),outFile)
close(outFile)
}

inDirName = '/EQL1/NSL/WXS/coverage/average_coverage'
sIdL = unique(regmatches(dir(inDirName),regexpr(".*_[TS]S",dir(inDirName))))
total_base <- 61598409 #2216990 #112815 #61598409

for (sId in sIdL) {
  tryCatch({
  coverageCalc(inDirName,sId,total_base)}, error=function(e) sId, finally=NULL)
}

