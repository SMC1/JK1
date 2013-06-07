scatter <- function(
  geneGctPath,
  pathGctPath,
  geneL,
  pathL,
  dsetN
)
{
  
  isPdf = T
  
  geneDF = read.table(geneGctPath,sep='\t',header=T,skip=2)
  pathDF = read.table(pathGctPath,sep='\t',header=T,skip=2)

  df = rbind(geneDF[geneDF$NAME %in% geneL,], pathDF[pathDF$NAME %in% pathL,])

  NRP1=as.numeric(as.vector(as.matrix(df[df$NAME=='NRP1',]))[3:ncol(df)])
  SEMA3A=as.numeric(as.vector(as.matrix(df[df$NAME=='SEMA3A',]))[3:ncol(df)])
  TGFb=as.numeric(as.vector(as.matrix(df[df$NAME=='TGF-beta',]))[3:ncol(df)]) * -1
  
  if (isPdf) pdf(sprintf('/data1/IRCR/JW/NRP/%s_scatter1.pdf',dsetN))
  
  par(mfrow=c(2,2))
  par(oma=c(0,1,1,1))
  par(mar=c(3,3,3,1))
  par(mgp=c(2,1,0))
  
  colCode = rep(0,length(TGFb))
  colAmp = round((1- abs(TGFb/max(abs(TGFb)))) *255)
    
  for (i in 1:length(TGFb)) {
    if (TGFb[i]>=0) colCode[i] = sprintf('#ff%02x%02x',colAmp[i],colAmp[i])
    else colCode[i] = sprintf('#%02x%02xff',colAmp[i],colAmp[i])
  }
  
  plot(NRP1,TGFb,cex=0.5)
  f = lm(TGFb ~ NRP1)
  y = as.numeric(f$coefficient['(Intercept)'])
  a = as.numeric(f$coefficient['NRP1'])
  TGFb_NRP1 = TGFb - (NRP1*a+y)
  t = cor.test(NRP1,TGFb)
  title(sprintf('r=%.2f, p=%.1E, a=%.3f', t$estimate, t$p.value,a),cex.main=0.8)
  abline(f)
  
  plot(SEMA3A,TGFb,cex=0.5)
  f = lm(TGFb ~ SEMA3A)
  y = as.numeric(f$coefficient['(Intercept)'])
  a = as.numeric(f$coefficient['SEMA3A'])
  TGFb_SEMA3A = TGFb - (SEMA3A*a+y)
  t = cor.test(SEMA3A,TGFb)
  title(sprintf('r=%.2f, p=%.1E, a=%.3f', t$estimate, t$p.value,a),cex.main=0.8)
  abline(f)
  
  plot(NRP1,TGFb_SEMA3A,cex=0.5)
  t = cor.test(NRP1,TGFb_SEMA3A)
  f = lm(TGFb_SEMA3A ~ NRP1)
  y = as.numeric(f$coefficient['(Intercept)'])
  a = as.numeric(f$coefficient['NRP1'])
  title(sprintf('r=%.2f, p=%.1E, a=%.3f', t$estimate, t$p.value,a),cex.main=0.8)
  abline(f)

  plot(SEMA3A,TGFb_NRP1,cex=0.5)
  t = cor.test(SEMA3A,TGFb_NRP1)
  f = lm(TGFb_NRP1 ~ SEMA3A)
  y = as.numeric(f$coefficient['(Intercept)'])
  a = as.numeric(f$coefficient['SEMA3A'])
  title(sprintf('r=%.2f, p=%.1E, a=%.3f', t$estimate, t$p.value,a),cex.main=0.8)
  abline(f)
  
  if (isPdf) dev.off()
  
  if (isPdf) pdf(sprintf('/data1/IRCR/JW/NRP/%s_scatter2.pdf',dsetN))
  
  par(mfrow=c(1,1))
  plot(NRP1,SEMA3A,pch=21,bg=colCode)
  t = cor.test(NRP1,SEMA3A)
  title(sprintf('NRP1-SEMA3A: r=%.2f, p=%.1E', t$estimate, t$p.value), cex.main=0.9)
  
  if (isPdf) dev.off()
  
  if (isPdf) pdf(sprintf('/data1/IRCR/JW/NRP/%s_scatter3.pdf',dsetN))
  
  par(mfrow=c(1,1))
  s3d <- scatterplot3d(NRP1,SEMA3A,TGFb,pch=19,color=colCode)
  par(new=T)
  s3d <- scatterplot3d(NRP1,SEMA3A,TGFb,pch=21,lty.hplot=2,axis=F)
  fit <- lm(TGFb ~ NRP1+SEMA3A) 
  s3d$plane3d(fit)
  
  if (isPdf) dev.off()
  
}

library(scatterplot3d)

# dsetN = 'Avatar'
# geneGctPath = '/EQL1/NSL/array_gene/NSL_GBM_93.gct'
# pathGctPath = '/EQL1/NSL/array_gene/NSL_GBM_93_pathway_NTP.gct'

dsetN = 'TCGA-GBM'
geneGctPath = '/EQL1/TCGA/GBM/array_gene/TCGA_GBM_gene_BI_sIdClps.gct'
pathGctPath = '/EQL1/TCGA/GBM/array_gene/TCGA_GBM_gene_BI_pathway.gct'

geneL=c('NRP1','SEMA3A')
pathL=c('TGF-beta')

scatter(geneGctPath=geneGctPath, pathGctPath=pathGctPath, geneL, pathL, dsetN)