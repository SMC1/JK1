getChrLen<-function(chromsizeFile='/data1/Sequence/ucsc_hg19/chromsizes_hg19.txt')
{
  chrLenDF = read.table(chromsizeFile,header=F)
  cumChrLen = data.frame(matrix(nrow=25,ncol=2))
  totChrLen = 0
  for (chr in c(1:22, c('X','Y','M'))) {
    if (chr=='X') {
      i = 23
    } else if (chr=='Y') {
      i = 24
    } else if (chr=='M') {
      i = 25
    } else { i = chr }
    cumChrLen[i, 1] = sprintf('chr%s',chr)
    cumChrLen[i, 2] = totChrLen
    totChrLen = totChrLen + chrLenDF[chrLenDF[,1]==sprintf('chr%s',chr),2]
  }
  colnames(cumChrLen)<-c("chrom","len")
  row.names(cumChrLen)<-cumChrLen$chrom
  ret=list()
  ret[[1]]<-cumChrLen
  ret[[2]]<-totChrLen
  return(ret)
}

drawTraj<-function(fileN, sampN, lColCommon=NaN, cnaMaxAbs=2, chromsizeFile='/data1/Sequence/ucsc_hg19/chromsizes_hg19.txt') {
  chrLen = getChrLen(chromsizeFile)
  totChrLen = chrLen[[2]]
  cumChrLen = chrLen[[1]]
  
  df = read.table(fileN, header=T)
  plot(c(0,totChrLen),c(0,0),ylab='CN (log2)',xlab='', xlim=c(0,totChrLen), ylim=c(-cnaMaxAbs,cnaMaxAbs), type='l',pch=22,lty=2,axes=T,ann=T,xaxs='i',yaxs='i',xaxt='n',cex.lab=1)
  totLen = 0
  for (chr in c(1:22,c('X','Y','M'))) {
    totLen = cumChrLen[sprintf('chr%s',chr),2]
    df_ft = df[df$chrom==chr,c(3,4,6)]
    df_ft = df_ft[order(df_ft$loc.start),]
    text(totLen,-cnaMaxAbs+cnaMaxAbs*2*0.03,chr,adj=c(0,0),col='grey',cex=1.1)
    
    if (nrow(df_ft) > 0) {
      for (j in 1:nrow(df_ft)) {
        if (is.nan(lColCommon)){
          if (df_ft[j,3]>=0.2) lCol = 'magenta'
          else if (df_ft[j,3]<=-0.2) lCol = 'green'
          else lCol = 'yellow'
        }else {
          lCol = lColCommon
        }
        
        if (df_ft[j,3]>=cnaMaxAbs) {
          lWth = 9
          df_ft[j,3] = cnaMaxAbs
        } else if (df_ft[j,3]<=-cnaMaxAbs) {
          lWth = 9
          df_ft[j,3] = -cnaMaxAbs
        } else {
          lWth = 3
        }
        lines(c(df_ft[j,1],df_ft[j,2])+totLen,c(df_ft[j,3],df_ft[j,3]),lwd=lWth,col=lCol)
      }
    }
    abline(v=totLen,pch=22,lty=2,col='grey')
  }
  abline(v=totChrLen,pch=22,lty=2,col='grey')
}

