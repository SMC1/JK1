paired_scatter <- function(
  inDirName,
  sId_p,
  graphicsFormat='png'
)
{
  
  if (graphicsFormat == 'png') {
    png(sprintf("%s/patient/paired_scatter_patient_%s.png", inDirName,sId_p))
  } else if (graphicsFormat== 'pdf') {
    pdf(sprintf("%s/patient/paired_scatter_patient_%s.pdf", inDirName,sId_p))
  }
  
  #plot.new()
  par(mfrow=c(2,2))
  par(oma=c(1,1,1,1))
  par(mar=c(3,3,2,1))
  
  for (dType in c('RPKM','CNA','mut','pathway')) {
    
    if (dType=='RPKM' || dType=='CNA') {
      df = read.table(sprintf('%s/df_paired_gene.txt',inDirName),header=T)
    } else {
      df = read.table(sprintf('%s/df_paired_%s.txt',inDirName,dType),header=T)
    }
    
    df = df[df$sId_p==sId_p,]
    
    if (dType=='RPKM' || dType=='CNA') {
      
      df = df[df$dType==dType,]
      
      if (dType=='RPKM'){
        xSta = -2
        xEnd = 12
      } else {
        xSta = -7
        xEnd = 7
      }
      
    } else if (dType=='mut') {
      
      df = df[df$p_mut>1 | df$r_mut>1,]
      df$val_p = df$p_mut / (df$p_mut + df$p_ref)
      df$val_r = df$r_mut / (df$r_mut + df$r_ref)
      
      xSta = 0
      xEnd = 1
      
    } else if (dType=='pathway') {
      
      df = df[df$dType=='PATHR',]

      xSta = -1
      xEnd = 1
    
    }
    
    df$delta = df$val_r-df$val_p
    
    if (nrow(df)>0) df$color = 'black'
#     df$color[df$geneN=='EGFR'] = 'red'
#     df$color[df$geneN=='TP53'] = 'yellow'
#     df$color[df$geneN=='IDH1'] = 'green'
#     df$color[df$geneN=='MLH1'] = 'blue'
#     df$color[df$geneN=='BRAF'] = 'grey'
#     df$color[df$geneN=='PTEN'] = 'orange'  
    
    df = df[order(-abs(df$delta)),]
    
    plot(c(xSta,xEnd),c(xSta,xEnd), type='l', pch=22, lty=2, xlim=c(xSta,xEnd), ylim=c(xSta,xEnd), axes=F,ann=F, xaxt='n',yaxt='n')
    par(new=T)
    plot(x=df$val_p, y=df$val_r, xlim=c(xSta,xEnd), ylim=c(xSta,xEnd), bg=df$color, pch=21)
    
    labelCount = min(5,nrow(df))
    if (labelCount>0)
      text(df[1:labelCount,'val_p'],df[1:labelCount,'val_r'],df[1:labelCount,'geneN'],adj=c(0,1),col='red',cex=0.6)
    
    title(sprintf('%s: %s',sId_p,dType))
  }
  
  if (graphicsFormat=='png' || graphicsFormat=='pdf') {
    dev.off()
  }
}

inDirName = '/EQL1/PrimRecur/paired'
sId_pL = c('S780','S671','S592','S437','S453','S586','S538','S567','S428','S572','S460','S458','S372','S520','S023','S042','S640','S697','S768','S577')
#sId_pL = c('S780')

for (sId_p in sId_pL) 
  for (fmt in c('png','pdf','')) paired_scatter(inDirName,sId_p,fmt)

#paired_scatter(inDirName,'S437','')