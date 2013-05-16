inDirName <- '/data1/IRCR/WY'

geneN <- 'HIF1A'

groupL = list(list(c(2),3:5,'S827'),list(c(6),7:9,'S448'),list(c(10),11:13,'S559'),list(c(14),15:17,'S464'))

#pdf(sprintf("%s/matrix/paired_scatter_%s_3pair.pdf", inDirName,dType))

#opar=par()
par(mfcol=c(4,2))
par(oma=c(1,3,3,1))
par(mar=c(1.5,1.5,1.5,1.5))

yrange = c(-1,1)

for (dsetName in c('human','mouse')) {
  
  df = read.table(sprintf('%s/%s_quant_max.txt',inDirName,dsetName),header=T)
  df_ft <- df[df$GeneSymbol==geneN,]
  
  df_hk <- (df[df$GeneSymbol=='GAPDH',2:ncol(df)] + df[df$GeneSymbol=='ACTB',2:ncol(df)])/2
  df_ft[1,2:ncol(df_ft)] <- df_ft[1,2:ncol(df_ft)] - df_hk
  
  for (exp in groupL) {
    
    df_ft[1,exp[[2]]] <- df_ft[1,exp[[2]]] - df_ft[1,exp[[1]]]
    
    barplot(as.vector(t(df_ft[1,exp[[2]]])),ylim=yrange,col='white')
    abline(h=0)
    
  }
}

mtext(geneN,3,outer=T)

#par(opar)

#dev.off()
