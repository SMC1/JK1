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
  vL,
  pointEst
) 
{
  mL = c()
  for (i in 1:500) {
    mL = c(mL,pointEst(sample(vL,length(vL),replace=T)))
  }
  return(quantile(mL,c(.025,.975)))
}

customBar <- function(
  df,
  pointEstN
)
{
  if (pointEstN == 'mean') pointEst = mean
  else pointEst = median
  
  geneNL = levels(df$geneN)
  
  c_geneN = c()
  c_dType = c()
  c_m = c()
  c_e1 = c()
  c_e2 = c()
  
  for (geneN in geneNL) {
    for (dType in c('RPKM')) {
      vL = df[df$geneN==geneN & df$dType==dType,'val_diff']
      m = pointEst(vL)
      e = confInterval(vL,pointEst)
      c_geneN = c(c_geneN,geneN)
      c_dType = c(c_dType,sprintf('%s (n=%d)',dType,length(vL)))
      c_m = c(c_m,m)
      c_e1 = c(c_e1,e[1])
      c_e2 = c(c_e2,e[2])
    }
  }
  
  dfplot = data.frame(geneN=c_geneN,dType=c_dType,m=c_m,e1=c_e1,e2=c_e2)
  dfplot$geneN <- factor(dfplot$geneN,geneNL)
  g <- ggplot(dfplot,aes(x=geneN,y=m,fill=dType)) + geom_bar(position="dodge", stat="identity") + geom_errorbar(aes(ymax=e2, ymin=e1), position=position_dodge(width=0.9), width=0.25) + theme(axis.text.x=element_text(angle=90,vjust=1),legend.position="bottom") + ylab(sprintf('%s change (log2)',pointEstN)) + ylim(-2.7,2.7) + ggtitle(sprintf('%s paired',dbN))

  return(g)
}

paired_box <- function(
  inDirName,
  pointEstN,
  graphicsFormat='png',
  dbN,
  idh1
)
{
#   if (graphicsFormat == 'png') {
#     png(sprintf("%s/box/paired_box_%s_%s.png", inDirName,listN,dType))
#   } else if (graphicsFormat== 'pdf') {
#     pdf(sprintf("%s/box/paired_box_%s_%s.pdf", inDirName,listN,dType))
#   }
  
#  df = read.table(sprintf('%s/df_sel2.txt',inDirName),header=TRUE)
  df = read.table(sprintf('%s/df_paired_gene.txt',inDirName),header=TRUE)
  df$val_diff = df$val_r - df$val_p
  
  gL <- vector(mode="list", length=2) 

  for (i in 1:2) {
    
    geneNL = geneNLL[[i]]

	if (idh1 == T) { 
    df_ft = df[df$geneN %in% geneNL & df$sId_p %in% IDH1,]
    } else {
	df_ft = df[df$geneN %in% geneNL,]
    }
	df_ft$geneN <- factor(df_ft$geneN[drop=TRUE],geneNL)
    
    gL[[i]] <- customBar(df_ft,pointEstN)
    
    #  n = length(df_ft_ch)/length(geneNL)
    #  radius=max(abs(floor(min(df_ft_ch))), abs(ceiling(max(df_ft_ch))))  
    #boxplot(df_ft_ch ~ df_ft$geneN, ylim=c(-radius,radius), ylab=sprintf('Change in %s',lab), axes=F, cex.axis=0.6, cex=0.5, main=sprintf('%s, %s gene P->R change (n=%d)',dType,listN,n))
    #stripchart(df_ft_ch ~ df_ft$geneN, vertical=T, add=T, pch=1, ylim=c(-radius,radius), cex=0.5)
    #   abline(h=0,pch=22,lty=2)
    #   
    #   labelL <- geneNL
    #   
    #   for (geneN in geneNL){
    #     df_ft2 <- df_ft[df_ft$geneN==geneN,]
    #     pval_t <- t.test(df_ft2$val_r-df_ft2$val_p)['p.value']
    #     pval_r <- wilcox.test(df_ft2$val_r-df_ft2$val_p)['p.value']
    #     labelL[labelL==geneN] <- sprintf('%s\nm=%.2f\nt=%.1E\nr=%.1E',geneN,mean(df_ft2$val_r-df_ft2$val_p),pval_t,pval_r)
    #   }

  }
  
  multiplot(plotlist=gL,cols=2)
  
#   if (graphicsFormat=='png' || graphicsFormat=='pdf'){    
#     dev.off()
#   }
  
}

library(ggplot2)

#inDirName = '/EQL1/Phillips/paired' #'/EQL1/PrimRecur/paired'
inDirName = '/EQL2/SGI_20131031/RNASeq/results'
geneNLL <- list(Amp=c('EGFR','CDK4','PDGFRA','MDM2','MDM4','MET','CDK6'), Del=c('CDKN2A','CDKN2B','PTEN','CDKN2C','RB1','QKI','NF1'))
IDH1 <- c('S453','S586','S428','S372','S042')
noIDH1 <- c('S567','S780','S592','S437','S538','S460','S572','S458','S640','S697','S768','S023')
#dbN <- 'Phillips'
dbN <- 'ircr1'

# for debug: 
# geneNL=geneNLL[['Del']]; graphicsFormat=''

# for (fmt in c('png','pdf',''))
paired_box(inDirName,pointEstN='mean',graphicsFormat='',dbN,idh1=F)
