scatter <- function(
  geneGctPath,
  pathGctPath,
  geneL,
  pathL,
  dsetN
)
{
  
  isPdf = F
  
  geneDF = read.table(geneGctPath,sep='\t',header=T,skip=2)
  pathDF = read.table(pathGctPath,sep='\t',header=T,skip=2)

  df = rbind(geneDF[geneDF$NAME %in% geneL,], pathDF[pathDF$NAME %in% pathL,])

  DRD2=as.numeric(as.vector(as.matrix(df[df$NAME=='DRD2',]))[3:ncol(df)])
  TH=as.numeric(as.vector(as.matrix(df[df$NAME=='TH',]))[3:ncol(df)])
  TGFb=as.numeric(as.vector(as.matrix(df[df$NAME=='TGF-beta',]))[3:ncol(df)]) * -1
  
  if (isPdf) pdf(sprintf('/data1/IRCR/JW/Dopamine/%s_scatter1.pdf',dsetN))
  
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
  
  plot(DRD2,TGFb,cex=0.5)
  f = lm(TGFb ~ DRD2)
  y = as.numeric(f$coefficient['(Intercept)'])
  a = as.numeric(f$coefficient['DRD2'])
  TGFb_DRD2 = TGFb - (DRD2*a+y)
  t = cor.test(DRD2,TGFb)
  title(sprintf('r=%.2f, p=%.1E, a=%.3f', t$estimate, t$p.value,a),cex.main=0.8)
  abline(f)
  
  plot(TH,TGFb,cex=0.5)
  f = lm(TGFb ~ TH)
  y = as.numeric(f$coefficient['(Intercept)'])
  a = as.numeric(f$coefficient['TH'])
  TGFb_TH = TGFb - (TH*a+y)
  t = cor.test(TH,TGFb)
  title(sprintf('r=%.2f, p=%.1E, a=%.3f', t$estimate, t$p.value,a),cex.main=0.8)
  abline(f)
  
  plot(DRD2,TGFb_TH,cex=0.5)
  t = cor.test(DRD2,TGFb_TH)
  f = lm(TGFb_TH ~ DRD2)
  y = as.numeric(f$coefficient['(Intercept)'])
  a = as.numeric(f$coefficient['DRD2'])
  title(sprintf('r=%.2f, p=%.1E, a=%.3f', t$estimate, t$p.value,a),cex.main=0.8)
  abline(f)

  plot(TH,TGFb_DRD2,cex=0.5)
  t = cor.test(TH,TGFb_DRD2)
  f = lm(TGFb_DRD2 ~ TH)
  y = as.numeric(f$coefficient['(Intercept)'])
  a = as.numeric(f$coefficient['TH'])
  title(sprintf('r=%.2f, p=%.1E, a=%.3f', t$estimate, t$p.value,a),cex.main=0.8)
  abline(f)
  
  if (isPdf) dev.off()
  
  if (isPdf) pdf(sprintf('/data1/IRCR/JW/Dopamine/%s_scatter2.pdf',dsetN))
  
  par(mfrow=c(1,1))
  #plot(DRD2,TH,pch=21,bg=colCode)
  plot(DRD2,TH,pch=21)
  t = cor.test(DRD2,TH)
  title(sprintf('DRD2-TH: r=%.2f, p=%.1E', t$estimate, t$p.value), cex.main=0.9)
  
  if (isPdf) dev.off()
  
  if (isPdf) pdf(sprintf('/data1/IRCR/JW/Dopamine/%s_scatter3.pdf',dsetN))
  
  par(mfrow=c(1,1))
  s3d <- scatterplot3d(DRD2,TH,TGFb,pch=19,color=colCode)
  par(new=T)
  s3d <- scatterplot3d(DRD2,TH,TGFb,pch=21,lty.hplot=2,axis=F)
  fit <- lm(TGFb ~ DRD2+TH) 
  s3d$plane3d(fit)
  
  if (isPdf) dev.off()
  
}

library(scatterplot3d)

# dsetN = 'Avatar'
# geneGctPath = '/EQL1/NSL/array_gene/NSL_GBM_93.gct'
# pathGctPath = '/EQL1/NSL/array_gene/NSL_GBM_93_pathway_NTP.gct'

dsetN = 'TCGA-GBM'
geneGctPath = '/EQL1/TCGA/GBM/array_gene/TCGA_GBM_gene_BI_sIdClps.gct'
pathGctPath = '/EQL1/TCGA/GBM/array_gene/TCGA_GBM_BI_pathway.gct'

geneL=c('EGFR','MGMT')
pathL=c('TGF-beta')

scatter(geneGctPath=geneGctPath, pathGctPath=pathGctPath, geneL, pathL, dsetN)