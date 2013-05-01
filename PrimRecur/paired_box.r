paired_box <- function(
  inDirName,
  listN,
  geneNL,
  graphicsFormat='png'
)
{
  
  if (graphicsFormat == 'png') {
    png(sprintf("%s/box/paired_box_%s.png", inDirName,listN))
  } else if (graphicsFormat== 'pdf') {
    pdf(sprintf("%s/box/paired_box_%s.pdf", inDirName,listN))
  }
  
  par(mfrow=c(2,1))

  df = read.table(sprintf('%s/df.txt',inDirName),header=TRUE)
  
  for (dType in c('CNA','Expr')){
    
    if (dType == 'CNA'){
      lab = 'CN (log2)'
    }else{
      lab = 'Expr (z-score)'
    }
    
    df_ft = df[df$dType==dType & df$geneN %in% geneNL,]
    
    df_ft$geneN <- factor(df_ft$geneN[drop=TRUE],geneNL)
    
    df_ft_ch = df_ft$val_r - df_ft$val_p
    
    xSta=floor(min(df_ft_ch))
    xEnd=ceiling(max(df_ft_ch))
    
    xSta=max(abs(xSta),abs(xEnd)) * -1
    xEnd=max(abs(xSta),abs(xEnd))
    
    n = length(df_ft_ch)/length(geneNL)
    
    boxplot(df_ft_ch ~ df_ft$geneN, ylim=c(xSta,xEnd), ylab=sprintf('Change in %s',lab), axes=F, cex.axis=0.6, cex=0.5, main=sprintf('%s, %s gene P->R change (n=%d)',dType,listN,n))
    stripchart(df_ft_ch ~ df_ft$geneN, vertical=T, add=T, pch=1, ylim=c(xSta,xEnd), cex=0.5)
    abline(h=0,pch=22,lty=2)
    
    labelL <- geneNL
    
    for (geneN in geneNL){
      df_ft2 <- df_ft[df_ft$geneN==geneN,]
      pval_t <- t.test(df_ft2$val_r-df_ft2$val_p)['p.value']
      pval_r <- wilcox.test(df_ft2$val_r-df_ft2$val_p)['p.value']
      labelL[labelL==geneN] <- sprintf('%s\nt=%.1E\nr=%.1E',geneN,pval_t,pval_r)
    }
    
    axis(1,axTicks(1),labels=labelL,cex.axis=0.6)
    axis(2,axTicks(2),cex.axis=0.6)
        
  }
  
  if (graphicsFormat=='png' || graphicsFormat=='pdf'){    
    dev.off()
  }
}

inDirName = '/EQL1/NSL/PrimRecur/paired'
geneNLL <- list(Amp=c('EGFR','CDK4','CDK6','PDGFRA','MET','MDM2','MDM4'), Del=c('CDKN2A','CDKN2B','CDKN2C','PTEN','RB1','NF1','QKI'))

# for debug: listN='Amp'; geneNL=geneNLL[[listN]]; fmt=''

for (listN in c('Amp','Del'))
  for (fmt in c('png','pdf','')) paired_box(inDirName,listN=listN,geneNL=geneNLL[[listN]],graphicsFormat=fmt)
