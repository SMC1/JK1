inDirName = '/EQL1/PrimRecur/paired'
inSegDirName = '/data1/IRCR/CGH/seg/seg/link'
graphicsFormat = ''
cnaMaxAbs = 3

chrLenDF = read.table('/data1/Sequence/ucsc_hg19/chromsizes_hg19.txt',header=F)
totChrLen = 0

for (chr in c(1:22,c('X','Y','M'))) {
  totChrLen = totChrLen + chrLenDF[chrLenDF[,1]==sprintf('chr%s',chr),2]
}

drawTraj <- function(
  sId,
  lColCommon=NaN,
  cnaMaxAbs=3
)
{
  df = read.table(sprintf('%s/%s.seg',inSegDirName,sId),header=T)
  
  plot(c(0,totChrLen),c(0,0),ylab='CN (log2)',xlim=c(0,totChrLen), ylim=c(-cnaMaxAbs,cnaMaxAbs), type='l',pch=22,lty=2,axes=T,ann=T,xaxs='i',yaxs='i',xaxt='n',cex.lab=1)
  
  totLen = 0
  
  for (chr in c(1:22,c('X','Y','M'))) {
    
    chrLen = as.numeric(chrLenDF[chrLenDF[,1]==sprintf('chr%s',chr),2])
    
    df_ft = df[df$chrom==chr,c(3,4,6)]
    df_ft = df_ft[order(df_ft$loc.start),]
    
    text(totLen,-cnaMaxAbs+cnaMaxAbs*2*0.03,chr,adj=c(0,0),col='grey',cex=1.1)

    if (nrow(df_ft) > 0) {
      
      for (j in 1:nrow(df_ft)) {
        
        if (is.nan(lColCommon)){
          if (df_ft[j,3]>=0.2) lCol = 'red'
          else if (df_ft[j,3]<=-0.2) lCol = 'blue'
          else lCol = 'black'
        }else {
          lCol = lColCommon
        }
        
        if (df_ft[j,3]>=cnaMaxAbs) {
          lWth = 6
          df_ft[j,3] = cnaMaxAbs
        } else if (df_ft[j,3]<=-cnaMaxAbs) {
          lWth = 6
          df_ft[j,3] = -cnaMaxAbs
        } else {
          lWth = 3
        }
        
        lines(c(df_ft[j,1],df_ft[j,2])+totLen,c(df_ft[j,3],df_ft[j,3]),lwd=lWth,col=lCol)
      }
    }
    
    abline(v=totLen,pch=22,lty=2,col='grey')
    
    totLen = totLen + chrLen
  }
    
  abline(v=totLen,pch=22,lty=2,col='grey')
}


paired_CNA_traj <- function(
  inDirName,
  inSegDirName,
  graphicsFormat='png'
)
{
  
  df = read.table(sprintf('%s/paired_df_CNA.txt',inDirName),header=TRUE)
  sIdPairDF = unique(df[,1:2])[,]
  sIdPriL = as.vector(sIdPairDF[,1])
  sIdRecL = as.vector(sIdPairDF[,2])
    
  for (i in 1:nrow(sIdPairDF)) {
    
    sId_p = sIdPriL[i]
    sId_r = sIdRecL[i]
    
    if (graphicsFormat == 'png') {
      png(sprintf("%s/CNA_traj/paired_CNA_traj_%s_%s.png", inDirName,sId_p,sId_r))
    } else if (graphicsFormat== 'pdf') {
      pdf(sprintf("%s/CNA_traj/paired_CNA_traj_%s_%s.pdf", inDirName,sId_p,sId_r))
    }
    
    par(mfrow=c(3,1),mgp=c(2,1,0))
    par(oma=c(1,2,1,1))
    par(mar=c(1,3,0,0))  
    
    drawTraj(sId_p); text(totChrLen*0.02,cnaMaxAbs-cnaMaxAbs*2*0.03,sprintf('%s',sId_p),adj=c(0,1),cex=1.1)
    drawTraj(sId_r); text(totChrLen*0.02,cnaMaxAbs-cnaMaxAbs*2*0.03,sprintf('%s',sId_r),adj=c(0,1),cex=1.1)
    drawTraj(sId_p,'green'); par(new=T); drawTraj(sId_r,'magenta'); text(totChrLen*0.02,cnaMaxAbs-cnaMaxAbs*2*0.03,sprintf('%s-%s',sId_p,sId_r),adj=c(0,1),cex=1)
    
    r = cor.test(df[df$sId_p==sId_p,'val_p'], df[df$sId_r==sId_r,'val_r'])$estimate
    text(totChrLen*0.02,cnaMaxAbs-cnaMaxAbs*2*0.12,sprintf('R = %.2f',r),adj=c(0,1),cex=1.1)
    
    if (graphicsFormat=='png' || graphicsFormat=='pdf'){
      dev.off()
    }
  }
  
}

# for (fmt in c('')) paired_CNA_traj(inDirName,inSegDirName,fmt)

for (fmt in c('png','pdf','')) paired_CNA_traj(inDirName,inSegDirName,fmt)
