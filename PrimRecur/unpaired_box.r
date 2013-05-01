unpaired_box <- function(
  inDirName,
  dbT,
  listN,
  geneNL,
  graphicsFormat='png'
)
{
  
  if (graphicsFormat == 'png') {
    png(sprintf("%s/box/unpaired_box_%s.png", inDirName,listN))
  } else if (graphicsFormat== 'pdf') {
    pdf(sprintf("%s/box/unpaired_box_%s.pdf", inDirName,listN))
  }
  
  par(mfrow=c(2,1))
  
  df = read.table(sprintf('%s/df_unpaired.txt',inDirName),header=TRUE)
  
  for (dType in c('CNA','Expr')){
    
    if (dType == 'CNA'){
      lab = 'CN (log2)'
    }else{
      lab = 'Expr (z-score)'
    }
    
    df_ft = df[df$dbT==dbT & df$dType==dType & df$geneN %in% geneNL,]
    
    df_ft$geneN <- factor(df_ft$geneN[drop=TRUE],geneNL)
    
    xSta=floor(min(df_ft$val))
    xEnd=ceiling(max(df_ft$val))
    
    xSta=max(abs(xSta),abs(xEnd)) * -1
    xEnd=max(abs(xSta),abs(xEnd))
        
    df_ftP = df_ft[df_ft$PR=='P',]
    df_ftR = df_ft[df_ft$PR=='R',]
    
    boxplot(df_ftP$val ~ df_ftP$geneN, ylim=c(xSta,xEnd), ylab=sprintf('Change in %s',lab), axes=F, cex.axis=0.6, cex=0.5)
    stripchart(df_ftR$val ~ df_ftR$geneN, vertical=T, add=T, pch=1, cex=0.5, ylim=c(xSta,xEnd), method='jitter', col='red')
    abline(h=0,pch=22,lty=2)
    title(sprintf('%s, %s, %s gene P->R change (n=%d,%d)',dbT,dType,listN,nrow(df_ftP)/length(geneNL),nrow(df_ftR)/length(geneNL)))
    
    labelL <- geneNL
    
    for (geneN in geneNL){
      df_ftP2 <- df_ftP[df_ftP$geneN==geneN,]
      df_ftR2 <- df_ftR[df_ftR$geneN==geneN,]
      pval_t <- t.test(df_ftP2$val,df_ftR2$val)['p.value']
      pval_r <- wilcox.test(df_ftP2$val,df_ftR2$val)['p.value']
      pval_k <- ks.test(df_ftP2$val,df_ftR2$val)['p.value']
      labelL[labelL==geneN] <- sprintf('%s\nt=%.1E\nr=%.1E\nk=%.1E',geneN,pval_t,pval_r,pval_k)
    }
    
    axis(1,axTicks(1),labels=labelL,cex.axis=0.6,las=2)
    axis(2,axTicks(2),cex.axis=0.6)
    
  }
  
  if (graphicsFormat=='png' || graphicsFormat=='pdf'){    
    dev.off()
  }
}

inDirName = '/EQL1/NSL/PrimRecur/unpaired'
geneNLL <- list(Amp=c('EGFR','CDK4','CDK6','PDGFRA','MET','MDM2','MDM4'), Del=c('CDKN2A','CDKN2B','CDKN2C','PTEN','RB1','NF1','QKI'))

# for debug: listN='Amp'; geneNL=geneNLL[[listN]]; fmt=''

for (dbT in c('TCGA-GBM','IRCR-GBM'))
  for (listN in c('Amp','Del'))
    for (fmt in c('png','pdf','')) unpaired_box(inDirName,dbT=dbT,listN=listN,geneNL=geneNLL[[listN]],graphicsFormat=fmt)
