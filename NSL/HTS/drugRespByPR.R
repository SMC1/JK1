test <- function(
  inFileName,
  outFileName,
  plot,
  outPlotDirName,
  type
) {

  sId = c('592T', '626T', '723T', '775T', 'GBM13_235T', 'GBM13_352T1', 'GBM13_352T2', 'GBM14_458T_M2', 'GBM14_485T1_M2', 'GBM14_487T_M3', 'GBM14_497T_M3', 
          'GBM14_499T1_M3', 'GBM14_500T_M8', 'GBM14_503T_M3', 'GBM14_504T3_M3', 'GBM14_508T_M8', 'GBM14_524T_M3', 'GBM14_526T', 'GBM14_527T2', 'GBM14_529T', 
          'GBM14_534T', 'GBM14_541T', 'GBM14_542T', 'GBM14_543T', 'GBM14_544T', 'GBM14_549T1_M8', 'GBM14_554T_M8', 'GBM14_559T1', 'GBM14_559T2', 'GBM14_565T', 
          'GBM14_569T', 'GBM14_570T1', 'GBM14_570T2_M8', 'GBM14_571T', 'GBM14_574T', 'GBM14_576T', 'GBM14_586T_M8', 'GBM14_588T_M8', 'GBM14_591T1', 'GBM14_593T', 
          'GBM14_594T2_M8', 'GBM14_605T_M8', 'GBM14_606T', 'GBM14_608T', 'GBM14_617T', 'GBM14_619T', 'GBM14_629T', 'GBM14_664T1', 'GBM14_664T2_M9', 'GBM14_665T1',
          'GBM14_669T', 'GBM15_677T', 'GBM15_680T', 'GBM15_682T', 'GBM15_689T', 'GBM15_693T1', 'GBM15_693T2', 'GBM15_693T4', 'GBM15_694T2', 'GBM15_694T3', 
          'GBM15_694T5', 'GBM15_696T', 'GBM15_698T', 'GBM15_699T', 'GBM15_700T', 'GBM15_705T', 'GBM15_708T', 'GBM15_709T1_M8', 'GBM15_714T_M9', 'GBM15_717T', 
          'GBM15_718T1', 'GBM15_718T2', 'GBM15_729T', 'GBM15_732T_M8', 'GBM15_734T2_M8', 'GBM15_756T_M8', 'GBM15_757T2_M8', 'GBM15_758T_M8')
  pr = c('P', 'P', 'P', 'R', 'P', 'P', 'P', 'P', 'R', 'R', 'P', 'R', 'P', 'P', 'P', 'P', 'R', 'P', 'P', 'R', 'P', 'R', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 
         'P', 'P', 'P', 'P', 'P', 'R', 'P', 'P', 'R', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'R', 'P', 'P', 'P', 'R', 'P', 'P', 'R', 'P', 'P', 'P', 'P', 'P', 'P',
         'P', 'P', 'P', 'P', 'R', 'P', 'P', 'P', 'P', 'P', 'R', 'R', 'P', 'P', 'P', 'P', 'P', 'P')
  
  ex.list = c()
  
  df = read.csv(inFileName,check.names=F)
  d1 = data.frame(sId,pr)
  d2 = merge(d1,df,by.y=colnames(df)[1],by.x="sId")
  
  d2 = d2[!(d2[,1] %in% ex.list),]
  
  pr = gsub("P","Initial",d2$pr)
  pr = gsub("R","Recurrent",pr)
  
  initial_sampN = c()
  recur_sampN = c()
  initial_mean = c()
  recur_mean = c()
  initial_z_mean = c()
  recur_z_mean = c()
  initial_z_median = c()
  recur_z_median = c()
  ttest_p = c()
  wilcox_p= c()

  for (i in 3:ncol(d2)){ print(i)
    #addlab = as.character(d2[,1])

    sub = factor(pr,levels=c("Initial","Recurrent"))

	auc = data.frame("AUC"=d2[,i],sub)
	auc = na.omit(auc)

    z_norm = scale(auc$AUC)
    
	iN = length(grep("Initial",auc$sub))
	rN = length(grep("Recurrent",auc$sub))
    initial_sampN = c(initial_sampN,iN)
    recur_sampN = c(recur_sampN,rN)
    
    initial_mean = c(initial_mean,by(as.numeric(auc$AUC),auc$sub,mean,na.rm=T)[1])
    recur_mean = c(recur_mean,by(as.numeric(auc$AUC),auc$sub,mean,na.rm=T)[2])
	
	if (rN > 1) {
	t = t.test(auc$AUC~auc$sub)
    ttest_p = c(ttest_p,round(t$p.value,4))
	} else {
	ttest_p = c(ttest_p,NA)
	}

    wilcox_p = c(wilcox_p,round(wilcox.test(auc$AUC~auc$sub)$p.value,4))
    
	initial_z_mean = c(initial_z_mean,by(as.numeric(z_norm),auc$sub,mean,na.rm=T)[1])
    recur_z_mean = c(recur_z_mean,by(as.numeric(z_norm),auc$sub,mean,na.rm=T)[2])
    initial_z_median = c(initial_z_median,by(as.numeric(z_norm),auc$sub,median,na.rm=T)[1])
    recur_z_median = c(recur_z_median,by(as.numeric(z_norm),auc$sub,median,na.rm=T)[2])
    
    # boxplot
    if (plot==T) {
    pdf(sprintf("%s/%s_boxplot.pdf",outPlotDirName,colnames(d2)[i]))
    #boxplot(d2[,i]~sub,ylab=type, main=sprintf("%s",colnames(d2)[i]))
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
    }
  }
  
  outdf = data.frame("Drug"=colnames(df)[-1],initial_sampN,recur_sampN,initial_mean,recur_mean,ttest_p,wilcox_p,initial_z_mean,recur_z_mean,initial_z_median,recur_z_median)
  write.table(outdf, file = outFileName, row.names=F, col.names=T, quote=F, sep="\t")
  
}

#suppressWarnings(warning("Setting"))

#args <- commandArgs(TRUE)
#
#inFileName = args[1]
#outFileName = args[2]
#plot = args[3]
#outPlotDirName = args[4]
#type = args[5]

inFileName = '/home/heejin/DrugScreening/Input/150409_AUC_v4.csv'
outFileName = '/home/heejin/DrugScreening/result_AUC_QC_v4_PR.txt'
plot = TRUE
outPlotDirName = '/home/heejin/DrugScreening/figure/PRv4'
type = 'AUC'

test(inFileName,outFileName,plot,outPlotDirName,type)
