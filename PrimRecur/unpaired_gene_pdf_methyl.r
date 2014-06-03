  unpaired_cdf <- function(
    inDirName,
    geneN,
    graphicsFormat=''
  )
  {
    
    df = read.table(sprintf('%s/df_unpaired_methyl.txt',inDirName),header=TRUE)
    
    if (graphicsFormat == 'png') {
      png(sprintf("%s/cdf/unpaired_cdf_%s.png", inDirName,geneN))
    } else if (graphicsFormat== 'pdf') {
      pdf(sprintf("%s/cdf/unpaired_cdf_%s.pdf", inDirName,geneN))
    }
    
    par(mfrow=c(2,2))
    par(oma=c(1,1,1,0), mar=c(4,3,2,2),mgp=c(2,1,0))
    
    for (dType in c('Methyl')) {
      
      df_ft = df[df$dbT==dbT & df$dType==dType & df$geneN==geneN,]
  
      valL_p = df_ft[df_ft$PR=='P','val']
      valL_r = df_ft[df_ft$PR=='R','val']
      
      qL = quantile(valL_p,c(.1,.9))
      
      boxplot(df_ft$val ~ df_ft$PR,vertical=T)
      #stripchart(df_ft$val ~ df_ft$PR,vertical=T, add=T, method='jitter', jitter=0.3,pch=1)
  
  	#ks.test(valL_p,valL_r)
      
      title(sprintf('%s, %s (%d,%d)',geneN,dType,length(valL_p),length(valL_r)))
    }
    
    if (graphicsFormat=='png' || graphicsFormat=='pdf'){    
      dev.off()
    }
  }
  
  inDirName = '/EQL1/PrimRecur/unpaired'
  #geneNL <- c('EGFR','CDK4','CDK6','PDGFRA','MET','MDM2','MDM4','CDKN2A','CDKN2B','CDKN2C','PTEN','RB1','NF1','QKI')
  geneNL <- c('EGFR')
  
  dbT = 'TCGA-GBM'
  
  for (geneN in geneNL)
    for (fmt in c('png','pdf','')) unpaired_cdf(inDirName,geneN,graphicsFormat=fmt)
  
  # unpaired_cdf(inDirName,'PDGFRA','')
