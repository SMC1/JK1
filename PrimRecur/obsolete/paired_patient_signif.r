paired_patient_signif <- function(
  inDirName,
  outDirName,
  dType='skip',
  isPdf = T
)
{
  df = read.table(sprintf('%s/signif_%s_stat.txt',inDirName,dType),sep='\t',header=TRUE)
  df <- df[-which(df$p_wt==0 & df$r_wt==0),]
  
  for (sId_pair in unique(df$sId_pair)) {

    df_ft = df[df$sId_pair==sId_pair,]
    
    if(isPdf) pdf(sprintf('%s/signif_%s_%s.pdf',outDirName,dType,sId_pair))
    
    plot(ecdf(log10(df_ft[df_ft$oddratio>=1,'pval'])), xlim=c(-3,0), col='blue', main=sId_pair)
    par(new=T)
    plot(ecdf(log10(df_ft[df_ft$oddratio<1,'pval'])), xlim=c(-3,0), col='red', main='', axes=F)
    
    down = length(df_ft[df_ft$oddratio>1,'pval'])
    same = length(df_ft[df_ft$oddratio==1,'pval'])
    up = length(df_ft[df_ft$oddratio<1,'pval'])
    
    text(-3,1,sprintf('up: %d',up),adj=c(0,1))
    text(-3,0.9,sprintf('same: %d',same),adj=c(0,1))
    text(-3,0.8,sprintf('down: %d',down),adj=c(0,1))
    
    if(isPdf) dev.off()
  }
}

inDirName = '/EQL1/PrimRecur/signif'
outDirName = '/EQL1/PrimRecur/signif/pval_dist'
dType = 'skip'

#for (dType in c('fusion','skip','eiJunc'))
for (dType in c('skip'))
  paired_patient_signif(inDirName,outDirName,dType,T)