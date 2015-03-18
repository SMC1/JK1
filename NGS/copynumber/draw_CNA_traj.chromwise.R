source(sprintf('%s/JK1/NGS/copynumber/draw_CNA_traj_lib.R',Sys.getenv('HOME')))

args<-commandArgs(trailingOnly=T) ## 1:sampN, 2:prbFile, 3:outName
sId <- args[1]
prbFile <- args[2]
outName <- args[3]

#par(mgp=c(2,1,0), oma=c(1,2,1,1), mar=c(1,3,0,0))
format<-substr(outName, nchar(outName)-2, nchar(outName))
if (format == 'png') {
  png(outName, width=1000)
} else { 
  pdf(outName, width=20)
}
for (chr in c(1:22,'X','Y')) {
  drawTraj_chromwise(chr, fileN=prbFile, sampN=sId, lColCommon='black')
}
dev.off()
