paired_scatter_matrix <- function(
  inDirName,
  dType,
  graphicsFormat='png'
)
{
  if (dType == 'CNA'){
    lab = 'CN (log2)'
  }else{
    lab = 'Expr (z-score)'
  }
  
  df = read.table(sprintf('%s/paired_df_%s.txt',inDirName,dType),header=TRUE)
  
  if (graphicsFormat == 'png') {
    png(sprintf("%s/matrix/paired_scatter_%s_3pair.png", inDirName,dType))
  } else if (graphicsFormat== 'pdf') {
    pdf(sprintf("%s/matrix/paired_scatter_%s_3pair.pdf", inDirName,dType))
  }
  
  xSta=floor(min(df$val_p,df$val_r))
  xEnd=ceiling(max(df$val_p,df$val_r))
       
  if (dType=='RPKM') xSta=0 
  else xSta=max(abs(xSta),abs(xEnd)) * -1
  xEnd=max(abs(xSta),abs(xEnd))
  
  sIdPairDF = unique(df[,1:2])[2:4,]
  sIdPriL = as.vector(sIdPairDF[,1])
  sIdRecL = as.vector(sIdPairDF[,2])
  
  par(mfrow=c(length(sIdPriL),length(sIdRecL)))
  par(oma=c(1,1,1,1))
  par(mar=c(0,0,0,0))
  
  for (sId_p in sIdPriL) {
    
    for (sId_r in sIdRecL) {
      
      plot(df[df$sId_p==sId_p,'val_p'], df[df$sId_r==sId_r,'val_r'], xlim=c(xSta,xEnd), ylim=c(xSta,xEnd), ann=F, pch=1, cex=0.55, cex.axis=0.7)
      par(new=T)
      plot(c(xSta,xEnd),c(xSta,xEnd), type='l',pch=22,lty=2, xlim=c(xSta,xEnd), ylim=c(xSta,xEnd),xaxt='n', yaxt='n', ann=F)
      
      r = cor.test(df[df$sId_p==sId_p,'val_p'], df[df$sId_r==sId_r,'val_r'])$estimate
      text(xSta,xEnd,sprintf('%s-%s',sId_p,sId_r),adj=c(0,1),cex=0.9)
      text(xSta,xEnd-(xEnd-xSta)*0.1,sprintf('R = %.2f',r),adj=c(0,1),cex=0.9)
    }
    
  }
    
  if (graphicsFormat=='png' || graphicsFormat=='pdf'){
    dev.off()
  }
}

inDirName = '/EQL1/PrimRecur/paired'
dType = 'CNA'; graphicsFormat = ''

for (dType in c('CNA','Expr','RPKM'))
  for (fmt in c('png','pdf','')) paired_scatter_matrix(inDirName,dType,fmt)

# for (dType in c('RPKM'))
#   for (fmt in c('')) paired_scatter_matrix(inDirName,dType,fmt)
