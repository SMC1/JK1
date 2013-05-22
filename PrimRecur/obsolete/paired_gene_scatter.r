paired_scatter <- function(
  inDirName,
  geneN='EGFR',
  graphicsFormat='png'
)
{
  
  if (graphicsFormat == 'png') {
    png(sprintf("%s/scatter/paired_scatter_%s.png", inDirName,geneN))
  } else if (graphicsFormat== 'pdf') {
    pdf(sprintf("%s/scatter/paired_scatter_%s.pdf", inDirName,geneN))
  }
  
  par(mfrow=c(2,2))
  
  for (dType in c('CNA','RPKM')){
    
    df = read.table(sprintf('%s/df_sel2.txt',inDirName),header=TRUE)
    df_ft = df[df$dType==dType & df$geneN==geneN,]
    
#     if (dType=='RPKM') xSta=0 
#     else xSta=max(abs(xSta),abs(xEnd)) * -1
    
    radius=max(abs(floor(min(df_ft$val_p,df_ft$val_r))), abs(ceiling(max(df_ft$val_p,df_ft$val_r))))
    
    xSta=radius * -1
    xEnd=radius
    
    if (dType == 'CNA'){
      lab = 'CN (log2)'
    }else if (dType == 'RPKM'){
      lab = 'log2(RPKM+1)'
    }else{
      lab = 'Expr (z-score)'
    }
    
    plot(df_ft$val_p, df_ft$val_r, xlim=c(xSta,xEnd), ylim=c(xSta,xEnd), xlab=sprintf('Prim, %s',lab), ylab=sprintf('Recur, %s',lab))
    par(new=T)
    plot(c(xSta,xEnd),c(xSta,xEnd), type='l',pch=22,lty=2, xlim=c(xSta,xEnd), ylim=c(xSta,xEnd),xlab='',ylab='')
    title(main=sprintf('%s %s (n=%d)',geneN,dType,nrow(df_ft)),cex.main=0.9)
    
    pval_t <- t.test(df_ft$val_r-df_ft$val_p)['p.value']
    pval_r <- wilcox.test(df_ft$val_r-df_ft$val_p)['p.value']
    
    boxplot(df_ft$val_r-df_ft$val_p, ylim=c(xSta,xEnd), main=sprintf('P(t,rs)=%.1E,%.1E',pval_t,pval_r), ylab=sprintf('Change in %s',lab))    
    stripchart(df_ft$val_r-df_ft$val_p, add=T, vertical=T, ylim=c(xSta,xEnd))
    abline(h=0,pch=22,lty=2)
  }
    
  if (graphicsFormat=='png' || graphicsFormat=='pdf'){    
    dev.off()
  }
}

inDirName = '/EQL1/PrimRecur/paired'

for (geneN in c('EGFR','CDK4','CDK6','PDGFRA','MET','MDM2','MDM4','CDKN2A','CDKN2B','CDKN2C','PTEN','RB1','NF1','QKI')){
  for (fmt in c('png','pdf','')) paired_scatter(inDirName,geneN,fmt)
}