addCensus<-function(cumChrLen, cnaMaxAbs, upFile='/data1/Sequence/ucsc_hg19/annot/refFlat_censusA_pos.txt',dnFile='/data1/Sequence/ucsc_hg19/annot/refFlat_censusD_pos.txt')
{
  up = read.table(upFile,header=F,sep='\t',colClasses=c("character","character","numeric"))
  colnames(up)<-c("gene","chrom","pos")
  up$totPos <-0
  for (i in 1:nrow(up)) {
    up$totPos[i] = up[i,3] + cumChrLen[up[i,2],2]
  }
  axis(side=3, at=up$totPos, labels=F, col.ticks='red')
  text(x=up$totPos, par("usr")[4]+0.2, labels=up$gene, srt=90, pos=3, xpd=T, cex=0.6)
  segments(x0=up$totPos, y0=0, x1=up$totPos,y1=cnaMaxAbs, col='red')
  dn = read.table(dnFile,header=F,sep='\t',colClasses=c("character","character","numeric"))
  colnames(dn)<-c("gene","chrom","pos")
  dn$totPos<-0
  for (i in 1:nrow(dn)) {
    dn$totPos[i] = dn[i,3] + cumChrLen[dn[i,2],2]
    if (dn$gene[i] %in% c('FBXO11','FANCD2')) {
      dn$gene[i]<-''
    } else if (dn$gene[i] == 'MSH2') {
      dn$gene[i]<-'MSH2;FBXO11'
    } else if (dn$gene[i] == 'VHL') {
      dn$gene[i]<-'VHL;FANCD2'
    }
  }
  axis(side=1, at=dn$totPos, labels=F, col.ticks='blue')
  text(x=dn$totPos, y=par("usr")[3]-0.2, labels=dn$gene, srt=90, pos=1, xpd=T, cex=0.6, adj=1)
  segments(x0=dn$totPos, y0=0, x1=dn$totPos, y1=-cnaMaxAbs,col='blue')
}

drawTraj2<-function(fileN,sampN, lColCommon=NaN, cnaMaxAbs=2, chromsizeFile='/data1/Sequence/ucsc_hg19/chromsizes_hg19.txt') 
{
  chrLen = getChrLen(chromsizeFile)
  totChrLen = chrLen[[2]]
  cumChrLen = chrLen[[1]]
  
  df = read.table(fileN, header=T)
  plot(c(0,totChrLen),c(0,0),ylab='CN (log2)',xlab='', xlim=c(0,totChrLen), ylim=c(-cnaMaxAbs,cnaMaxAbs), type='l',pch=22,lty=2,axes=F,ann=T,xaxs='i',yaxs='i',xaxt='n',cex.lab=1)
  box()
  axis(side=2, at=seq(-3,3,by=1))
  addCensus(cumChrLen=cumChrLen, cnaMaxAbs=cnaMaxAbs)
  for (chr in c(1:22,c('X','Y','M'))) {
    totLen = cumChrLen[sprintf('chr%s',chr),2]
    df_ft = df[df$chrom==chr,c(3,4,6)]
    df_ft = df_ft[order(df_ft$loc.start),]
    text(totLen,-cnaMaxAbs+cnaMaxAbs*2*0.03,chr,adj=c(0,0),col='grey',cex=1.1)
    
    if (nrow(df_ft) > 0) {
      for (j in 1:nrow(df_ft)) {
        if (is.nan(lColCommon)){
          if (df_ft[j,3]>=0.2) lCol = 'red'
          else if (df_ft[j,3]<=-0.2) lCol = 'cyan'
          else lCol = 'yellow'
        }else {
          lCol = lColCommon
        }
        
        if (df_ft[j,3]>=cnaMaxAbs) {
          lWth = 9
          df_ft[j,3] = cnaMaxAbs
        } else if (df_ft[j,3]<=-cnaMaxAbs) {
          lWth = 9
          df_ft[j,3] = -cnaMaxAbs
        } else {
          lWth = 6
        }
        lines(c(df_ft[j,1],df_ft[j,2])+totLen,c(df_ft[j,3],df_ft[j,3]),lwd=lWth,col=lCol)
      }
    }
    abline(v=totLen,pch=22,lty=2,col='grey')
  }
  abline(v=totChrLen,pch=22,lty=2,col='grey')
  text(totChrLen*0.02,cnaMaxAbs-cnaMaxAbs*2*0.03,sprintf('%s',sampN),adj=c(0,1),cex=1.1)
}

args<-commandArgs(trailingOnly=T) ## 1:sampN, 2:prbFile, 3:segFile, 4:outName
sId <- args[1]
prbFile <- args[2]
segFile <- args[3]
outName <- args[4]

par(mgp=c(2,1,0), oma=c(1,2,1,1), mar=c(1,3,0,0))
format<-substr(outName, nchar(outName)-2, nchar(outName))
if (format == 'png') {
  png(outName, width=1000)
} else { 
  pdf(outName, width=10)
}
drawTraj(fileN=prbFile, sampN=sId, lColCommon='black'); par(new=T); drawTraj2(fileN=segFile, sampN=sId)
dev.off()
