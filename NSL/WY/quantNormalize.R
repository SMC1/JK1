inDirName <- '/data1/IRCR/WY'
dsetName <- 'mouse'

df = read.table(sprintf('%s/%s.txt', inDirName,dsetName),header=T)
#png(sprintf("%s/boxplot_human.pdf", inDirName))

par(oma=c(1,1,1,1))
par(mfrow=c(1,1))

df_mat <- as.matrix(log2(df[,2:ncol(df)]))

library(preprocessCore)
df_mat2 <- normalize.quantiles(df_mat)

boxplot(df_mat2)

df[,2:ncol(df)] <- df_mat2

write.table(df,sprintf('%s/%s_quant.txt', inDirName,dsetName),sep='\t',quote=F,row.names=F)

#dev.off()

# df_out = read.table(inFileName,header=T)
# df_out[,] <- NaN
# 
# geneL = unique(df$GeneSymbol)
# nGenes = length(geneL)
# 
# i = 1
# 
# for (g in geneL) {
#   
#   df_ft = df[df$GeneSymbol==g,]
#   df_max = apply(df_ft[,2:ncol(df)],2,max)
#   df_out[i,1]<-g
#   df_out[i,2:ncol(df_out)]<-df_max
#   
#   i = i+1
# }
# 
# df_out <- df_out[-(i:nrow(df_out)),]
# 
# write.table(df_out,outFileName,sep='\t',quote=F,row.names=F)