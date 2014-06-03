distribution <- function(

dirN,
sampN,
graphicsFormat='png'

)
{

df = read.table(sprintf('%s/%s.depth',dirN,sampN),header=F)

cdf = cumsum(df$V2) / sum(df$V2)

if (graphicsFormat == 'png') {
  png(sprintf("%s/%s.png",dirN,sampN))
} else {
  png(sprintf("%s/%s.pdf",dirN,sampN))
}

plot(0:(length(cdf)-1),cdf,xlim=c(0,150),xaxs='i',yaxs='i',pch=20,main=sprintf('%s (Exome: %d Mb)', sampN, floor(sum(df$V2)/1000000)),xlab='depth',ylab='cumulative fraction')

dev.off()
}

args <- commandArgs(trailingOnly = T)
distribution(args[1],args[2])

#inFile = '/EQL1/NSL/Exome/mutation/671T_Br1_WXS_trueSeq.depth'
#inFile = '/EQL1/NSL/Exome/mutation/GBM10_042TD_WXS.depth'
#distribution('/EQL1/NSL/Exome/mutation','GBM10_042TD_WXS')
