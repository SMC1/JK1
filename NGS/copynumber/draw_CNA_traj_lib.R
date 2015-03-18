getChrLenAll<-function(chromsizeFile='/data1/Sequence/ucsc_hg19/chromsizes_hg19.txt')
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

addCensusAll<-function(cumChrLen, cnaMaxAbs, upFile='/data1/Sequence/ucsc_hg19/annot/refFlat_censusA_pos.txt',dnFile='/data1/Sequence/ucsc_hg19/annot/refFlat_censusD_pos.txt')
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

drawTrajAll<-function(fileN,sampN, lColCommon='black', cnaMaxAbs=2, chromsizeFile='/data1/Sequence/ucsc_hg19/chromsizes_hg19.txt') 
{
  chrLen = getChrLenAll(chromsizeFile)
  totChrLen = chrLen[[2]]
  cumChrLen = chrLen[[1]]
  
  df = read.table(fileN, header=T)
  plot(c(0,totChrLen),c(0,0),ylab='CN (log2)',xlab='', xlim=c(0,totChrLen), ylim=c(-cnaMaxAbs,cnaMaxAbs), type='l',pch=22,lty=2,axes=F,ann=T,xaxs='i',yaxs='i',xaxt='n',cex.lab=1)
  box()
  axis(side=2, at=seq(-3,3,by=1))
  addCensusAll(cumChrLen=cumChrLen, cnaMaxAbs=cnaMaxAbs)
  for (chr in c(1:22,c('X','Y','M'))) {
    totLen = cumChrLen[sprintf('chr%s',chr),2]
    if (nchar(as.character(df$chrom[1]))>3) {
      df_ft = df[df$chrom==sprintf('chr%s',chr),c(3,4,6)]
    } else {
      df_ft = df[df$chrom==sprintf('%s',chr),c(3,4,6)]
    }
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

getChrLen<-function(chr, chromsizeFile='/data1/Sequence/ucsc_hg19/chromsizes_hg19.txt')
{
  chrLenDF = read.table(chromsizeFile,header=F)
  return(chrLenDF[chrLenDF[,1]==sprintf('chr%s',chr),2])
}

addCensus<-function(chr, cnaMaxAbs, upFile='/data1/Sequence/ucsc_hg19/annot/refFlat_censusA_pos.txt',dnFile='/data1/Sequence/ucsc_hg19/annot/refFlat_censusD_pos.txt')
{
  up = read.table(upFile,header=F,sep='\t',colClasses=c("character","character","numeric"))
  colnames(up)<-c("gene","chrom","pos")
  up = up[up$chrom == sprintf('chr%s',chr), ]
  
  axis(side=3, at=up$pos, labels=F, col.ticks='red')
  if (nrow(up) > 0 ) {  
    text(x=up$pos, par("usr")[4]+0.2, labels=up$gene, srt=90, pos=3, xpd=T, cex=0.6)
    segments(x0=up$pos, y0=0, x1=up$pos,y1=cnaMaxAbs, col='red')
  }#if
  
  dn = read.table(dnFile,header=F,sep='\t',colClasses=c("character","character","numeric"))
  colnames(dn)<-c("gene","chrom","pos")
  dn = dn[dn$chrom == sprintf('chr%s',chr), ]
  
  axis(side=1, at=dn$pos, labels=F, col.ticks='blue')
  if (nrow(dn) > 0 ) {
    for (i in 1:nrow(dn)) {
      if (dn$gene[i] %in% c('FBXO11','FANCD2')) {
        dn$gene[i]<-''
      } else if (dn$gene[i] == 'MSH2') {
        dn$gene[i]<-'MSH2;FBXO11'
      } else if (dn$gene[i] == 'VHL') {
        dn$gene[i]<-'VHL;FANCD2'
      }
    }
    text(x=dn$pos, y=par("usr")[3]-0.2, labels=dn$gene, srt=90, pos=1, xpd=T, cex=0.6, adj=1)
    segments(x0=dn$pos, y0=0, x1=dn$pos, y1=-cnaMaxAbs,col='blue')
  }#if
}

addSScov<-function(chr, cnaMaxAbs, bedFile='/data1/Sequence/ucsc_hg19/annot/refFlat_hg19_gene_merged500000.bed')
{
  dat<-read.table(bedFile, header=F, sep='\t', colClasses=c("character","numeric","numeric",NULL))
  colnames(dat)<-c("chrom","begin","end")
  dat<-dat[dat$chrom == sprintf('chr%s',chr), ]
  
  if (nrow(dat) > 0)
  {
    rect(xleft=dat$begin, xright=dat$end, ybottom=-cnaMaxAbs, ytop=cnaMaxAbs, col='green', border=F, density=30)
  }#if
}#function

drawTraj_chromwise<-function(fileN, sampN, chr, lColCommon=NaN, cnaMaxAbs=3, chromsizeFile='/data1/Sequence/ucsc_hg19/chromsizes_hg19.txt')
{
  chrLen = getChrLen(chr, chromsizeFile)
  
  df = read.table(fileN, header=F)
  colnames(df) <- c('chrom','loc.start','loc.end','V4','V5','value')
  
  plot(c(0,chrLen),c(0,0),ylab='CN (log2)',xlab='',main=sprintf('%s (chr%s)', sampN, chr), xlim=c(0,chrLen), ylim=c(-cnaMaxAbs,cnaMaxAbs), type='l',pch=22,lty=2,axes=T,ann=T,xaxs='i',yaxs='i',xaxt='n',cex.lab=1)
  
  addSScov(chr, cnaMaxAbs)
  df_ft = df[df$chrom == sprintf('chr%s', chr), c(2,3,6)]
  df_ft = df_ft[!is.na(df_ft[,3]), ]
  df_ft = df_ft[order(df_ft$loc.start),]
  
  if (nrow(df_ft) > 0) {
    for (j in 1:nrow(df_ft)) {
      if (is.nan(lColCommon)) {
        if (df_ft[j, 3]>=0.2) lCol = 'magenta'
        else if (df_ft[j, 3]<=-0.2) lCol='green'
        else lCol='yellow'
      } else {
        lCol = lColCommon
      }#if
      
      if (df_ft[j,3] >= cnaMaxAbs) {
        lWth = 9
        df_ft[j,3] = cnaMaxAbs
      } else if (df_ft[j,3] <= -cnaMaxAbs) {
        lWth = 9
        df_ft[j,3] = -cnaMaxAbs
      } else {
        lWth = 3
      }#if
      
      lines(c(df_ft[j,1],df_ft[j,2]), c(df_ft[j,3],df_ft[j,3]),lwd=lWth,col=lCol)
    }# for j
  }# if
  ## vertical lines per 10,000,000 bases
  for (i in 1:floor(chrLen/10000000))
  {
    abline(v=i * 10000000, pch=22, lty=2, col='grey')
    text(i*10000000,-cnaMaxAbs+cnaMaxAbs*2*0.03,i,adj=c(0,0),col='grey',cex=1.1)
  }
  addCensus(chr, cnaMaxAbs=cnaMaxAbs)
}