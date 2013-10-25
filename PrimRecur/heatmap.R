es2 = read.csv('/EQL1/PrimRecur/paired/DEG_RPKM.csv',header=T)

#pdf('/Users/jinkuk/Data/NSL/GBM_tumorSig_HM.pdf')
mat = as.matrix(es2[1:dim(es2)[1],2:dim(es2)[2]])
#heatmap.2(mat[c(1:10,(nrow(mat)-10):nrow(mat)),], col=bluered(50), breaks=seq(-2.5,2.5,.1), key=T, symkey=FALSE, density.info="none", trace="none", scale='none', cexRow=0.7, margins = c(13, 13), Rowv=FALSE, Colv=T)
heatmap.2(mat, col=bluered(30), breaks=seq(-1.5,1.5,.1), key=T, symkey=FALSE, density.info="none", trace="none", scale='none', cexRow=0.7, margins = c(13, 13), Rowv=F, Colv=T)
#dev.off()
