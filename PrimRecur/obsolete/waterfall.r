waterfall <- function(

inFile, # input dst file
graphicsFormat='png',
samplesToMark='',
vSta_global='',
vEnd_global=''


)
{

panelLimit <- 4

lines <- readLines(inFile)

analysisName <- strsplit(inFile,'.dst')[[1]][1]

if (graphicsFormat == 'png') {
	png(sprintf("%s_waterfall.png", analysisName))
} else {
	pdf(sprintf("%s_waterfall.pdf", analysisName))
}

par(mfrow=c(1,4))
#par(mfrow=c(1,min(length(lines)/4,panelLimit)))

i = 0

while (i+4 <= min(length(lines),panelLimit*4)) {

	tokL <- strsplit(lines[i+2], '\t')[[1]]

	dataName <- lines[i+1]
	featName <- tokL[1]
	valueL <- sapply(strsplit(lines[i+3], '\t')[[1]], as.double)
	sIdL <- strsplit(lines[i+4], '\t')[[1]]
	n <- length(valueL)

	vMax <- max(valueL)
	vMin <- min(valueL)

	vSta <- vMin - (vMax-vMin) * 0.1
	vEnd <- vMax + (vMax-vMin) * 0.1

	if (vSta_global!='' & vEnd_global!=''){

		vSta <- as.double(vSta_global)
		vEnd <- as.double(vEnd_global)

		valueL[valueL<=vSta] <- vSta
		valueL[valueL>=vEnd] <- vEnd
	}

	plot(seq(1,length(valueL)),valueL, ylab=featName, xlab='rank', main=sprintf('%s (n=%d)', dataName, n), pch=20, xlim=c(1,length(valueL)), ylim=c(vSta,vEnd))

	sIdL_mark <- strsplit(samplesToMark,',')[[1]]

	df <- data.frame(sId=sIdL,value=valueL,rank=seq(1,length(valueL)))
	
	count <- 0

	for (sId in sIdL_mark){

		idx <- df$sId==sId
		par(new=T)
		print(sprintf('%s %d %.2f',sId,df$rank[idx],df$value[idx]))
		plot(df$rank[idx],df$value[idx], xlim=c(1,length(valueL)), ylim=c(vSta,vEnd), xlab='', ylab='', col='red')
		text(1,vEnd-(vEnd-vSta)/20*count,sprintf('%s %d %.2f',sId,df$rank[idx],df$value[idx]),cex=0.5,adj=0)

		count <- count + 1
	}

	i <- i + 4
}

dev.off()

}

waterfall('TCGA_GBM_CNA_SNP6_Up1.dst','pdf',samplesToMark='TCGA-28-5209,TCGA-06-0747,TCGA-06-0211,TCGA-14-0817,TCGA-14-0817,TCGA-14-2554,TCGA-06-2557',vSta_global='',vEnd_global='')
