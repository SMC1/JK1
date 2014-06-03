paired_scatter <- function(
  inDirName,
  sId_p,
  graphicsFormat='png'
)
{
  
  if (graphicsFormat == 'png') {
    png(sprintf("%s/timescale/paired_timescale_%s.png", inDirName,sId_p))
  } else if (graphicsFormat== 'pdf') {
    pdf(sprintf("%s/timescale/paired_timescale_%s.pdf", inDirName,sId_p))
  }
  
  par(mfcol=c(2,1))
  par(oma=c(1,1,1,1))
  par(mar=c(3,3,2,1))
  
  rng = c(0,0)
  
  for (dType in c('RPKM','mut')) {
    
    if (dType=='RPKM' || dType=='CNA') {
      df = read.table(sprintf('%s/df_paired_gene.txt',inDirName),header=T)
    } else {
      df = read.table(sprintf('%s/df_paired_%s.txt',inDirName,dType),header=T)
    }
    
    df = df[df$sId_p==sId_p,]
    
    if (dType=='RPKM') {
      
      df = df[df$dType==dType,]
      rng = c(-2,2)
      
    } else if (dType=='mut') {
      
      df = df[df$p_mut>1 | df$r_mut>1,]
      df$val_p = df$p_mut / (df$p_mut + df$p_ref)
      df$val_r = df$r_mut / (df$r_mut + df$r_ref)
      
      rng = c(0,1)      
    }
    
    df$delta = df$val_r-df$val_p
    
    if (nrow(df)>0) df$color = 'black'
    df$color[df$geneN=='EGFR'] = 'red'
    df$color[df$geneN=='TP53'] = 'yellow'
    df$color[df$geneN=='IDH1'] = 'green'
    df$color[df$geneN=='MLH1'] = 'blue'
    df$color[df$geneN=='BRAF'] = 'grey'
    df$color[df$geneN=='PTEN'] = 'orange'  
    
    df = df[order(-abs(df$delta)),]
    
    for (geneN in geneNL) {
      if (dType=='RPKM') {
        d=df$delta[df$geneN==geneN][1]
        plot(c(0,1),c(0,d),type='l',xlim=c(0,1),ylim=rng,axes=F,ann=F)
        text(min(1,rng[2]/abs(d)),min(abs(d),rng[2])*sign(d),geneN,adj=c(1,1),col='red',cex=0.6)
      } else if (dType=='mut') {
        plot(c(0,1),c(df$val_p[df$geneN==geneN][1],df$val_r[df$geneN==geneN][1]),type='l',xlim=c(0,1),ylim=rng,axes=F,ann=F)
        text(1,df$val_r[df$geneN==geneN][1],geneN,adj=c(1,1),col='red',cex=0.6)        
      }
      par(new=T)
    }
    
    plot(1,type='n',xlim=c(0,1),ylim=rng)
    
    title(sprintf('%s: %s',sId_p,dType))
  }  
  
  if (graphicsFormat=='png' || graphicsFormat=='pdf')
    dev.off()
}

inDirName = '/EQL1/PrimRecur/paired'
#sId_pL = c('S780','S671','S592','S437','S453','S586','S538','S567','S428','S572','S460','S458','S372','S520','S023','S042','S640','S697','S768','S577','S096')
sId_pL = c('S437')

geneNL = c('CDK4','CDK6','MET','RB1','EGFR','PTEN','IDH1','APC','TP53')

for (sId_p in sId_pL)
  for (fmt in c('png','pdf','')) paired_scatter(inDirName,sId_p,fmt)