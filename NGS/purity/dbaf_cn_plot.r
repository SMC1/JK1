args <- commandArgs(TRUE)

inDirName=args[1]
inCNDirName=args[2]
sId=args[3]
outDirName=args[4]

drawDbafTraj <- function(
  sId
){
  
  cnaMaxAbs = 1
  lColCommon = NaN

chrLenDF = read.table('/data1/Sequence/ucsc_hg19/chromsizes_hg19.txt',header=F)
totChrLen = 0

for (chr in c(1:22,c('X','Y','M'))) {
  totChrLen = totChrLen + chrLenDF[chrLenDF[,1]==sprintf('chr%s',chr),2]
}

df = read.delim(sprintf('%s/%s.dbaf.seg',inDirName,sId),header=T)

plot(c(0,totChrLen),c(0,0),ylab='delta BAF',xlim=c(0,totChrLen), ylim=c(0,cnaMaxAbs), type='l',pch=22,lty=2,axes=T,ann=T,xaxs='i',yaxs='i',xaxt='n',cex.lab=1)

totLen = 0

for (chr in c(1:22,c('X','Y','M'))) {
  
  chrLen = as.numeric(chrLenDF[chrLenDF[,1]==sprintf('chr%s',chr),2])
  
  df_ft = df[df$chrom==chr,c(3,4,6)]
  df_ft = df_ft[order(df_ft$loc.start),]
  text(totLen,cnaMaxAbs*2*0.03,chr,adj=c(0,0),col='grey',cex=1.1)
  
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

drawTraj <- function(
  sId
){
  
  cnaMaxAbs = 3
  lColCommon = NaN
  
  chrLenDF = read.table('/data1/Sequence/ucsc_hg19/chromsizes_hg19.txt',header=F)
  totChrLen = 0
  
  for (chr in c(1:22,c('X','Y','M'))) {
    totChrLen = totChrLen + chrLenDF[chrLenDF[,1]==sprintf('chr%s',chr),2]
  }
  
  df = read.delim(sprintf('%s/%s.copyNumber.seg',inCNDirName,sId),header=T)
  
  plot(c(0,totChrLen),c(0,0),ylab='CN (log2)',xlim=c(0,totChrLen), ylim=c(-cnaMaxAbs,cnaMaxAbs), type='l',pch=22,lty=2,axes=T,ann=T,xaxs='i',yaxs='i',xaxt='n',cex.lab=1)
  
  totLen = 0
  
  for (chr in c(1:22,c('X','Y','M'))) {
    
    chrLen = as.numeric(chrLenDF[chrLenDF[,1]==sprintf('chr%s',chr),2])
    
    df_ft = df[df$chrom==chr,c(3,4,6)]
    df_ft = df_ft[order(df_ft$loc.start),]
    df_ft = na.omit(df_ft) #
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

main <- function(
inDirName,
inCNDirName,
sId,
outDirName
){

  pdf(sprintf("%s/%s.dBAF_CNA_traj.pdf",outDirName,sId))
  
  par(mfrow=c(3,1),mgp=c(2,1,0))
  par(oma=c(1,2,1,1))
  par(mar=c(1,3,0,0))  
  
  cnaMaxAbs=1
  drawDbafTraj(sId); text(totChrLen*0.02,cnaMaxAbs-cnaMaxAbs*2*0.03,sprintf('%s',sId),adj=c(0,1),cex=1.1)
  
  cnaMaxAbs=3
  drawTraj(sId); text(totChrLen*0.02,cnaMaxAbs-cnaMaxAbs*2*0.03,sprintf('%s',sId),adj=c(0,1),cex=1.1)
  
  dev.off()

  print("Done")
}

main(inDirName,inCNDirName,sId,outDirName)
