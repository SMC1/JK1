drawTraj<-function(fileN,sampN, addChr=FALSE, lColCommon=NaN, cnaMaxAbs=3, chromsizeFile='/data1/Sequence/ucsc_hg19/chromsizes_hg19.txt') 
{
  chrLenDF = read.table(chromsizeFile,header=F)
  totChrLen = 0
  for (chr in c(1:22, c('X','Y','M'))) {
    totChrLen = totChrLen + chrLenDF[chrLenDF[,1]==sprintf('chr%s',chr),2]
  }
  
  df = read.table(fileN, header=T)
  plot(c(0,totChrLen),c(0,0),ylab='CN (log2)',xlab='', xlim=c(0,totChrLen), ylim=c(-cnaMaxAbs,cnaMaxAbs), type='l',pch=22,lty=2,axes=T,ann=T,xaxs='i',yaxs='i',xaxt='n',cex.lab=1)
  totLen = 0
  for (chr in c(1:22,c('X','Y','M'))) {
    chrLen = as.numeric(chrLenDF[chrLenDF[,1]==sprintf('chr%s',chr),2])
    if (addChr) df_ft = df[df$chrom==sprintf('chr%s',chr),c(3,4,6)]
	else df_ft = df[df$chrom==chr,c(3,4,6)]
    df_ft = df_ft[order(df_ft$loc.start),]
    text(totLen,-cnaMaxAbs+cnaMaxAbs*2*0.03,chr,adj=c(0,0),col='grey',cex=1.1)
    
    if (nrow(df_ft) > 0) {
      for (j in 1:nrow(df_ft)) {
        if (is.nan(lColCommon)){
          if (df_ft[j,3]>=0.2) lCol = 'red'
          else if (df_ft[j,3]<=-0.2) lCol = 'cyan'
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
  text(totChrLen*0.02,cnaMaxAbs-cnaMaxAbs*2*0.03,sprintf('%s',sampN),adj=c(0,1),cex=1.1)
}

paired_CNA_traj<-function(aFile,xFile,sId,xDatN,cnaMaxAbs=3, chromsizeFile='/data1/Sequence/ucsc_hg19/chromsizes_hg19.txt')
{
  chrLenDF = read.table(chromsizeFile,header=F)
  totChrLen = 0
  for (chr in c(1:22, c('X','Y','M'))) {
    totChrLen = totChrLen + chrLenDF[chrLenDF[,1]==sprintf('chr%s',chr),2]
  }
  
  par(mfrow=c(3,1),mgp=c(2,1,0))
  par(oma=c(1,2,1,1))
  par(mar=c(1,3,0,0))
  drawTraj(fileN=aFile,sampN=sprintf('%s (aCGH)',sId),cnaMaxAbs=cnaMaxAbs,chromsizeFile=chromsizeFile);
  drawTraj(fileN=xFile,sampN=sprintf('%s (WXS)',sId),addChr=TRUE, cnaMaxAbs=cnaMaxAbs,chromsizeFile=chromsizeFile);
  drawTraj(fileN=aFile,sampN='',lColCommon='green',cnaMaxAbs=cnaMaxAbs,chromsizeFile=chromsizeFile);par(new=T);drawTraj(fileN=xFile,sampN='',lColCommon='magenta',addChr=TRUE,cnaMaxAbs=cnaMaxAbs,chromsizeFile=chromsizeFile)

  aCN<-read.table('/EQL1/PrimRecur/paired/paired_df_CNA.txt',header=T)
  xCN<-read.table(xDatN,header=F)
  if (sId %in% unique(aCN$sId_p))
  {
    a<-aCN[ aCN$sId_p == sId, c('geneN','val_p')]
  }
  else if (sId %in% unique(aCN$sId_r))
  {
    a<-aCN[ aCN$sId_r == sId, c('geneN','val_r')]
  }
  a<-a[ order(a$geneN),]
  b<-xCN[,c(2,3)]
  b<-b[ order(b[,1]), ]
  r=cor.test(a[,2], b[,2])$estimate
  text(totChrLen*0.02,cnaMaxAbs-cnaMaxAbs*2*0.12,sprintf('R = %.2f',r),adj=c(0,1),cex=1.1)
}


args<-commandArgs(trailingOnly=T) ## 1:segFile (aCGH), 2: segFile (WXS), 3: sampN, 4: datFile (WXS), 5: outName
aSeg<-args[1]
xSeg<-args[2]
sampN<-args[3]
cn_dat<-args[4]
outName<-args[5]

par(mgp=c(2,1,0), oma=c(1,2,1,1), mar=c(1,3,0,0))
format<-substr(outName, nchar(outName)-2, nchar(outName))
if (format == 'png') {
  png(outName, width=1000)
} else { 
  pdf(outName, width=10)
}
paired_CNA_traj(aFile=aSeg,xFile=xSeg,sId=sampN,xDatN=cn_dat,cnaMaxAbs=3, chromsizeFile='/data1/Sequence/ucsc_hg19/chromsizes_hg19.txt')
dev.off()
