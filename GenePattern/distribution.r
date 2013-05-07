distribution <- function(

inFile, # input dst file
graphicsFormat='pdf',
nBins = 10

)
{

lines <- readLines(inFile)

tokL <- strsplit(lines[2], '\t')[[1]]

dataName <- lines[1]
featName <- tokL[1]
valueL <- sapply(strsplit(lines[3], '\t')[[1]], as.double)
n <- length(valueL)

xMax <- max(valueL)
xMin <- min(valueL)

if (length(tokL) > 1) {
	xSta <- as.double(tokL[2]) * 0.9
	xEnd <- as.double(tokL[3]) * 1.1
} else {
	xSta <- xMin - (xMax-xMin) * 0.1
	xEnd <- xMax + (xMax-xMin) * 0.1
}

interval <- (xEnd-xSta)/as.numeric(nBins)
xBreaks <- seq(xSta,xEnd,interval)

if (graphicsFormat == 'png') {
	png(sprintf("%s_%s_dist.png", dataName,featName))
} else {
	pdf(sprintf("%s_%s_dist.pdf", dataName,featName))
}

par(mfrow=c(2,2))

hist(valueL, breaks=xBreaks, xlim=c(xSta,xEnd), xlab=featName, ylab='Count', main=sprintf('%s (n=%d)', dataName, n))
plot(ecdf(valueL), xlim=c(xSta,xEnd), xlab=featName, ylab='Cumulative Fraction', main=sprintf('%s (n=%d)', dataName, n))

boxplot(valueL, ylab=featName, main=sprintf('%s (n=%d)', dataName, n))

plot(seq(1,length(valueL)),valueL, ylab=featName, xlab='rank', main=sprintf('%s (n=%d)', dataName, n))

dev.off()

}

#distribution('TCGA_GBM_miRNA_hsa-miR-9.dst')
