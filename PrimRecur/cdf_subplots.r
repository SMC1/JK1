drawCdf <- function(
  inDirName,
  geneN,
  graphicsFormat=''
)
{
  
  if (graphicsFormat == 'png') {
    png(sprintf("%s/%s_4cdf.png", inDirName,geneN))
  } else if (graphicsFormat== 'pdf') {
    pdf(sprintf("%s/%s_4cdf.pdf", inDirName,geneN))
  }
  
  par(mfrow=c(2,2))
  
  for (dbN in c('IRCR-GBM','TCGA-GBM')){
    
    for (dType in c('CNA','Expr')){
      
      lines <- readLines(sprintf('%s/%s_%s_%s.dst2',inDirName,geneN,dType,dbN))
      
      tokL <- strsplit(lines[1], '\t')[[1]]
      g1 <- tokL[1]
      n1 <- tokL[2]
      vL1 <- sapply(strsplit(lines[2], ',')[[1]], as.double)
      
      tokL <- strsplit(lines[4], '\t')[[1]]
      g2 <- tokL[1]
      n2 <- tokL[2]
      vL2 <- sapply(strsplit(lines[5], ',')[[1]], as.double)
      
      analysisName <-sprintf('%s_%s_%s',geneN,dType,dbN)
      
      xSta=floor(min(vL1,vL2))
      xEnd=ceiling(max(vL1,vL2))
      
      if (dType=='CNA'){
        xLab='copy number (log2)'
      }else if (dType=='Expr'){
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
    }
  }
  
  if (graphicsFormat=='png' || graphicsFormat=='pdf'){
    dev.off()
  }
  
}


inDirName = '/EQL1/NSL/PrimRecur/unpaired'
for (geneN in c('EGFR','CDK4','CDK6','PDGFRA','MET','MDM2','MDM4','CDKN2A','CDKN2B','CDKN2C','PTEN','RB1','NF1','QKI')){
  for (fmt in c('png','pdf','')) drawCdf(inDirName,geneN,fmt)
}