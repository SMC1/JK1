draw_CN_density<-function(dn, title) {
  plot(dn, main=title)
  idx<-which(diff(sign(diff(dn$y)))==-2 & dn$y[3:length(dn$x)-1]>0.01)+1
  
  if (length(idx) > 10) {
    cutoff<-max(sort(dn$y[idx],decreasing=T)[11], 0.01)
    idx<-which(diff(sign(diff(dn$y)))==-2 & dn$y[3:length(dn$x)-1]>cutoff)+1
    px<-dn$x[idx]
  } else {
    px<-dn$x[idx]
  }
  
  abline(v=px,pch=22,lty=2,col='grey')
  text(x=px,y=max(dn$y*0.9),labels=round(px,digits=3),adj=c(0,0.1),col='grey',cex=0.9,srt=90)
}

segFiles<-Sys.glob('/EQL3/pipeline/CNA/*/*seg')
for (file in unique(segFiles))
{
  sampN<-gsub(pattern='.ngCGH.seg',replacement='',x=basename(file),fixed=T)
  sId<-substr(x=sampN, start=1, stop=gregexpr(pattern='_', text=sampN, fixed=T)[[1]][1]-1)
  print(sId)
  fname<-file.path("/EQL1/NSL/WXS/results/CNA/cn_density",paste(sId,'_CN_density.pdf',sep=''))
  gname<-file.path(dirname(file),paste(sampN,'.cn_gene.dat',sep=''))
  dat<-read.table(file, sep='\t', header=T)
  g<-read.table(gname, sep='\t', header=F)
  colnames(g)<-c("sId","gene","log2")
  pdf(fname, width=15)
  par(mfrow=c(1,2))
  draw_CN_density(density(dat$seg.mean), title=paste(sId,"(segment)",sep=' '))
  draw_CN_density(density(g$log2), title=paste(sId,'(gene)',sep=' '))
  dev.off()
}
