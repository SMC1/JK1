data = read.table("/EQL6/NSL/Barcode/NY/pooled_screeen_2.txt",sep='\t',header=T)
colTot = colSums(data[,-1])
data = data[data[,2]>=1000,]

for (i in 1:nrow(data)){
  data[i,-1] = data[i,-1]/colTot
}

for (i in 3:ncol(data)){
  data[,i] = data[,i]/data[,2]
}

data[,-1] = log2(data[,-1])

geneNameL = c('BTG3','CTNNB1','DDAH1','DDX6','FBXW7','GNG10','HERPUD1','KIF11','KRIT1','MAPK14','MDM2','MGC16025','MYC','MYD88','NSC','P4HTM','PRMT7','PRTG','RFX7','RRM1','SLC10A5','TGFB1','TP53','WEE1','ZNF649')
expNameL = c('G2','G3','G4','G5')

pvalues_shRNA = data.frame(matrix(nrow=nrow(data),ncol=length(expNameL)))
names(pvalues_shRNA) = expNameL

pvalues_gene = data.frame(matrix(nrow=nrow(data),ncol=length(expNameL)))
names(pvalues_gene) = expNameL

pvalues_tot = matrix(nrow=nrow(data),ncol=1)

for (i in 1:nrow(data)){
  for (eN in expNameL){
    values_f = data[i, grep(eN,names(data))]
    values_b = data[grep(sprintf('%s-',gN),data[,1])*-1, grep(eN,names(data))]
    pvalues_shRNA[[eN]][i]=ks.test(values_f,as.matrix(values_b))$p.value
  }
}

for (gN in geneNameL){
  for (eN in expNameL){
    if (length(grep(sprintf('%s-',gN),data[,1]))==0) next
    values_f = data[grep(sprintf('%s-',gN),data[,1]), grep(eN,names(data))]
    values_b = data[grep(sprintf('%s-',gN),data[,1])*-1, grep(eN,names(data))]
    pvalues_gene[[eN]][grep(sprintf('%s-',gN),data[,1])[1]] = ks.test(values_f,as.matrix(values_b))$p.value
  }
}

for (gN in geneNameL){
  if (length(grep(sprintf('%s-',gN),data[,1]))==0) next
  values_f = data[grep(sprintf('%s-',gN),data[,1]), c(-1,-2)]
  values_b = data[grep(sprintf('%s-',gN),data[,1])*-1, c(-1,-2)]
  pvalues_tot[grep(sprintf('%s-',gN),data[,1])[1]] = ks.test(values_f,as.matrix(values_b))$p.value  
}

result = data[,1]

for (eN in expNameL){
  result = cbind(result,data[,grep(eN,names(data))],pvalues_shRNA[[eN]],pvalues_gene[[eN]])
}

result = cbind(result,pvalues_tot)

write.table(result,'/EQL6/NSL/Barcode/NY/pooled_screeen_2_pvalue.txt',sep='\t',quote=F,row.names=F)