paired_delta <- function(
  inDirName
)
{
  
  par(mfcol=c(2,2))
  par(oma=c(1,1,1,0), mar=c(4,3,2,2), mgp=c(2,1,0))

  df = read.table(sprintf('%s/df_paired_gene_phillips.txt',inDirName),header=T)
  df$val_diff = df$val_r - df$val_p
  
  geneNL = 'EGFR'
  
#  for (dType in c('CNA','RPKM')) {
  for (dType in c('Expr')) {
  
    df_ft = df[df$geneN==geneN & substring(df$dType,1,2)==substring(dType,1,2)]
    
#     if (dType=='CNA') {
# 	    plot(df_ft$val_p,log10(2^df_ft$val_diff),ylim=c(-1.5,1.0))
#     }else{  
#       plot(log10(2^df_ft$val_p),log10(2^df_ft$val_diff),ylim=c(-1.5,1.0))
#     }
    
    plot(df_ft$val_p,df_ft$val_diff,ylim=c(-7,4))
    result <- cor.test(df_ft$val_p,df_ft$val_diff)
    
    title(sprintf("%s n=%d r=%f p=%f",dType,nrow(df_ft),result$estimate,result$p.value))
    abline(h=0)
        
  }
}

inDirName <- '/EQL1/PrimRecur/paired'
geneNLL <- list(Amp=c('EGFR','CDK4','PDGFRA','MDM2','MDM4','MET','CDK6'), Del=c('CDKN2A','CDKN2B','PTEN','CDKN2C','RB1','QKI','NF1'))
Cases <- c('S437','S586','S023','S697','S372','S538','S458','S453','S428','S460','S768','S780','S640','S096','S671','S592','S572','S520','S1A','S2A','S3A','S4A','S5A','S6A','S7A','S8A','S9A','S10A','S11A','S12A','S13A','S14A','S722','S171','S121','S652','S752','S386')

paired_delta(inDirName)
