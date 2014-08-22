library(ggplot2)
library(gridExtra)

inDirName = '/data1/IRCR/352'

df = read.table(sprintf('%s/EGFR_cn_rppa.txt',inDirName),header=TRUE)

df$phospho <- pmax(df$Y1068,df$Y1173,df$Y992)
df$group <- '1'
#df$group[df$cn>1] <- '2'
df$group[df$cn>3] <- '3'

#par(mfrow=c(1,1))
#par(oma=c(1,1,1,0), mar=c(4,3,2,2),mgp=c(2,1,0))
#plot(df$cn_log2,df$phospho)

#ggplot(df,aes(cn_log2,phospho))  + geom_point() + geom_rug(col="darkred",alpha=.1)

xvar <- df$cn_log2
yvar <- df$phospho
zvar <- df$group
xy <- df

#placeholder plot - prints nothing at all
empty <- ggplot()+geom_point(aes(1,1), colour="white") +
  theme(                              
    plot.background = element_blank(), 
    panel.grid.major = element_blank(), 
    panel.grid.minor = element_blank(), 
    panel.border = element_blank(), 
    panel.background = element_blank(),
    axis.title.x = element_blank(),
    axis.title.y = element_blank(),
    axis.text.x = element_blank(),
    axis.text.y = element_blank(),
    axis.ticks = element_blank()
  )

#scatterplot of x and y variables
scatter <- ggplot(xy,aes(xvar, yvar)) + 
  geom_point(aes(color=zvar)) + 
  #scale_color_manual(values = c("orange", "purple", "red")) + 
  scale_color_manual(values = c("orange", "red")) + 
  theme(legend.position=c(1,1),legend.justification=c(1,1)) 

#marginal density of x - plot on top
plot_top <- ggplot(xy, aes(xvar, fill=zvar)) + 
  geom_density(alpha=.5) + 
  #scale_fill_manual(values = c("orange", "purple", "red")) + 
  scale_fill_manual(values = c("orange", "red")) + 
  theme(legend.position = "none")

#marginal density of y - plot on the right
plot_right <- ggplot(xy, aes(yvar, fill=zvar)) + 
  geom_density(alpha=.5) + 
  coord_flip() + 
  #scale_fill_manual(values = c("orange", "purple", "red")) + 
  scale_fill_manual(values = c("orange", "red")) + 
  theme(legend.position = "none") 

#arrange the plots together, with appropriate height and width for each row and column
grid.arrange(plot_top, empty, scatter, plot_right, ncol=2, nrow=2, widths=c(4, 1), heights=c(1, 4))