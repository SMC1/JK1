# Multiple plot function
#
# ggplot objects can be passed in ..., or to plotlist (as a list of ggplot objects)
# - cols:   Number of columns in layout
# - layout: A matrix specifying the layout. If present, 'cols' is ignored.
#
# If the layout is something like matrix(c(1,2,3,3), nrow=2, byrow=TRUE),
# then plot 1 will go in the upper left, 2 will go in the upper right, and
# 3 will go all the way across the bottom.
#
multiplot <- function(..., plotlist=NULL, file, cols=1, layout=NULL) {
  require(grid)
  
  # Make a list from the ... arguments and plotlist
  plots <- c(list(...), plotlist)
  
  numPlots = length(plots)
  
  # If layout is NULL, then use 'cols' to determine layout
  if (is.null(layout)) {
    # Make the panel
    # ncol: Number of columns of plots
    # nrow: Number of rows needed, calculated from # of cols
    layout <- matrix(seq(1, cols * ceiling(numPlots/cols)),
                     ncol = cols, nrow = ceiling(numPlots/cols))
  }
  
  if (numPlots==1) {
    print(plots[[1]])
    
  } else {
    # Set up the page
    grid.newpage()
    pushViewport(viewport(layout = grid.layout(nrow(layout), ncol(layout))))
    
    # Make each plot, in the correct location
    for (i in 1:numPlots) {
      # Get the i,j matrix positions of the regions that contain this subplot
      matchidx <- as.data.frame(which(layout == i, arr.ind = TRUE))
      
      print(plots[[i]], vp = viewport(layout.pos.row = matchidx$row,
                                      layout.pos.col = matchidx$col))
    }
  }
}

confInterval <- function(
  vL_P,
  vL_R,
  pointEst
) 
{
  mL = c()
  for (i in 1:500) {
    mL = c(mL, pointEst(sample(vL_R,length(vL_R),replace=T)) - pointEst(sample(vL_P,length(vL_P),replace=T)))
  }
  return(quantile(mL,c(.025,.975)))
}

customBar <- function(
  df,
  pointEstN
)
{
  if (pointEstN == 'mean') {
    pointEst = mean
  } else {
    pointEst = median
  }
  
  geneNL = levels(df$geneN)
  
  c_geneN = c()
  c_dType = c()
  c_m = c()
  c_e1 = c()
  c_e2 = c()
  
  for (geneN in geneNL) {
    for (dType in c('CNA','Expr')) {
      vL_P = df[df$geneN==geneN & df$dType==dType & df$PR=='P','val']
      vL_R = df[df$geneN==geneN & df$dType==dType & df$PR=='R','val']
      e = confInterval(vL_P,vL_R,pointEst)
      c_geneN = c(c_geneN,geneN)
      c_dType = c(c_dType,sprintf('%s (n=%d,%d)',dType,length(vL_P),length(vL_R)))
      c_m = c(c_m,pointEst(pointEst(vL_R) - pointEst(vL_P)))
      c_e1 = c(c_e1,e[1])
      c_e2 = c(c_e2,e[2])
    }
  }
  
  dfplot = data.frame(geneN=c_geneN,dType=c_dType,m=c_m,e1=c_e1,e2=c_e2)
  dfplot$geneN <- factor(dfplot$geneN,geneNL)
  g <- ggplot(dfplot,aes(x=geneN,y=m,fill=dType)) + geom_bar(position="dodge", stat="identity") + geom_errorbar(aes(ymax=e2, ymin=e1), position=position_dodge(width=0.9), width=0.25) + theme(legend.position="bottom") + ylab(sprintf('%s change (log2)',pointEstN)) + ylim(-2.6,2.6) + ggtitle('TCGA unpaired')
  
  return(g)
}

unpaired_waterfall <- function(
  inDirName,
  pointEstN
)
{
  df = read.table(sprintf('%s/df_unpaired2.txt',inDirName),header=T)
  df = df[df$dbT=='TCGA-GBM',]
  
  gL <- vector(mode="list", length=2) 
  
  for (i in 1:2) {
    
    geneNL = geneNLL[[i]]
    
    df_ft = df[df$geneN %in% geneNL,]
    df_ft$geneN <- factor(df_ft$geneN[drop=T],geneNL)
    
    gL[[i]] <- customBar(df_ft,pointEstN)
  }
  
  multiplot(plotlist=gL,cols=2)
#     pval_t <- t.test(df_ftP$val,df_ftR$val)['p.value']
#     pval_r <- wilcox.test(df_ftP$val,df_ftR$val)['p.value']
#     pval_k <- ks.test(df_ftP$val,df_ftR$val)['p.value']
#     labelL[index] <- sprintf('%s\nt=%.1E\nr=%.1E\nk=%.1E',geneN,pval_t,pval_r,pval_k)
}

inDirName = '/EQL1/PrimRecur/unpaired'
geneNLL <- list(Amp=c('EGFR','CDK4','PDGFRA','MDM2','MDM4','MET','CDK6'), Del=c('CDKN2A','CDKN2B','PTEN','CDKN2C','RB1','QKI','NF1'))

# for debug: dbT='TCGA-GBM';listN='Amp'; geneNL=geneNLL[[listN]]; fmt=''; dType='Expr';geneN='EGFR'

unpaired_waterfall(inDirName,'mean')

#   for (listN in c('Amp','Del'))
#     for (dType in c('CNA','Expr','Expr'))
#       for (fmt in c('png','pdf','')) 
        
