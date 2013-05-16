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
  
  for (dType in c('CNA','Expr','RPKM')){
    
    df = read.table(sprintf('%s/df_sel2.txt',inDirName),header=TRUE)
    df_ft = df[df$dType==dType & df$geneN==geneN,]
    
    radius=max(abs(floor(min(df_ft$val_p,df_ft$val_r))), abs(ceiling(max(df_ft$val_p,df_ft$val_r))))
    
    if (dType=='RPKM') xSta = 0 
    else xSta = -radius
    xEnd = radius
        
    if (dType == 'CNA'){
      lab = 'CN (log2)'
    }else if (dType == 'RPKM'){
      lab = 'log2(RPKM+1)'
    }else{
      lab = 'Expr (z-score)'
    }
    
    pval_t <- t.test(df_ft$val_r-df_ft$val_p)['p.value']
    pval_r <- wilcox.test(df_ft$val_r-df_ft$val_p)['p.value']
    
    plot(df_ft$val_p, df_ft$val_r, xlim=c(xSta,xEnd), ylim=c(xSta,xEnd), xlab=sprintf('Prim, %s',lab), ylab=sprintf('Recur, %s',lab),cex.lab=0.9,cex.axis=0.9)
    par(new=T)
    plot(c(xSta,xEnd),c(xSta,xEnd), type='l',pch=22,lty=2, xlim=c(xSta,xEnd), ylim=c(xSta,xEnd), axes=F, ann=F)
    title(main=sprintf('%s %s (n=%d)',geneN,dType,nrow(df_ft)),cex.main=0.95)
    
    text(xEnd,xSta+(xEnd-xSta)*0.3,sprintf('m=%.2f',mean(df_ft$val_r-df_ft$val_p)),cex=0.9, adj=c(1,1))
    text(xEnd,xSta+(xEnd-xSta)*0.2,sprintf('p_t=%.2E',pval_t),cex=0.9, adj=c(1,1))
    text(xEnd,xSta+(xEnd-xSta)*0.1,sprintf('p_r=%.2E',pval_r),cex=0.9, adj=c(1,1))
  }
    
  if (graphicsFormat=='png' || graphicsFormat=='pdf'){    
    dev.off()
  }
}

inDirName = '/EQL1/PrimRecur/paired'

for (geneN in c('EGFR','CDK4','CDK6','PDGFRA','MET','MDM2','MDM4','CDKN2A','CDKN2B','CDKN2C','PTEN','RB1','NF1','QKI')){
  for (fmt in c('png','pdf','')) paired_scatter(inDirName,geneN,fmt)
}
