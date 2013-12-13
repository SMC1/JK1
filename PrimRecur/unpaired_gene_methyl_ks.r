unpaired_ks <- function(
  inDirName,
  outFileN
)
{
  
  df = read.table(sprintf('%s/df_unpaired_methyl.txt',inDirName),header=TRUE)
  
#  if (graphicsFormat == 'png') {
#    png(sprintf("%s/cdf/unpaired_methyl_cdf_%s.png", inDirName,geneN))
#  } else if (graphicsFormat== 'pdf') {
#    pdf(sprintf("%s/cdf/unpaired_methyl_cdf_%s.pdf", inDirName,geneN))
#  }
#  
#  par(mfrow=c(2,2))
#  par(oma=c(1,1,1,0), mar=c(4,3,2,2),mgp=c(2,1,0))
#  
  for (dType in c('Methyl')) {
    
    df_ft = df[df$dbT==dbT & df$dType==dType,]
                        
    valL_p = df_ft[df_ft$PR=='P','val']
    valL_r = df_ft[df_ft$PR=='R','val']
    geneN = df_ft[1,'geneN']
    locus = df_ft[1,'loc']
    
#    qL = quantile(valL_r,c(.1,.9))
#    
#    plot(ecdf(valL_p),verticals=T,xlim=qL,ylim=c(0,1),pch=46,main='')
#    par(new=T)
#    plot(ecdf(valL_r),verticals=T,axes=F,ann=F,xlim=qL,ylim=c(0,1),pch=46,main='')
#

	ks = ks.test(valL_p,valL_r)
	p_value = ks['p.value']
	ks_score = ks['statistic']

	g = ks.test(valL_p,valL_r,alternative="greater")
	g_p_value = g['p.value']
	g_ks_score = g['statistic']

	l = ks.test(valL_p,valL_r,alternative="less")
	l_p_value = l['p.value']
	l_ks_score = l['statistic']
	
	cat(sprintf('%s\t%s\t%.2E\t%.2f\t%.2E\t%.2f\t%.2E\t%.2f\t%d\t%d',locus,geneN,p_value,ks_score,g_p_value,g_ks_score,l_p_value,l_ks_score,length(valL_p),length(valL_r)),file=outFileN,append=TRUE,sep='\n')

#    title(sprintf('%s, %s (%d,%d), P=%.1E',geneN,dType,length(valL_p),length(valL_r),p_value))
  }
  
#  if (graphicsFormat=='png' || graphicsFormat=='pdf'){    
#    dev.off()
#  }
}

#inDirName = '/EQL1/PrimRecur/unpaired'
#geneNL <- c('EGFR','CDK4','CDK6','PDGFRA','MET','MDM2','MDM4','CDKN2A','CDKN2B','CDKN2C','PTEN','RB1','NF1','QKI')

dbT = 'TCGA-GBM'

args <- commandArgs(TRUE)
unpaired_ks(args[1],args[2])
#unpaired_ks(inDirName,geneN,locus)

# unpaired_cdf(inDirName,'PDGFRA','')
