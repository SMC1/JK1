test <- function(
  inFileName,
  outFileName,
  plot,
  outPlotDirName,
  type
  ) {
  
  df = read.delim(inFileName)
  
  print("--------------------------------------")
  print(as.character(df$Gene[1]))
  
  drugNameL = unique(df$Drug)
  
  for (drug in drugNameL) {
    df_ft = df[df$Drug == drug & !is.na(df$AUC) & df$db_id != '',]
    df_ft = df_ft[order(df_ft$AUC),]
    
    auc_z = scale(df_ft$AUC)
    df_ft$AUC_Z = auc_z
    
    if (TRUE %in% !is.na(df_ft$Alt)){
      
      df_ft$group = 'WT'
      df_ft$group[!is.na(df_ft$Alt)]='Alt'
      w_p = round(wilcox.test(df_ft$AUC~df_ft$group)$p.value,4)
      if (sum(df_ft$group=='Alt')>1 & sum(df_ft$group!='Alt')>1) {
        t_p = round(t.test(df_ft$AUC~df_ft$group)$p.value,4)
      } else {
        t_p = NA
      }
      
      t = nrow(df_ft)
      m = which(!is.na(df_ft[,"Alt"]))
      value = m/t
      
      z_med_alt = median(df_ft$AUC_Z[m])
      z_mean_alt = mean(df_ft$AUC_Z[m])
      
      p_two= ks.test(value,"punif",alternative="two.sided")$p.value
      d= ks.test(value,"punif",alternative="two.sided")$stat
      p_two2= ks.test(df_ft$AUC[m],"punif",alternative="two.sided",min(df_ft$AUC),max(df_ft$AUC))$p.value
      d2= ks.test(df_ft$AUC[m],"punif",alternative="two.sided",min(df_ft$AUC),max(df_ft$AUC))$stat
      p_g = ks.test(value,"punif",alternative="g")$p.value
      p_l = ks.test(value,"punif",alternative="l")$p.value
      wt_n = t-length(m)
      mut_n = length(m)
      mut_sampn = length(unique(df_ft[m,"db_id"]))
      wt_sampn = length(unique(df_ft$db_id)) - mut_sampn
      
      altinfo = paste(df_ft$db_id[df_ft$group=="Alt"],df_ft$Alt[df_ft$group=="Alt"],sep=":",collapse=",")
      
      write(sprintf('%s\t%s\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%s\t%s\t%s\t%s\t%s\t%s\t%.4f\t%.4f\t%s',
                    drug,df_ft$Gene[1],p_two,p_g,p_l,d,p_two2,d2,wt_n,mut_n,wt_sampn,mut_sampn,w_p,t_p,z_med_alt,z_mean_alt,altinfo),
            file=outFileName,append=T)
      
      if (plot == T) {
        addlab = as.character(df_ft$db_id)
        outFilePrefix = strsplit(rev(strsplit(outFileName,"/")[[1]])[1],".txt")[[1]]
        outFilePrefix = sprintf("%s/%s",outPlotDirName,outFilePrefix)
        pdf(sprintf("%s_%s_%s.pdf",outFilePrefix,df_ft$Gene[1],drug),useDingbats=F,width=5)
        df_ft[df_ft$group=="Alt","group"] = as.character(df_ft$Gene[1])
        group = factor(df_ft$group,levels=c(as.character(df_ft$Gene[1]),'WT'))
        #boxplot(df_ft$AUC~group,main=sprintf("%s",drug),add=F,ylab=sprintf('%s',type))
        boxplot(df_ft$AUC~group,main=sprintf("%s (p-value:%.2e)",drug,w_p),add=F,ylab=expression(bold("Area Under Curve")),boxwex=.5,
                boxlwd=3,whisklwd=3,staplelwd=3,outlwd=3,frame.plot=F,medlwd=5,axes=F,outcol=NA)
        box(lwd=3)
        axis(side=2,font=2,lwd=3) 
        axis(side=1,font=2,lwd=3,at=1:length(unique(group)),labels=levels(group))
        stripchart(df_ft$AUC~group,vertical = TRUE, pch=16,method = "jitter",add=T,col=c("black","black"))
        #for (i in 1:nrow(df_ft)){
        #text(group[i],df_ft$AUC[i],label=addlab[i],cex=.6, adj=1,pos=4)
        #}
        dev.off()
      }
      
    }
  }
}

#suppressWarnings(warning("Setting"))

args <- commandArgs(TRUE)

inFileName = args[1]
outFileName = args[2]
plot = args[3]
outPlotDirName = args[4]
type = args[5]

test(inFileName,outFileName,plot,outPlotDirName,type)
