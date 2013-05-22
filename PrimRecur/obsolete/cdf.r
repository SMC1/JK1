drawCdf <- function(
  
  inFileName,
  graphicsFormat=''
)
{
  
  lines <- readLines(inFileName)
  
  tokL <- strsplit(lines[1], '\t')[[1]]
  g1 <- tokL[1]
  n1 <- tokL[2]
  vL1 <- sapply(strsplit(lines[2], ',')[[1]], as.double)
  
  tokL <- strsplit(lines[4], '\t')[[1]]
  g2 <- tokL[1]
  n2 <- tokL[2]
  vL2 <- sapply(strsplit(lines[5], ',')[[1]], as.double)
  
  pathPrefix <- strsplit(inFileName,'.dst2')[[1]][1]
  analysisName <-strsplit(pathPrefix,'/')[[1]]
  analysisName <-analysisName[length(analysisName)]
  
  if (graphicsFormat == 'png') {
    png(sprintf("%s_cdf.png", pathPrefix))
  } else if (graphicsFormat== 'pdf') {
    pdf(sprintf("%s_cdf.pdf", pathPrefix))
  }
  
  xSta=floor(min(vL1,vL2))
  xEnd=ceiling(max(vL1,vL2))
  
  if (length(grep('CNA',inFileName))>0){
    xLab='copy number (log2)'
  }else if (length(grep('Expr',inFileName))>0){
    xLab='expr (z score)'
  }else{
    xLab=''
  }
  
  plot(ecdf(vL1), xlim=c(xSta,xEnd),xlab=xLab,ylab='Cumulative Fraction', main=sprintf('%s (n=%s,%s)',analysisName,n1,n2), col='black')
  par(new=T)
  plot(ecdf(vL2), xlim=c(xSta,xEnd),xlab='',ylab='',main='',col='red')
  
  pval <- ks.test(vL1,vL2)['p.value']
  
  if (pval<0.01){
    text(x=xSta+0.5,y=0.9,sprintf('P=%.1E',pval))
  }else{
    text(x=xSta+0.5,y=0.9,sprintf('P=%.2f',pval))
  }
  if (graphicsFormat=='png' || graphicsFormat=='pdf'){
    dev.off()
  }
  
}


inFileName = '/EQL1/NSL/PrimRecur/unpaired/EGFR_CNA_IRCR-GBM_paired.dst2'

for (fmt in c('png','pdf','')) drawCdf(inFileName,fmt)