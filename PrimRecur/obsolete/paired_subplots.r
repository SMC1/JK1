distPaired <- function(
  inDirName,
  geneN,
  graphicsFormat=''
)
{
  
  if (graphicsFormat == 'png') {
    png(sprintf("%s/%s_2dist.png", inDirName,geneN))
  } else if (graphicsFormat== 'pdf') {
    pdf(sprintf("%s/%s_2dist.pdf", inDirName,geneN))
  }
  
  par(mfrow=c(2,2))
  
  dbN='IRCR-GBM'
  
  for (dType in c('CNA','Expr')){
    
    lines <- readLines(sprintf('%s/%s_%s_%s_paired.dst2',inDirName,geneN,dType,dbN))
    
    tokL <- strsplit(lines[1], '\t')[[1]]
    g1 <- tokL[1]
    n1 <- tokL[2]
    vL1 <- sapply(strsplit(lines[2], ',')[[1]], as.double)
    
    analysisName <-sprintf('%s_%s_%s',geneN,dType,dbN)
    
    xSta=floor(min(vL1))
    xEnd=ceiling(max(vL1))
    
    xSta=max(abs(xSta),abs(xEnd)) * -1
    xEnd=max(abs(xSta),abs(xEnd))
    
    if (dType=='CNA'){
      xLab='Copy number (log2)'
    }else if (dType=='Expr'){
      xLab='Expr (z score)'
    }else{
      xLab=''
    }
    
    plot(ecdf(vL1), xlim=c(xSta,xEnd),xlab=xLab,ylab='Cumulative Fraction', main=sprintf('%s (n=%s)',analysisName,n1), col='black')
    par(new=T)
    plot(c(0,0),c(0,1), type='l',pch=22,lty=2,xlim=c(xSta,xEnd),xlab=xLab,ylab='Cumulative Fraction', main=sprintf('%s (n=%s)',analysisName,n1), col='black')
    
    pval <- t.test(vL1)['p.value']
    
    if (pval<0.01){
      text(x=xSta+0.5,y=0.9,sprintf('P=%.1E',pval))
    }else{
      text(x=xSta+0.5,y=0.9,sprintf('P=%.2f',pval))
    }
  }
  
  if (graphicsFormat=='png' || graphicsFormat=='pdf'){
    dev.off()
  }
  
}


inDirName = '/EQL1/NSL/PrimRecur/paired'
for (geneN in c('EGFR','CDK4','CDK6','PDGFRA','MET','MDM2','MDM4','CDKN2A','CDKN2B','CDKN2C','PTEN','RB1','NF1','QKI')){
  for (fmt in c('png','pdf','')) distPaired(inDirName,geneN,fmt)
}