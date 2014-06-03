subplot <- function(X,Y,subtype,xlab,ylab){ 
  
  subtypeName = c('P','N','C','M','U')
  subtypeColor = c('red','orange','green','blue','grey')

  plot(X,Y,cex=0.5,col='white',xlab=xlab,ylab=ylab)
  
  f = lm(Y ~ X)
  g_a = as.numeric(f$coefficient['X'])
  g_t = cor.test(X,Y)
  
  txt = sprintf('ALL r=%.2f, p=%.1E, a=%.2f, n=%d', g_t$estimate, g_t$p.value, g_a, length(X))
  
  for (i in c(5,1,2,3,4)) {
    par(new=T)
    plot(X[subtype==i],Y[subtype==i],cex=0.5,col=subtypeColor[i],xlim=c(min(X),max(X)),ylim=c(min(Y),max(Y)),axes=F,ann=F)
    f = lm(Y[subtype==i] ~ X[subtype==i])
    a = as.numeric(f$coefficient[2])
    t = cor.test(X[subtype==i],Y[subtype==i])    
    abline(f,col=subtypeColor[i])
    txt = paste(txt,sprintf('%s r=%.2f, p=%.1E, a=%.2f, n=%d', subtypeName[i], t$estimate, t$p.value, a, length(X[subtype==i])),sep="\n")
  }

  mtext(txt,side=3,cex=0.5)
}

scatter <- function(
  geneGctPath,
  pathGctPath,
  subtypePath,
  geneL,
  pathL,
  dsetN
)
{
  
  isPdf = F
  
  geneDF = read.table(geneGctPath,sep='\t',header=T,skip=2)
  pathDF = read.table(pathGctPath,sep='\t',header=T,skip=2)
  
  tmp = read.table(subtypePath,sep='\t',header=T)
  subtypeDF = data.frame(t(tmp$Class))
  names(subtypeDF) = lapply(tmp$sId, function(x) gsub('-','.',x))
  subtypeDF$NAME = 'subtype'
  subtypeDF$DESCRIPTION = ''
  
  df = rbind(geneDF[geneDF$NAME %in% geneL,], pathDF[pathDF$NAME %in% pathL,], subtypeDF)

  NRP1=as.numeric(as.vector(as.matrix(df[df$NAME=='NRP1',]))[3:ncol(df)])
  SEMA3A=as.numeric(as.vector(as.matrix(df[df$NAME=='SEMA3A',]))[3:ncol(df)])
  TGFb=as.numeric(as.vector(as.matrix(df[df$NAME=='TGFb',]))[3:ncol(df)])
  subtype=as.numeric(as.vector(as.matrix(df[df$NAME=='subtype',]))[3:ncol(df)])

  f = lm(TGFb ~ NRP1)
  y = as.numeric(f$coefficient[1])
  a = as.numeric(f$coefficient[2])
  
  f = lm(TGFb ~ SEMA3A)
  y = as.numeric(f$coefficient[1])
  a = as.numeric(f$coefficient[2])
  
  if (isPdf) pdf(sprintf('/data1/IRCR/JW/NRP/SEMA3A/%s_scatter_subtype.pdf',dsetN))
  
  par(mfrow=c(1,1))
  par(oma=c(0,1,1,1))
  par(mar=c(3,3,3,1))
  par(mgp=c(2,1,0))
  
  subplot(NRP1,SEMA3A,subtype,'NRP1','SEMA3A')

#   plot(NRP1,SEMA3A,pch=21,bg=colCode)
#   t = cor.test(NRP1,SEMA3A)
#   title(sprintf('NRP1-SEMA3A: r=%.2f, p=%.1E', t$estimate, t$p.value), cex.main=0.9)
  
  if (isPdf) dev.off()
}

dsetN = 'TCGA-GBM'
geneGctPath = '/EQL1/TCGA/GBM/array_gene/TCGA_GBM_gene_BI_sIdClps.gct'
pathGctPath = '/EQL1/TCGA/GBM/array_gene/TCGA_GBM_BI_pathway.gct'
subtypePath = '/EQL1/TCGA/GBM/TCGA_BI_subtype_num.txt'

geneL=c('NRP1','SEMA3A')
pathL=c('TGFb')

scatter(geneGctPath=geneGctPath, pathGctPath=pathGctPath, subtypePath=subtypePath, geneL, pathL, dsetN)