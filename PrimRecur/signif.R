signif_mut <- function(
  inDirName,
  dType='skip'
)
{
  df = read.table(sprintf('%s/signif_%s.txt',inDirName,dType),sep='\t',header=TRUE)
    
  df_stat <- data.frame(oddratio=rep(NA,nrow(df)),pval=NA)
  
  for (i in 1:nrow(df)) {
    
    v <- t(df[i,c('p_mt','p_wt','r_mt','r_wt')])
    
    if ((v[1]>0 && v[4]>0) || (v[2]>0 && v[3]>0)) {
      
      result <- fisher.test(matrix(v,nrow=2))
      
      df_stat[i,'oddratio'] <- result$estimate
      df_stat[i,'pval'] <- result$p.value
      
    } else {
      
      df_stat[i,'oddratio'] <- 0
      df_stat[i,'pval'] <- 1
    }
    
  }
  
  df <- cbind(df,df_stat)
  df <- df[order(df$pval),]
  
  write.table(df,sprintf('%s/signif_%s_stat.txt',inDirName,dType),sep='\t',row.names=F,quote=F)
}

inDirName = '/EQL1/PrimRecur/signif'
dType = 'skip'

#for (dType in c('fusion','skip','eiJunc'))
for (dType in c('mutation'))
  signif_mut(inDirName,dType)