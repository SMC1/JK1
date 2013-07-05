library(gplots)
source('heatmap.3.R')

gene_gct <- read.table("/EQL1/TCGA/GBM/array_gene/TCGA_GBM_gene_BI_sIdClps_zNorm.gct",header=T,sep='\t',skip=2)
tgfb_sig <- rev(as.character(read.table("/data1/IRCR/JW/NRP/TGFb_Xu_proc.sig",header=T,sep='\t')$name))

indexL = c()

for (i in 1:length(tgfb_sig)) {
  indexL <- c(indexL,which(gene_gct$NAME==tgfb_sig[i]))
}

tgfb_gct <- gene_gct[indexL,]

path_gct <- read.table('/EQL1/TCGA/GBM/array_gene/TCGA_GBM_BI_pathway.gct',header=T,sep='\t',skip=2)[path_gct$NAME=='TGFb',]
path_gct$NAME <- NULL
path_gct$DESCRIPTION <- NULL
pIdL <- names(path_gct)
pIdL_sorted <-pIdL[order(as.vector(path_gct[1,]))]

tgfb_gct = tgfb_gct[,pIdL_sorted]

tgfbL = bluered(201)[round(t(as.matrix(path_gct[1,pIdL_sorted]))*100+101)]

nrp1_gct <- gene_gct[gene_gct$NAME=='NRP1',pIdL_sorted]
nrp1L = bluered(9)[round(t(as.matrix(nrp1_gct))*2+5)]

sema3a_gct <- gene_gct[gene_gct$NAME=='SEMA3A',pIdL_sorted]
sema3aL = bluered(9)[round(t(as.matrix(sema3a_gct))*2+5)]

subtypeDF = read.table('/EQL1/TCGA/GBM/TCGA_BI_subtype_num.txt',sep='\t',header=T)

subtypeL = c()

for (i in 1:ncol(tgfb_gct)) {
  subtypeL <- c(subtypeL,subtypeDF[gsub('-','.',subtypeDF$sId)==names(tgfb_gct)[i],'Class'])
}

subtypeL[subtypeL==1] <- 'red'
subtypeL[subtypeL==2] <- 'orange'
subtypeL[subtypeL==3] <- 'green'
subtypeL[subtypeL==4] <- 'blue'
subtypeL[subtypeL==5] <- 'grey'

par(mfrow=c(1,1))
par(oma=c(0,0,0,0))
par(mar=c(0,0,0,0))
par(mgp=c(2,1,0))

subtypeL <- t(t(subtypeL))
colSideM = cbind(tgfbL,sema3aL,nrp1L,subtypeL)
colnames(colSideM) <- c('TGFb','SEMA3A','NRP1','Subtype')

heatmap.3(as.matrix(tgfb_gct[,1:ncol(tgfb_gct)]), col=bluered(9), key=F, symkey=F, ColSideColors=colSideM, NumColSideColors=3, margins=c(2,2), density.info="none", trace="none", cexRow=0.7, dendrogram='none', Rowv=FALSE, Colv=FALSE, labRow=F, labCol=F, scale='none')