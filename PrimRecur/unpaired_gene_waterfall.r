unpaired_waterfall <- function(
  inDirName,
  dbT,
  listN,
  dType,
  geneNL,
  graphicsFormat='png'
)
{
  df = read.table(sprintf('%s/df_unpaired2.txt',inDirName),header=TRUE)
  
  df_ft = df[df$dbT==dbT & df$dType==dType & df$geneN %in% geneNL,]
  
  if (nrow(df_ft[df_ft$PR=='R',])==0) return (0)
  
  if (graphicsFormat == 'png') {
    png(sprintf("%s/waterfall/unpaired_waterfall_%s_%s_%s.png", inDirName,dbT,listN,dType))
  } else if (graphicsFormat== 'pdf') {
    pdf(sprintf("%s/waterfall/unpaired_waterfall_%s_%s_%s.pdf", inDirName,dbT,listN,dType))
  }
  
  par(mfrow=c(1,1))
  par(oma=c(1,1,1,0), mar=c(4,3,2,2),mgp=c(2,1,0))

  if (dType == 'CNA'){
    lab = 'CN (log2)'
  }else if (dType == 'RPKM'){
    lab = 'log2(RPKM+1)'
  }else{
    lab = 'Expr (z-score)'
  }
  
  df_ft$geneN <- factor(df_ft$geneN[drop=TRUE],geneNL)
  
  radius=max(abs(floor(min(df_ft$val))), abs(ceiling(max(df_ft$val))))
  
  if (dType=='RPKM') ySta=0
  else ySta = -radius
  yEnd = radius
  
  xSta=0.5; xEnd=length(geneNL)+0.5
  
  index=1
  labelL <- geneNL
  
  for (geneN in geneNL){
    
    df_ftP = df_ft[df_ft$geneN==geneN & df_ft$PR=='P',]
    nP=nrow(df_ftP)
    
    df_ftR = df_ft[df_ft$geneN==geneN & df_ft$PR=='R',]
    nR=nrow(df_ftR)
    
    if (index>1) par(new=T)
    plot(seq(1,nP)/nP*0.8+index-0.4,df_ftP$val[order(df_ftP$val)],xaxs='i', xaxt='n', yaxt='n', xlab='', ylab='', xlim=c(xSta,xEnd), ylim=c(ySta,yEnd), cex.axis=0.6, pch=20, cex=0.4)
    par(new=T)
    plot(seq(1,nR)/nR*0.8+index-0.4,df_ftR$val[order(df_ftR$val)],xaxs='i', axes=F, ann=F, xlim=c(xSta,xEnd), ylim=c(ySta,yEnd), pch=1, cex=0.6, col='red')
    
    pval_t <- t.test(df_ftP$val,df_ftR$val)['p.value']
    pval_r <- wilcox.test(df_ftP$val,df_ftR$val)['p.value']
    pval_k <- ks.test(df_ftP$val,df_ftR$val)['p.value']
    labelL[index] <- sprintf('%s\nt=%.1E\nr=%.1E\nk=%.1E',geneN,pval_t,pval_r,pval_k)
    
    if (dType=='RPKM') abline(v=index-0.5,pch=22,lty=2)
    
    index = index+1
  }
  
  if (dType=='RPKM') abline(v=index-0.5,pch=22,lty=2)
  else abline(h=0,pch=22,lty=2)
  
  title(sprintf('%s, %s, %s gene P->R change (n=%d,%d)',dbT,dType,listN,nP,nR), ylab=sprintf('%s',lab),cex.lab=0.7,cex.main=0.9)
  
  axis(1,seq(1,length(geneNL)),labels=labelL,cex.axis=0.6,las=2)
  axis(2,axTicks(2),cex.axis=0.6)
  
  if (graphicsFormat=='png' || graphicsFormat=='pdf'){    
    dev.off()
  }
}

inDirName = '/EQL1/PrimRecur/unpaired'
geneNLL <- list(Amp=c('EGFR','CDK4','CDK6','PDGFRA','MET','MDM2','MDM4'), Del=c('CDKN2A','CDKN2B','CDKN2C','PTEN','RB1','NF1','QKI'))

# for debug: dbT='TCGA-GBM';listN='Amp'; geneNL=geneNLL[[listN]]; fmt=''; dType='RPKM';geneN='EGFR'

for (dbT in c('TCGA-GBM','IRCR-GBM'))
  for (listN in c('Amp','Del'))
    for (dType in c('CNA','Expr','RPKM'))
      for (fmt in c('png','pdf','')) unpaired_waterfall(inDirName,dbT=dbT,listN=listN,dType,geneNL=geneNLL[[listN]],graphicsFormat=fmt)
