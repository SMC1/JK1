getChrLen<-function(chr, chromsizeFile='/data1/Sequence/ucsc_hg19/chromsizes_hg19.txt')
{
  chrLenDF = read.table(chromsizeFile,header=F)
  return(chrLenDF[chrLenDF[,1]==sprintf('chr%s',chr),2])
}

drawTraj<-function(fileN, sampN, chr, lColCommon=NaN, cnaMaxAbs=3, chromsizeFile='/data1/Sequence/ucsc_hg19/chromsizes_hg19.txt') {
  chrLen = getChrLen(chr, chromsizeFile)

  df = read.table(fileN, header=F)
  colnames(df) <- c('chrom','loc.start','loc.end','V4','V5','value')
  
  plot(c(0,chrLen),c(0,0),ylab='CN (log2)',xlab='',main=sprintf('chr%s',chr), xlim=c(0,chrLen), ylim=c(-cnaMaxAbs,cnaMaxAbs), type='l',pch=22,lty=2,axes=T,ann=T,xaxs='i',yaxs='i',xaxt='n',cex.lab=1)
  
  addSScov(chr, cnaMaxAbs)
  df_ft = df[df$chrom == sprintf('chr%s', chr), c(2,3,6)]
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

args<-commandArgs(trailingOnly=T) ## 1:sampN, 2:prbFile, 3:outName
sId <- args[1]
prbFile <- args[2]
outName <- args[3]

#par(mgp=c(2,1,0), oma=c(1,2,1,1), mar=c(1,3,0,0))
format<-substr(outName, nchar(outName)-2, nchar(outName))
if (format == 'png') {
  png(outName, width=1000)
} else { 
  pdf(outName, width=20)
}
for (chr in c(1:22,'X','Y')) {
  drawTraj(chr, fileN=prbFile, sampN=sId, lColCommon='black')
}
dev.off()
