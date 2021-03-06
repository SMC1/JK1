paired_scatter <- function(
  inDirName,
  geneN='EGFR',
  graphicsFormat='png'
)
{
  
  if (graphicsFormat == 'png') {
    png(sprintf("%s/bubble/paired_bubble_%s.png", inDirName,geneN))
  } else if (graphicsFormat== 'pdf') {
    pdf(sprintf("%s/bubble/paired_bubble_%s.pdf", inDirName,geneN))
  }
  
  plot.new()
  par(mfrow=c(2,2))
  par(oma=c(1,1,1,1))
  par(mar=c(2,2,2,1))  
  
  for (dType in c('CNA','Expr','RPKM')){
    
    if (dType=='RPKM') {
      xSta = -1
      xEnd = 13
    } else if (dType=='Expr') {
      xSta = 4
      xEnd = 18
    } else {
      xSta = -7
      xEnd = 7
    }
    
    if (dType == 'CNA'){
      lab = 'CN (log2)'
    }else if (dType == 'RPKM'){
      lab = 'log2(RPKM+1)'
    }else{
      lab = 'Expr (z-score)'
    }
    
    df = read.table(sprintf('%s/df_sel2.txt',inDirName),header=TRUE)
    df_ft = df[df$dType==dType & df$geneN==geneN,]
    
    pval_t <- t.test(df_ft$val_r-df_ft$val_p)['p.value']
    pval_r <- wilcox.test(df_ft$val_r-df_ft$val_p)['p.value']
    
    df_ft$delta = df_ft$val_r-df_ft$val_p
    df_ft$color = as.character(df_ft$delta)
    df_ft$color[df_ft$delta >= 0] = 'red'
    df_ft$color[df_ft$delta <= 0] = 'blue'
    
    df_ft = df_ft[order(-abs(df_ft$delta)),]
    
    dmean = mean(df_ft$delta)*20
    dmean_scale = round(min(abs(dmean),50) * sign(dmean) + 51)
    plot(c(),c(), xlim=c(xSta,xEnd), ylim=c(xSta,xEnd), axes=F, ann=F, xaxt='n',yaxt='n', xaxs='i',yaxs='i')
    par(new=T)
    rect(xSta,xSta,xEnd,xEnd,border='black',col=bluered(101)[dmean_scale],xaxt='n',yaxt='n', xaxs='i',yaxs='i')
    par(new=T)
    symbols(x=df_ft$val_p, y=df_ft$val_r, circles=abs(df_ft$delta)/5, inches=F, bg=df_ft$color, fg='black', xlim=c(xSta,xEnd), ylim=c(xSta,xEnd), xlab=sprintf('Prim, %s',lab), ylab=sprintf('Recur, %s',lab), xaxs='i',yaxs='i')
    par(new=T)
    plot(c(xSta,xEnd),c(xSta,xEnd), type='l',pch=22,lty=2, xlim=c(xSta,xEnd), ylim=c(xSta,xEnd), axes=F, ann=F,  xaxs='i',yaxs='i')
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

for (geneN in c('EGFR','CDK4','CDK6','PDGFRA','MET','MDM2','MDM4','CDKN2A','CDKN2B','CDKN2C','PTEN','RB1','NF1','QKI','FGFR1','FGFR2','FGFR3','IGF1R','IDH1','IDH2','TP53')){
  for (fmt in c('png','pdf','')) paired_scatter(inDirName,geneN,fmt)
}

#paired_scatter(inDirName,'MET','')