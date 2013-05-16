#inFileName <- '/data1/IRCR/WY/avastin_U87MG/data_edit1_beforeMax.txt'

inFileName <- '/data1/IRCR/human_beforeMax.txt'
outFileName <- '/data1/IRCR/human_afterMax.txt'

df = read.table(inFileName,header=T)
df_out = read.table(inFileName,header=T)
df_out[,] <- NaN

geneL = unique(df$GeneSymbol)
nGenes = length(geneL)

i = 1

for (g in geneL) {
  
  df_ft = df[df$GeneSymbol==g,]
  df_max = apply(df_ft[,2:ncol(df)],2,max)
  fc = mean(df_max[5:8])-mean(df_max[1:4])
  df_out[i,2]<-fc
  
  i = i+1
}

#write.table(df_out[order(df_out$fc),],'/data1/IRCR/WY/avastin_U87MG/ctrlVsAvastin_U87MG.rnk',sep='\t',quote=F,row.names=F)