paired_scatter <- function(
  inDirName,
  geneN='EGFR',
  graphicsFormat='png',
  dTypeL=c('CNA','Expr','RPKM')
)
{
  
  if (graphicsFormat == 'png') {
    png(sprintf("%s/bubble/paired_bubble_%s.png", inDirName,geneN))
  } else if (graphicsFormat== 'pdf') {
    pdf(sprintf("%s/bubble/paired_bubble_%s.pdf", inDirName,geneN))
  }
  
  par(mfrow=c(2,2))
  par(oma=c(1,1,1,1))
  par(mar=c(2,2,2,1))  
  
  for (dType in dTypeL){
    
    if (dType=='RPKM') {
      xSta = -1
      xEnd = 13
    } else if (dType=='Expr') {
      xSta = 5
      xEnd = 17
    } else {
      xSta = -7
      xEnd = 7
    }
    
    if (dType == 'CNA'){
      lab = 'CN (log2)'
    }else if (dType == 'RPKM'){
      lab = 'log2(RPKM+1)'
    }else{
      lab = 'Expr (z-score)'
    }
    
    df = read.table(sprintf('%s/df_paired_gene.txt',inDirName),header=TRUE)
    df_ft = df[df$dType==dType & df$geneN==geneN,]
    
    pval_t <- t.test(df_ft$val_r-df_ft$val_p)['p.value']
    pval_r <- wilcox.test(df_ft$val_r-df_ft$val_p)['p.value']
    
    df_ft$delta = df_ft$val_r-df_ft$val_p
    df_ft$color = 'white'
#     df_ft$color = as.character(df_ft$delta)
#     df_ft$color[df_ft$delta >= 0] = 'red'
#     df_ft$color[df_ft$delta <= 0] = 'blue'
    
    df_ft$color[df_ft$sId_p=='S586'] = 'green'
    df_ft$color[df_ft$sId_p=='S453'] = 'green'
    df_ft$color[df_ft$sId_p=='S428'] = 'green'
    df_ft$color[df_ft$sId_p=='S372'] = 'green'
    
    ## snuh samples
    df_ft$color[grep(pattern="A", x=df_ft$sId_p)] = 'red'
    
    
    df_ft = df_ft[order(-abs(df_ft$delta)),]
    
    dmean = mean(df_ft$delta)*20
    dmean_scale = round(min(abs(dmean),50) * sign(dmean) + 51)
    plot(c(),c(), xlim=c(xSta,xEnd), ylim=c(xSta,xEnd), axes=F, ann=F, xaxt='n',yaxt='n', xaxs='i',yaxs='i')
    par(new=T)
    rect(xSta,xSta,xEnd,xEnd,border='black',col=bluered(101)[dmean_scale],xaxt='n',yaxt='n', xaxs='i',yaxs='i')
    par(new=T)
#     symbols(x=df_ft$val_p, y=df_ft$val_r, circles=abs(df_ft$delta)/5, inches=F, bg=df_ft$color, fg='black', xlim=c(xSta,xEnd), ylim=c(xSta,xEnd), xlab=sprintf('Prim, %s',lab), ylab=sprintf('Recur, %s',lab), xaxs='i',yaxs='i')
    symbols(x=df_ft$val_p, y=df_ft$val_r, circles=abs(df_ft$delta)/5, inches=F, bg=df_ft$color, fg='black', xlim=c(xSta,xEnd), ylim=c(xSta,xEnd), xlab=sprintf('Prim, %s',lab), ylab=sprintf('Recur, %s',lab), xaxs='i',yaxs='i')
    par(new=T)
    plot(c(xSta,xEnd),c(xSta,xEnd), type='l',pch=22,lty=2, xlim=c(xSta,xEnd), ylim=c(xSta,xEnd), axes=F, ann=F,  xaxs='i',yaxs='i')
    title(main=sprintf('%s %s (n=%d,m=%.2f,p_t=%.2E,p_r=%.2E)',geneN,dType,nrow(df_ft),mean(df_ft$val_r-df_ft$val_p),pval_t,pval_r),cex.main=0.7)
  }
  
  plot(c(),c(), xlim=c(0,1), ylim=c(0,1), axes=F, ann=F, xaxt='n',yaxt='n', xaxs='i',yaxs='i')
  color.legend(0,0,0.1,1,c(-2,-1,0,1,2),bluered(101)[10:91],gradient="y")
    
  if (graphicsFormat=='png' || graphicsFormat=='pdf'){    
    dev.off()
  }
}

require(gplots)
require(plotrix)
#inDirName = '/EQL1/PrimRecur/paired'
inDirName = '/EQL2/SGI_20131031/RNASeq/results'

for (geneN in c('EGFR','CDK4','CDK6','PDGFRA','MET','MDM2','MDM4','CDKN2A','CDKN2B','CDKN2C','PTEN','RB1','NF1','QKI','FGFR1','FGFR2','FGFR3','IGF1R','IDH1','IDH2','TP53')){
  for (fmt in c('png','pdf','')) paired_scatter(inDirName,geneN,fmt,c('RPKM'))
}

# paired_scatter(inDirName,'EGFR','')
