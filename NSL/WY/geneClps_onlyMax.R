inFileName <- '/data1/IRCR/WY/mouse_quant.txt'
outFileName <- '/data1/IRCR/WY/mouse_quant_max.txt'

# inFileName <- '/data1/IRCR/WY/human_quant.txt'
# outFileName <- '/data1/IRCR/WY/human_quant_max.txt'

df = read.table(inFileName,header=T)
df = df[df$GeneSymbol %in% c('ACTB','GAPDH','TLN1','HIF1A'),]
df_out = read.table(inFileName,header=T)
df_out[,] <- NaN

geneL = unique(df$GeneSymbol)
nGenes = length(geneL)

i = 1

for (g in geneL) {
  
  df_ft = df[df$GeneSymbol==g,]
  df_max = apply(df_ft[,2:ncol(df)],2,max)
  df_out[i,1]<-g
  df_out[i,2:ncol(df_out)]<-df_max
  
  i = i+1
}

df_out <- df_out[-(i:nrow(df_out)),]

write.table(df_out,outFileName,sep='\t',quote=F,row.names=F)