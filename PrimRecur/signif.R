signif_mut <- function(
  inDirName,
  dType='skip',
  readCutOff=2
)
{
  df = read.table(sprintf('%s/signif_%s.txt',inDirName,dType),sep='\t',header=TRUE)
    
  df <- df[pmax(pmin(df$p_mt,df$p_wt),pmin(df$r_mt,df$r_wt))>readCutOff,]

  df_stat <- data.frame(oddratio=rep(NA,nrow(df)),pval=NA)
  
  for (i in 1:nrow(df)) {
    
    v <- t(df[i,c('p_mt','p_wt','r_mt','r_wt')])
    
    if (((v[1]>0 && v[4]>0) || (v[2]>0 && v[3]>0)) && max(min(v[1],v[2]),min(v[3],v[4]))>readCutOff) {
      
      result <- fisher.test(matrix(v,nrow=2))
      
      df_stat[i,'oddratio'] <- result$estimate
      df_stat[i,'pval'] <- result$p.value
      
    } else {
      
      df_stat[i,'oddratio'] <- NaN
      df_stat[i,'pval'] <- 1
    }
    
  }
  
  df <- cbind(df,df_stat)
  df <- df[order(df$pval),]
  
  write.table(df,sprintf('%s/signif_%s_stat.txt',inDirName,dType),sep='\t',row.names=F,quote=F)
}

#inDirName = '/EQL1/PrimRecur/signif'
inDirName = '/EQL1/PrimRecur/signif_20140107'
#dType = 'skip'
#dType = 'fusion'
 
#for (dType in c('mutation','fusion','skip','eiJunc'))
#for (dType in c('fusion'))
#for (dType in c('mutect_somatic'))
for (dType in 'mutation')
  signif_mut(inDirName,dType)
