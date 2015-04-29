source(sprintf('%s/JK1/NGS/copynumber/draw_CNA_traj_lib.R', Sys.getenv('HOME')))

args<-commandArgs(trailingOnly=T) ## 1:sampN, 2:segFile, 3:outName
sId <- args[1]
segFile <- args[2]
outName <- args[3]

format<-substr(outName, nchar(outName)-2, nchar(outName))
if (format == 'png') {
  png(outName, width=1000)
} else {
  pdf(outName, width=10)
}
drawTrajAll(segFile,sId)
dev.off()
