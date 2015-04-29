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
        #text(df_ft$Alt,df_ft$AUC,label=addlab,cex=.6, adj=1,pos=4)
        
        # vIII 
        #library("RMySQL")
        #con <- dbConnect(MySQL(), user="cancer", password="cancer", dbname='ircr1', host="localhost")
        #v3.df = dbGetQuery(con, sprintf("SELECT * FROM splice_skip
        #  where gene_sym ='EGFR' and delExons like '%s2-7%s' and nPos>2 and frame like '%s:Y%s' group by samp_id;",'%','%','%','%'))
        #df_ft$v3 = 'black'
        #df_ft$v3[df_ft$db_id %in% v3.df$samp_id] = 'red'
        #plot(df_ft$AUC~df_ft$Alt,main=sprintf("%s",drug),ylab=sprintf('%s',type),xlab=sprintf('%s log2(RPKM+1)',df_ft$Gene[1]),col=df_ft$v3)
        
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
