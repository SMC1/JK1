paired_bubble <- function(
  inDirName,
  graphicsFormat='png'
)
{
    
  if (graphicsFormat == 'png') {
    png(sprintf("%s/bubble/paired_gene_bubble_matrix.png", inDirName))
  } else if (graphicsFormat== 'pdf') {
    pdf(sprintf("%s/bubble/paired_gene_bubble_matrix.pdf", inDirName))
  }
  
  par(mfrow=c(7,4))
  par(oma=c(2,2,1,1))
  par(mar=c(0,0,0,0))
  
  idx = 1
  
  for (geneN in c('EGFR','CDKN2A','CDK4','CDKN2B','PDGFRA','PTEN','MDM2','CDKN2C','MDM4','RB1','MET','QKI','CDK6','NF1')){
        
    for (dType in c('CNA','RPKM')){
      
      if (dType=='RPKM') {
        xSta = -1
        xEnd = 13
      } else {
        xSta = -7
        xEnd = 7
      }
      
      df = read.table(sprintf('%s/df_paired_gene.txt',inDirName),header=TRUE)
      df_ft = df[df$dType==dType & df$geneN==geneN,]
      
      df_ft$delta = df_ft$val_r-df_ft$val_p
      df_ft$color = as.character(df_ft$delta)
      df_ft$color[df_ft$delta >= 0] = 'red'
      df_ft$color[df_ft$delta <= 0] = 'blue'
      
      df_ft = df_ft[order(-abs(df_ft$delta)),]
      
      dmean = mean(df_ft$delta)*20
      dmean_scale = round(min(abs(dmean),50) * sign(dmean) + 51)
      plot(c(),c(), xlim=c(xSta,xEnd), ylim=c(xSta,xEnd), axes=F, ann=F,xaxt='n',yaxt='n', xaxs='i',yaxs='i')
      par(new=T)
      rect(xSta,xSta,xEnd,xEnd,border='black',col=bluered(101)[dmean_scale],xaxt='n',yaxt='n', xaxs='i',yaxs='i')
      par(new=T)
#       symbols(x=df_ft$val_p, y=df_ft$val_r, circles=abs(df_ft$delta)/5, inches=F, bg=df_ft$color, fg='black', xlim=c(xSta,xEnd), ylim=c(xSta,xEnd), ann=F, xaxs='i',yaxs='i', xaxt='n',yaxt='n')
      symbols(x=df_ft$val_p, y=df_ft$val_r, circles=abs(df_ft$delta)/5, inches=F, bg='white', fg='black', xlim=c(xSta,xEnd), ylim=c(xSta,xEnd), xaxs='i',yaxs='i', xaxt='n',yaxt='n')
      par(new=T)
      plot(c(xSta,xEnd),c(xSta,xEnd), type='l',pch=22,lty=2, xlim=c(xSta,xEnd), ylim=c(xSta,xEnd), axes=T, xaxt='n', yaxt='n', ann=F, xaxs='i',yaxs='i')
      axis(side = 1, tck=0.05, labels = F)
      axis(side = 2, tck=0.05, labels = F)
      
      idx = idx + 1
    }
  }
  
  if (graphicsFormat=='png' || graphicsFormat=='pdf'){    
    dev.off()
  }
}

inDirName = '/EQL1/PrimRecur/paired'

for (fmt in c('png','pdf','')) paired_bubble(inDirName,fmt)

# paired_bubble(inDirName,'')