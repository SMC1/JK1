corrPlot <- function(
  inFileName,
  geneN,
  dType,
  tx
)
{
  df = read.table(inFileName,header=T)
  df$val_diff = df$val_r - df$val_p
  
  df_ft = df[df$geneN==geneN & df$dType==dType,]
  
  result = cor.test(df_ft$val_diff,df_ft$either)

  plot(df_ft[[tx]],df_ft$val_diff)    
  title(sprintf('%s %s %s (r=%.1f, p=%.1E)',geneN,dType,tx,result$estimate,result$p.value))
}

corrTable <- function(
  inFileName,
  outFileName
)
{
  df = read.table(inFileName,header=T)
  df$val_diff = df$val_r - df$val_p
  
  geneNL = c()
  dTypeL = c()
  txL = c()
  rL = c()
  pL = c()
  
  for (geneN in c('EGFR','CDK4','PDGFRA','MDM2','MDM4','MET','CDK6','CDKN2A','CDKN2B','PTEN','CDKN2C','RB1','QKI','NF1')) {
    for (dType in c('RPKM','Expr','CNA')) {
      for (tx in c('either','RT','chemo')) {
    
        df_ft = df[df$geneN==geneN & df$dType==dType,]
        #df_ft$geneN <- factor(df_ft$geneN[drop=TRUE],geneNL)
        
        result = cor.test(df_ft$val_diff,df_ft$either)

        geneNL = c(geneNL,geneN)
        dTypeL = c(dTypeL,dType)
        txL = c(txL,tx)
        rL = c(rL,result$estimate)
        pL = c(pL,result$p.value)
      }
    }
  }
  
  df_out = data.frame(geneN=geneNL,dType=dTypeL,tx=txL,r=rL,p=pL)
  
  write.table(df_out,outFileName,sep='\t',quote=F,row.names=F)
}

inFileName = '/EQL1/PrimRecur/paired/df_paired_tx.txt'
outFileName = '/EQL1/PrimRecur/paired/df_paired_tx_corr.txt'

corrTable(inFileName,outFileName)
corrPlot(inFileName,'PTEN','CNA','either')