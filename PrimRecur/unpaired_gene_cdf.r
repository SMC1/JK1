unpaired_cdf <- function(
  inDirName,
  geneN,
  graphicsFormat=''
)
{
  
  df = read.table(sprintf('%s/df_unpaired2.txt',inDirName),header=TRUE)
  
  if (graphicsFormat == 'png') {
    png(sprintf("%s/cdf/unpaired_cdf_%s.png", inDirName,geneN))
  } else if (graphicsFormat== 'pdf') {
    pdf(sprintf("%s/cdf/unpaired_cdf_%s.pdf", inDirName,geneN))
  }
  
  par(mfrow=c(2,2))
  par(oma=c(1,1,1,0), mar=c(4,3,2,2),mgp=c(2,1,0))
  
  for (dType in c('CNA','Expr')) {
    
    df_ft = df[df$dbT==dbT & df$dType==dType & df$geneN==geneN,]
                        
    valL_p = df_ft[df_ft$geneN==geneN & df_ft$PR=='P','val']
    valL_r = df_ft[df_ft$geneN==geneN & df_ft$PR=='R','val']
    
    qL = quantile(valL_p,c(.1,.9))
    
    plot(ecdf(valL_p),verticals=T,xlim=qL,ylim=c(0,1),pch=46,main='')
    par(new=T)
    plot(ecdf(valL_r),verticals=T,axes=F,ann=F,xlim=qL,ylim=c(0,1),pch=46,main='')

	#ks.test(valL_p,valL_r)
    
    title(sprintf('%s, %s (%d,%d)',geneN,dType,length(valL_p),length(valL_r)))
  }
  
  if (graphicsFormat=='png' || graphicsFormat=='pdf'){    
    dev.off()
  }
}

inDirName = '/EQL1/PrimRecur/unpaired'
#geneNL <- c('EGFR','CDK4','CDK6','PDGFRA','MET','MDM2','MDM4','CDKN2A','CDKN2B','CDKN2C','PTEN','RB1','NF1','QKI')
geneNL <- c('EGFR','PDGFRA')

dbT = 'TCGA-GBM'

for (geneN in geneNL)
  for (fmt in c('png','pdf','')) unpaired_cdf(inDirName,geneN,graphicsFormat=fmt)

# unpaired_cdf(inDirName,'PDGFRA','')
