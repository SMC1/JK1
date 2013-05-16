paired_corr_matrix <- function(
  inDirName,
  dType,
  graphicsFormat='png'
)
{
  df = read.table(sprintf('%s/paired_df_%s.txt',inDirName,dType),header=TRUE)
  
  if (graphicsFormat == 'png') {
    png(sprintf("%s/matrix/paired_corr_matrix_%s.png", inDirName,dType))
  } else if (graphicsFormat== 'pdf') {
    pdf(sprintf("%s/matrix/paired_corr_matrix_%s.pdf", inDirName,dType))
  }
  
  sIdPairDF = unique(df[,1:2])[,]
  sIdPriL = as.vector(sIdPairDF[,1])
  sIdRecL = as.vector(sIdPairDF[,2])
  
  par(mfrow=c(length(sIdPriL),length(sIdRecL)))
  par(oma=c(1,1,1,1))
  par(mar=c(0,0,0,0))
  
  for (sId_p in sIdPriL) {
    
    for (sId_r in sIdRecL) {
      
      r = cor.test(df[df$sId_p==sId_p,'val_p'], df[df$sId_r==sId_r,'val_r'])$estimate
      
      colAmp = sub(' ',0,sprintf('%2x',round((-abs(r)+1)*255)))
      if (r>=0) bgColCode = sprintf('#ff%s%s',colAmp,colAmp)
      else bgColCode = sprintf('#%s%sff',colAmp,colAmp)
      
      plot(c(),c(),xlim=c(-1,1),ylim=c(-1,1),axes=F,ann=F,xaxt='n',yaxt='n')
      par(new=T)
      rect(-1,-1,1,1,border='white',col=bgColCode)
      if (which(sIdPriL==sId_p)==which(sIdRecL==sId_r)){
        par(new=T)
        plot(c(-1,1),c(1,-1), type='l',pch=22,lty=2,xlim=c(-1,1),ylim=c(-1,1),axes=F,ann=F,xaxt='n',yaxt='n')
      }

      text(-1,1,sprintf('%s',sId_p),adj=c(0,1),cex=1)
      text(-1,0.4,sprintf('%s',sId_r),adj=c(0,1),cex=1)
      text(-1,-0.2,sprintf('R = %.2f',r),adj=c(0,1),cex=0.9)
    }
    
  }
    
  if (graphicsFormat=='png' || graphicsFormat=='pdf'){
    dev.off()
  }
}

inDirName = '/EQL1/PrimRecur/paired'
dType = 'CNA'; graphicsFormat = ''

for (dType in c('CNA','Expr','RPKM'))
  for (fmt in c('png','pdf','')) paired_corr_matrix(inDirName,dType,fmt)

# for (dType in c('RPKM'))
#   for (fmt in c('')) paired_corr_matrix(inDirName,dType,fmt)
