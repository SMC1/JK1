paired_CNA_traj <- function(
  inDirName,
  inSegDirName,
  graphicsFormat='png',
  chrLenFileName='/data1/Sequence/ucsc_hg19/chromsizes_hg19.txt'
)
{
  
  chrLenDF = read.table(chrLenFileName,header=F)
  totChrLen = 0
  
  for (chr in c(1:22,c('X','Y','M'))) {
    totChrLen = totChrLen + chrLenDF[chrLenDF[,1]==sprintf('chr%s',chr),2]
  }
  
  df = read.table(sprintf('%s/paired_df_CNA.txt',inDirName),header=TRUE)
  sIdPairDF = unique(df[,1:2])[,]
  sIdPriL = as.vector(sIdPairDF[,1])
  sIdRecL = as.vector(sIdPairDF[,2])
  
  if (graphicsFormat == 'png') {
    png(sprintf("%s/matrix/paired_CNA_traj.png", inDirName))
  } else if (graphicsFormat== 'pdf') {
    pdf(sprintf("%s/matrix/paired_CNA_traj.pdf", inDirName))
  }
  
  par(mfrow=c(length(sIdPriL),1))
  par(oma=c(1,2,1,1))
  par(mar=c(1,0,0,0))
  
  #   xSta=floor(min(df$val_p,df$val_r))
  #   xEnd=ceiling(max(df$val_p,df$val_r))
  #   
  #   xSta=max(abs(xSta),abs(xEnd)) * -1
  #   xEnd=max(abs(xSta),abs(xEnd))
  
  cnaMin = -1
  cnaMax = 1
  
  for (i in 1:nrow(sIdPairDF)) {
    
    sId_p = sIdPriL[i]
    sId_r = sIdRecL[i]
    
    df = read.table(sprintf('%s/%s.seg',inSegDirName,sId_p),header=T)
    
    plot(c(0,totChrLen),c(0,0),xlim=c(0,totChrLen), ylim=c(cnaMin,cnaMax), type='l',pch=22,lty=2,axes=T,ann=F,xaxt='n')
    
    totLen = 0
    
    for (chr in c(1:22,c('X','Y','M'))) {
      
      chrLen = as.numeric(chrLenDF[chrLenDF[,1]==sprintf('chr%s',chr),2])
      
      df_ft = df[df$chrom==chr,c(3,4,6)]
      df_ft = df_ft[order(df_ft$loc.start),]
      
      if (nrow(df_ft) > 0) {
        
        for (j in 1:nrow(df_ft)) {
          
          if (df_ft[j,3]>=0.2) lCol = 'red'
          else if (df_ft[j,3]<=-0.2) lCol = 'blue'
          else lCol = 'black'
          
          if (df_ft[j,3]>=cnaMax) {
            lWth = 5
            df_ft[j,3] = cnaMax
          } else if (df_ft[j,3]<=cnaMin) {
            lWth = 5
            df_ft[j,3] = cnaMin
          } else {
            lWth = 3
          }
          
          lines(c(df_ft[j,1],df_ft[j,2])+totLen,c(df_ft[j,3],df_ft[j,3]),lwd=lWth,col=lCol)
        }
      }
      
      totLen = totLen + chrLen
    }
    
    #     r = cor.test(df[df$sId_p==sId_p,'val_p'], df[df$sId_r==sId_r,'val_r'])$estimate
    # 
    #     text(-1,1,sprintf('%s',sId_p),adj=c(0,1),cex=1)
    #     text(-1,0.4,sprintf('%s',sId_r),adj=c(0,1),cex=1)
    #     text(-1,-0.2,sprintf('R = %.2f',r),adj=c(0,1),cex=0.9)
  }
  
  if (graphicsFormat=='png' || graphicsFormat=='pdf'){
    dev.off()
  }
}

inDirName = '/EQL1/PrimRecur/paired'
inSegDirName = '/data1/IRCR/CGH/seg/link'
graphicsFormat = ''

# for (fmt in c('png','pdf','')) paired_CNA_traj(inDirName,fmt)

for (fmt in c('')) paired_CNA_traj(inDirName,inSegDirName,fmt)
