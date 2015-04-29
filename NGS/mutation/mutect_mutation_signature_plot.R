require(ggplot2)

args<-commandArgs(trailingOnly=T)
fileN<-args[1]
outName<-args[2]

dat<-read.table(fileN, header=T, sep="\t")
id<-sub(x=basename(fileN), pattern=".mutation_signature.txt", replacement="", fixed=T)
dat$tmp<-dat$context
dat$context<-NULL
dat$context<-paste(substr(dat$tmp,1,1), substr(dat$tmp,3,3), sep="|")
dat$frac<-dat$freq/dat$n_total

pdf(outName, width=20)
p<-ggplot(dat, aes(x=context, y=frac))
p<-p+stat_bin(aes(fill=mutation))+facet_grid(~mutation)
p<-p+opts(title=id)+ylab('proportion in total mutation')
p+theme(legend.position="none",axis.text.x=element_text(angle=90),panel.grid.major.x=element_blank(), panel.background=theme_rect(fill="transparent",color=NA), panel.grid.major.y=element_line(color="black"),panel.grid.minor.y=element_blank())
dev.off()

