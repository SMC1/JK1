test <- function(
  inFileName,
  outFileName,
  plot,
  outPlotDirName,
  type
  ) {
  sId=c('592T', '626T', '723T', '775T', 'GBM13_235T', 'GBM13_352T1', 'GBM13_352T2', 'GBM14_458T_M2', 'GBM14_485T1_M2', 'GBM14_487T_M3', 'GBM14_497T_M3', 
        'GBM14_499T1_M3', 'GBM14_500T_M8', 'GBM14_503T_M3', 'GBM14_504T3_M3', 'GBM14_508T_M8', 'GBM14_524T_M3', 'GBM14_526T', 'GBM14_527T2', 'GBM14_529T', 
        'GBM14_534T', 'GBM14_541T', 'GBM14_542T', 'GBM14_543T', 'GBM14_544T', 'GBM14_549T1_M8', 'GBM14_554T_M8', 'GBM14_559T1', 'GBM14_559T2', 'GBM14_565T', 
        'GBM14_569T', 'GBM14_570T1', 'GBM14_570T2_M8', 'GBM14_571T', 'GBM14_574T', 'GBM14_576T', 'GBM14_586T_M8', 'GBM14_588T_M8', 'GBM14_591T1', 'GBM14_593T', 
        'GBM14_594T2_M8', 'GBM14_605T_M8', 'GBM14_606T', 'GBM14_608T', 'GBM14_617T', 'GBM14_619T', 'GBM14_629T', 'GBM14_664T1', 'GBM14_664T2_M9', 'GBM14_665T1',
        'GBM14_669T', 'GBM15_677T', 'GBM15_680T', 'GBM15_682T', 'GBM15_689T', 'GBM15_693T1', 'GBM15_693T2', 'GBM15_693T4', 'GBM15_694T2', 'GBM15_694T3', 
        'GBM15_694T5', 'GBM15_696T', 'GBM15_698T', 'GBM15_699T', 'GBM15_700T', 'GBM15_705T', 'GBM15_708T', 'GBM15_709T1_M8', 'GBM15_714T_M9', 'GBM15_717T', 
        'GBM15_718T1', 'GBM15_718T2', 'GBM15_729T', 'GBM15_732T_M8', 'GBM15_734T2_M8', 'GBM15_756T_M8', 'GBM15_757T2_M8', 'GBM15_758T_M8')
  
  dbId=c('S592', 'S626', '', 'S775', '', 'IRCR_GBM_352_TL', 'IRCR_GBM_352_TR', 'IRCR_GBM14_458', 'IRCR_GBM14_485', 'IRCR_GBM14_487', '', '', 'IRCR_GBM14_500', 
         'IRCR_GBM14_503', 'IRCR_GBM14_504_T03', 'IRCR_GBM14_508', 'IRCR_GBM14_524', 'IRCR_GBM14_526', 'IRCR_GBM14_527_T02', 'IRCR_GBM14_529', 'IRCR_GBM14_534',
         'IRCR_GBM14_541', 'IRCR_GBM14_542_T01', '', '', 'IRCR_GBM14_549_T01', 'IRCR_GBM14_554_TA', 'IRCR_GBM14_559_T01', 'IRCR_GBM14_559_T02', 'IRCR_GBM14_565',
         '', '', 'IRCR_GBM14_570_T02', 'IRCR_GBM14_571', 'IRCR_GBM14_574', 'IRCR_GBM14_576', 'IRCR_GBM14_586', 'IRCR_GBM14_588', 'IRCR_GBM14_591_T01', 
         'IRCR_GBM14_593', '', 'IRCR_GBM14_605', 'IRCR_GBM14_606', 'IRCR_GBM14_608', 'IRCR_GBM14_617', 'IRCR_GBM14_619_T01', 'IRCR_GBM14_629', 
         'IRCR_GBM14_664_T01', 'IRCR_GBM14_664_T02', 'IRCR_GBM14_665_T01', '', 'IRCR_GBM15_677', 'IRCR_GBM15_680', 'IRCR_GBM15_682', '', 'IRCR_GBM15_693_T01', 
         'IRCR_GBM15_693_T02', 'IRCR_GBM15_693_T04', 'IRCR_GBM15_694_T02', 'IRCR_GBM15_694_T03', 'IRCR_GBM15_694_T05', 'IRCR_GBM15_696', 'IRCR_GBM15_698', 
         'IRCR_GBM15_699', 'IRCR_GBM15_700', 'IRCR_GBM15_705', 'IRCR_GBM15_708_TA', 'IRCR_GBM15_709_T01', 'IRCR_GBM15_714', '', 'IRCR_GBM15_718_T01', 
         'IRCR_GBM15_718_T02', '', '', '', '', '', '')
  
  iddf = data.frame(sId,dbId)
  
  subtype = read.delim('~/NSL_GBM_RPKM_subtype_040915.dat',check.names=F,header=F)
  df = read.csv(inFileName,check.names=F) # inFileName = "/home/heejin/DrugScreening/Input/150409_AUC_v4.csv"
  d1 = merge(iddf,df,by.x=colnames(iddf)[1],by.y='Drug')
  d2 = merge(subtype,d1,by.x=colnames(subtype)[1],by.y="dbId")
  
  for (i in 9:ncol(d2)){
    #addlab = as.character(d2[,1])
    
  # boxplot
    pdf(sprintf("~/DrugScreening/figure/SUBTYPEv4/%s_boxplot.pdf",colnames(d2)[i]))
  par(mfrow=c(1,1))
  sub = factor(d2[,7],levels=c("P","N","C","M"))
 # boxplot(d2[,i]~sub,ylab='AUC', main=sprintf("%s",colnames(d2)[i]))
    boxplot(d2[,i]~sub,main=sprintf("%s",colnames(d2)[i]),add=F,ylab=expression(bold("Area Under Curve")),boxwex=.5,
            boxlwd=3,whisklwd=3,staplelwd=3,outlwd=3,frame.plot=F,medlwd=5,axes=F,outcol=NA)
    box(lwd=3)
    axis(side=2,font=2,lwd=3) 
    axis(side=1,font=2,lwd=3,at=1:length(levels(sub)),labels=levels(sub))
  stripchart(d2[,i]~sub,vertical = TRUE, pch=16,method = "jitter",add=T)
  #for (j in 1:nrow(d2)){
  #  text(sub[j],d2[j,i],label=addlab[j],cex=.6, adj=1,pos=4)
  #}
    dev.off()
  
  # cor plot
    pdf(sprintf("~/DrugScreening/figure/SUBTYPEv4//%s_corplot.pdf",colnames(d2)[i]))
  par(mfrow=c(2,2))
    
  pr = cor.test(d2[,2],d2[,i])
  plot(d2[,i]~d2[,2],xlab = 'Proneural Activity', ylab='AUC', main=sprintf("%s",colnames(d2)[i]), sub=sprintf("r=%.2f, p-value=%.2f",pr$esti,pr$p.value))
  pr = cor.test(d2[,3],d2[,i])
  plot(d2[,i]~d2[,3],xlab = 'Neural Activity', ylab='AUC', main=sprintf("%s",colnames(d2)[i]), sub=sprintf("r=%.2f, p-value=%.2f",pr$esti,pr$p.value))
  pr = cor.test(d2[,4],d2[,i])
  plot(d2[,i]~d2[,4],xlab = 'Classical Activity', ylab='AUC', main=sprintf("%s",colnames(d2)[i]), sub=sprintf("r=%.2f, p-value=%.2f",pr$esti,pr$p.value))
  pr = cor.test(d2[,5],d2[,i])
  plot(d2[,i]~d2[,5],xlab = 'Mesenchymal Activity', ylab='AUC', main=sprintf("%s",colnames(d2)[i]), sub=sprintf("r=%.2f, p-value=%.2f",pr$esti,pr$p.value))
    dev.off()
    }
  
  print("--------------------------------------")
  print(as.character(df$Gene[1]))
  
  drugNameL = unique(df$Drug)
  
  for (drug in drugNameL) {
    
    df_ft = df[df$Drug == drug & !is.na(df$AUC) & df$db_id != '',]
    df_ft = df_ft[order(df_ft$AUC),]
    
    if (TRUE %in% !is.na(df_ft$Alt)){
      
      df_ft$group = 'High 50%'
      df_ft$group[df_ft$Alt<=quantile(df_ft$Alt,0.5,na.rm=T)] = 'Low 50%'
      w_p = round(wilcox.test(df_ft$AUC~df_ft$group)$p.value,4)
      t_p = round(t.test(df_ft$AUC~df_ft$group)$p.value,4)
      
      cor_p = cor.test(df_ft$Alt,df_ft$AUC)$p.value
      cor_r = cor.test(df_ft$Alt,df_ft$AUC)$estimate
      
      low_n = length(df_ft$db_id[df_ft$group=='Low 50%'])
      high_n = length(df_ft$db_id[df_ft$group=='High 50%'])
      
      write(sprintf('%s\t%s\t%.4f\t%.4f\t%s\t%s\t%s\t%s',drug,df_ft$Gene[1],cor_p,cor_r,high_n,low_n,w_p,t_p),
            file=outFileName,append=T)
      
      if (plot == T) {
        addlab = as.character(df_ft$db_id)
        outFilePrefix = strsplit(rev(strsplit(outFileName,"/")[[1]])[1],".txt")[[1]]
        outFilePrefix = sprintf("%s/%s",outPlotDirName,outFilePrefix)
        pdf(sprintf("%s_%s_%s.pdf",outFilePrefix,df_ft$Gene[1],drug),useDingbats=F)#,width=5)
        plot(df_ft$AUC~df_ft$Alt,main=sprintf("%s",drug),ylab=sprintf('%s',type),xlab=sprintf('%s log2(RPKM+1)',df_ft$Gene[1]))
        text(df_ft$Alt,df_ft$AUC,label=addlab,cex=.6, adj=1,pos=4)
        
        #group = factor(df_ft$group,levels=c('High 50%','Low 50%'))
        #boxplot(df_ft$AUC~group,main=sprintf("%s",drug),add=F,ylab=sprintf('%s',type))
        #stripchart(df_ft$AUC~group,vertical = TRUE, pch=16,method = "jitter",add=T)
        #for (i in 1:nrow(df_ft)){
        #  text(group[i],df_ft$AUC[i],label=addlab[i],cex=.6, adj=1,pos=4)
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