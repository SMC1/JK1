
args<-commandArgs(trailingOnly=T)
pid<-args[1]
rid<-args[2]

dir='/EQL3/pipeline/somatic_mutation/'
postfix='.mutation_signature.txt'
p_name<-paste(dir,pid,'/',pid,postfix, sep='')
r_name<-paste(dir,rid,'/',rid,postfix, sep='')
p_data<-read.table(p_name, sep="\t", header=T)
r_data<-read.table(r_name, sep="\t", header=T)
p_data$frac<-p_data$freq/p_data$n_total
r_data$frac<-r_data$freq/r_data$n_total
d_name<-paste(dir,rid,'/',rid,'.mutation_signature_diff.txt', sep='')
d_data<-read.table(d_name, sep="\t", header=T)

p_data<-p_data[,c("samp_id","mutation","context","frac")]
r_data<-r_data[,c("samp_id","mutation","context","frac")]
d_data$samp_id<-"Delta fraction (R-P)"
diff<-d_data[,c("samp_id","mutation", "context","delta")]
colnames(diff)<-colnames(p_data)

dat<-rbind(p_data, r_data, diff)
dat$lab<-paste(substr(dat$context,1,1), substr(dat$context,3,3), sep="|")

require(ggplot2)
outName<-paste(dir,rid,'/',rid,'.mutation_signature_diff.pdf', sep='')
pdf(outName, height=15, width=25)
p<-ggplot(dat, aes(x=lab, y=frac))
p<-p+stat_bin(aes(fill=mutation))+facet_grid(samp_id ~ mutation)
p<-p+ylab('Proportion in total mutation')+xlab('Mutation context')
p+ylim(-0.15,0.15)+theme(legend.position="none", axis.text.x=element_text(angle=90), panel.grid.major.x=element_blank(), panel.background=theme_rect(fill="transparent", color=NA), panel.grid.major.y=element_line(color="black"), panel.grid.minor.y=element_blank())
dev.off()