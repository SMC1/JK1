subplot <- function(X,Y,subtype,xlab,ylab) { 
  
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
  dataN,
  lab1,
  lab2,
  graphicsFormat
)
{
# geneDF = rbind(read.table(geneGctPath,sep='\t',header=T,skip=2),read.table(pathGctPath,sep='\t',header=T,skip=2))
#  
#  tmp = read.table(subtypePath,sep='\t',header=T)
#  subtypeDF = data.frame(t(tmp$Class))
#  names(subtypeDF) = lapply(tmp$sId, function(x) gsub('-','.',x))
#  subtypeDF$NAME = 'subtype'
#  subtypeDF$DESCRIPTION = ''
#  
# df = rbind(geneDF[geneDF$NAME %in% c(geneN1,geneN2),], subtypeDF)
#
#  valueL1 = as.numeric(as.vector(as.matrix(df[df$NAME==geneN1,]))[3:ncol(df)])
#  valueL2 = as.numeric(as.vector(as.matrix(df[df$NAME==geneN2,]))[3:ncol(df)])
#  subtypeL = as.numeric(as.vector(as.matrix(df[df$NAME=='subtype',]))[3:ncol(df)])

  DF = read.table('/var/www/html/tmp/correlation.txt',sep='\t',header=T)

  if (graphicsFormat=='pdf') {
    pdf(sprintf('/var/www/html/tmp/correlation.pdf'))
  } else {
    png(sprintf('/var/www/html/tmp/correlation.png'))
  }
  
  par(mfrow=c(1,1))
  par(oma=c(0,1,1,1))
  par(mar=c(3,3,3,1))
  par(mgp=c(2,1,0))
  
  #subplot(valueL1,valueL2,subtypeL,geneN1,geneN2)

  plot(DF[[2]],DF[[3]],pch=21,cex=1,xlab=sprintf('%s (%s)',names(DF)[2],lab1),ylab=sprintf('%s (%s)',names(DF)[3],lab2))
  #plot(DF[[2]],DF[[3]],pch=19,cex=1,xlab=sprintf('%s (%s)',names(DF)[2],lab1),ylab=sprintf('%s (%s)',names(DF)[3],lab2))
  t = cor.test(DF[[2]],DF[[3]])
  title(sprintf('%s: r=%.2f, p=%.1E, n=%d', dataN, t$estimate, t$p.value, nrow(DF)), cex.main=0.9)
  
  dev.off()
}

#subtypePath = '/EQL1/TCGA/GBM/TCGA_BI_subtype_num.txt'

args <- commandArgs(trailingOnly = T)

scatter(dataN=args[1],lab1=args[2],lab2=args[3],graphicsFormat=args[4])
