data = read.table("/EQL6/NSL/Barcode/NY/NY_S827_count.txt",sep='\t',header=T)
colTot = colSums(data[,-1])
data = data[data[,2]>=1000,]
ctrlCnt = data[,2]

# data[,-1] = t(apply(data[,-1], 1, function(x) x/colTot))
for (i in 1:nrow(data)){
  data[i,-1] = data[i,-1]/colTot
}

data[,c(-1,-2)] = data[,c(-1,-2)]/data[,2]
# for (i in 3:ncol(data)){
#   data[,i] = data[,i]/data[,2]
# }

data[,-1] = log2(data[,-1])

geneNameL = c('BTG3','CTNNB1','DDAH1','DDX6','FBXW7','GNG10','HERPUD1','KIF11','KRIT1','MAPK14','MDM2','MGC16025','MYC','MYD88','NSC','P4HTM','PRMT7','PRTG','RFX7','RRM1','SLC10A5','TGFB1','TP53','WEE1','ZNF649')
expNameL = c('G2','G3','G4','G5')

pvalues_shRNA = data.frame(matrix(nrow=nrow(data),ncol=length(expNameL)))
names(pvalues_shRNA) = expNameL
fc_shRNA = data.frame(matrix(nrow=nrow(data),ncol=length(expNameL)))
names(fc_shRNA) = expNameL

pvalues_gene = data.frame(matrix(nrow=nrow(data),ncol=length(expNameL)))
names(pvalues_gene) = expNameL
fc_gene = data.frame(matrix(nrow=nrow(data),ncol=length(expNameL)))
names(fc_gene) = expNameL

pvalues_tot = matrix(nrow=nrow(data),ncol=1)
fc_tot = matrix(nrow=nrow(data),ncol=1)

for (i in 1:nrow(data)){
  for (eN in expNameL){
    values_f = data[i, grep(eN,names(data))]
    values_b = data[grep(sprintf('%s-',gN),data[,1])*-1, grep(eN,names(data))]
    pvalues_shRNA[[eN]][i]=ks.test(c(as.matrix(values_f)),c(as.matrix(values_b)))$p.value
    fc_shRNA[[eN]][i]=mean(c(as.matrix(values_f)))
  }
}

for (gN in geneNameL){
  for (eN in expNameL){
    if (length(grep(sprintf('%s-',gN),data[,1]))==0) next
    values_f = data[grep(sprintf('%s-',gN),data[,1]), grep(eN,names(data))]
    values_b = data[grep(sprintf('%s-',gN),data[,1])*-1, grep(eN,names(data))]
    pvalues_gene[[eN]][grep(sprintf('%s-',gN),data[,1])[1]] = ks.test(c(as.matrix(values_f)),c(as.matrix(values_b)))$p.value
    fc_gene[[eN]][grep(sprintf('%s-',gN),data[,1])[1]] = mean(c(as.matrix(values_f)))
  }
}

for (gN in geneNameL){
  if (length(grep(sprintf('%s-',gN),data[,1]))==0) next
  values_f = data[grep(sprintf('%s-',gN),data[,1]), c(-1,-2)]
  values_b = data[grep(sprintf('%s-',gN),data[,1])*-1, c(-1,-2)]
  pvalues_tot[grep(sprintf('%s-',gN),data[,1])[1]] = ks.test(c(as.matrix(values_f)),c(as.matrix(values_b)))$p.value  
  fc_tot[grep(sprintf('%s-',gN),data[,1])[1]] = mean(c(as.matrix(values_f)))  
}

result = data.frame(shRNA=data[,1],ctrlCnt=ctrlCnt)

for (eN in expNameL){
  result = cbind(result, data[,grep(eN,names(data))], fc_shRNA[[eN]],pvalues_shRNA[[eN]], fc_gene[[eN]],pvalues_gene[[eN]])
}

result = cbind(result,fc_tot,pvalues_tot)

write.table(result,'/EQL6/NSL/Barcode/NY/NY_S827_stat_matrix.txt',sep='\t',quote=F,row.names=F)

result_table = matrix(nrow=0,ncol=0)

for (eN in expNameL){
  tmpTable = data.frame(shRNA=data[,1],ctrlCnt=ctrlCnt,expName=eN,fc=fc_shRNA[[eN]],pvalue=pvalues_shRNA[[eN]])
  result_table = rbind(result_table,tmpTable)
}

write.table(result_table,'/EQL6/NSL/Barcode/NY/NY_S827_stat_table.txt',sep='\t',quote=F,row.names=F)