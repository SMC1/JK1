paired_scatter_patient <- function(
  inDirName,
  dType,
  graphicsFormat='png',
  geneNL_sel=c()
)
{
  if (dType == 'CNA'){
    lab = 'CN (log2)'
  }else{
    lab = 'Expr (z-score)'
  }
  
  df = read.table(sprintf('%s/paired_df_%s.txt',inDirName,dType),header=TRUE)
  
  xSta=floor(min(df$val_p,df$val_r))
  xEnd=ceiling(max(df$val_p,df$val_r))
  
  xSta=max(abs(xSta),abs(xEnd)) * -1
  xEnd=max(abs(xSta),abs(xEnd))
  
  for (sId_p in unique(df[,1])) {
    
    df_ft = df[df$sId_p==sId_p,]
    sId_r = df_ft[1,2]
    
    if (graphicsFormat == 'png') {
      png(sprintf("%s/dType/paired_scatter_%s_%s_%s.png", inDirName,dType,sId_p,sId_r))
    } else if (graphicsFormat== 'pdf') {
      pdf(sprintf("%s/dType/paired_scatter_%s_%s_%s.pdf", inDirName,dType,sId_p,sId_r))
    }
    
    par(mfrow=c(1,1))
    
    idx_p10 = order(df_ft$val_p-df_ft$val_r)[1:10]
    idx_r10 = order(df_ft$val_r-df_ft$val_p)[1:10]
    
    df_ft_sel = df_ft[df_ft$geneN %in% geneNL_sel,]
    df_ft_pr10 = df_ft[c(idx_p10,idx_r10),]
    
    plot(df_ft$val_p, df_ft$val_r, xlim=c(xSta,xEnd), ylim=c(xSta,xEnd), xlab='',ylab='', pch=1, cex=0.5)
    par(new=T)
    plot(c(xSta,xEnd),c(xSta,xEnd), type='l',pch=22,lty=2, xlim=c(xSta,xEnd), ylim=c(xSta,xEnd),xlab='',ylab='')
    par(new=T)
    plot(df_ft_sel$val_p, df_ft_sel$val_r, xlim=c(xSta,xEnd), ylim=c(xSta,xEnd), xlab='',ylab='', pch=1, cex=1, col='red')
    par(new=T)
    plot(df_ft_pr10$val_p, df_ft_pr10$val_r, xlim=c(xSta,xEnd), ylim=c(xSta,xEnd), xlab='',ylab='', pch=1, cex=1, col='blue')
    
    for (i in seq(1,nrow(df_ft_sel))){   
      text(df_ft_sel[i,'val_p'],df_ft_sel[i,'val_r'],df_ft_sel[i,'geneN'],adj=c(0,1),col='red',cex=0.6)
    }
       
    for (i in 1:length(idx_p10)){
      
      x=-xEnd
      y=xEnd-(xEnd-xSta)*0.03*(i-1)
      
      text(x,y,sprintf('%4s\t%.3f %.3f',df_ft[idx_p10[i],'geneN'],df_ft[idx_p10[i],'val_p'],df_ft[idx_p10[i],'val_r']),col='blue',adj=c(0,1),cex=0.6)
      
    }
    
    for (i in 1:length(idx_r10)){
      
      x=xEnd #xEnd-(xEnd-xSta)*0.25
      y=xSta+(xEnd-xSta)*0.3-(xEnd-xSta)*0.03*i
      
      text(x,y,sprintf('%4s\t%.3f %.3f',df_ft[idx_r10[i],'geneN'],df_ft[idx_r10[i],'val_p'],df_ft[idx_r10[i],'val_r']),col='blue',adj=c(1,1),cex=0.6)
      
    }
    
    r = cor.test(df_ft$val_p, df_ft$val_r)
    
    title(main=sprintf('IRCR-GBM, %s, %s-%s (n=%d, R=%.2f)',dType,sId_p,sId_r,nrow(df_ft),r$estimate), xlab=sprintf('Prim, %s',lab), ylab=sprintf('Recur, %s',lab),cex.main=0.9)
    
    if (graphicsFormat=='png' || graphicsFormat=='pdf'){
      dev.off()
    }
  }
}

inDirName = '/EQL1/PrimRecur/paired'
geneNL_sel = c('EGFR','CDK4','CDK6','PDGFRA','MET','MDM2','MDM4','CDKN2A','CDKN2B','CDKN2C','PTEN','RB1','NF1','QKI')
dType = 'CNA'; graphicsFormat = ''; sId_p='S372'

for (dType in c('CNA','Expr'))
  for (fmt in c('png','pdf','')) paired_scatter_patient(inDirName,dType,fmt,geneNL_sel)

# for (dType in c('CNA','Expr'))
#   for (fmt in c('')) paired_scatter_patient(inDirName,dType,fmt,geneNL_sel)