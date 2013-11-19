paired_DEG <- function(
  inDirName,
  dType
)
{
  df = read.table(sprintf('%s/paired_df_%s.txt',inDirName,dType),header=T)
  df_sort = df[order(df[,3]),]
  df_sort$fc = df_sort$val_r - df_sort$val_p

  nGenes = length(unique(df_sort[,'geneN']))
  nPairs = length(unique(df_sort[,'sId_p']))
  resultM = matrix(nrow=nGenes, ncol=nPairs+3)
  
  geneN = ''
  startIdx = 0
  geneIdx = 0
  
  df_geneN = as.character(df_sort$geneN)
  df_fc = df_sort$fc
  
  for (i in 1:nrow(df_sort)) {

    if (df_geneN[i] != geneN) {
    
      if (geneN != '') {
        values = as.vector(df_fc[startIdx:(i-1)])        
        resultM[geneIdx,1:nPairs] = values
        resultM[geneIdx,nPairs+1] = mean(values)
        resultM[geneIdx,nPairs+2] = t.test(values)$p.value
        resultM[geneIdx,nPairs+3] = wilcox.test(values)$p.value
      }
      
      geneN = df_sort[i,'geneN']
      startIdx = i
      geneIdx = geneIdx + 1
    }
    
    if (i %% 1000==0) {
      print (i)
    }
  }

  values = as.vector(df_sort[startIdx:nrow(df_sort),'fc'])
  resultM[geneIdx,1:nPairs] = values
  resultM[geneIdx,nPairs+1] = mean(values)
  resultM[geneIdx,nPairs+2] = t.test(values)$p.value
  resultM[geneIdx,nPairs+3] = wilcox.test(values)$p.value
  
  resultDF = data.frame(resultM)
  names(resultDF) = c(as.character(unique(df_sort[,'sId_p'])),'fc','pv_t','pv_rs')
  resultDF$geneN = unique(df_sort[,'geneN'])
  
  resultDF = resultDF[,c('geneN',as.character(unique(df_sort[,'sId_p'])),'fc','pv_t','pv_rs')]
  resultDF = resultDF[order(resultDF$fc),]
  
  write.table(resultDF,file=sprintf("%s/DEG_%s.txt",inDirName,dType),quote=F,sep='\t',row.names=F)

}

#inDirName = '/EQL1/PrimRecur/paired'
#dType = 'Expr'
inDirName = '/EQL2/SGI_20131031/RNASeq/results'
dType = 'RPKM'

#for (dType in c('CNA','Expr','RPKM'))
#for (dType in c('CNA','RPKM'))
for (dType in c('RPKM'))
  paired_DEG(inDirName,dType)
