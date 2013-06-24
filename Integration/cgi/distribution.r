distribution <- function(

inFile, # input dst file
graphicsFormat='png',
nBins = 10

)
{

df <- read.table(inFile,header=T)

dataName <- 'TCGA_GBM'
label <- strsplit(as.character(df$label[1]),' ')[[1]]
featName <- sprintf('%s %s',label[1],label[2])
#altType <- strsplit(as.character(df$label[1]),' ')[[1]][2]
valueL <- df$value[order(df$value)]

n <- length(valueL)

xMax <- max(valueL)
xMin <- min(valueL)

xSta <- xMin - (xMax-xMin) * 0.1
xEnd <- xMax + (xMax-xMin) * 0.1

interval <- (xEnd-xSta)/as.numeric(nBins)
xBreaks <- seq(xSta,xEnd,interval)

if (graphicsFormat == 'png') {
	png(sprintf("/var/www/html/survival/distribution.png"))
} else {
	png(sprintf("/var/www/html/survival/distribution.png"))
}

par(mfrow=c(2,2))

hist(valueL, breaks=xBreaks, xlim=c(xSta,xEnd), xlab=featName, ylab='Count', main=sprintf('%s (n=%d)', dataName, n))
plot(ecdf(valueL), xlim=c(xSta,xEnd), xlab=featName, ylab='Cumulative Fraction', main=sprintf('%s (n=%d)', dataName, n))

boxplot(valueL, ylab=featName, main=sprintf('%s (n=%d)', dataName, n))

plot(seq(1,length(valueL)),valueL, ylab=featName, xlab='rank', main=sprintf('%s (n=%d)', dataName, n))

dev.off()

}

args <- commandArgs(trailingOnly = T)

inFile = '/var/www/html/survival/survival.mvc'
distribution(args[1])
#distribution('/var/www/html/survival/survival.mvc')
