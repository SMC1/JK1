runascat <- function(
  DirName,
  sampN,
  inLogRFile,
  inBafFile,
  outFile,
  platformName = "AffySNP6"
){
  
  setwd(DirName)
  
  source("/data1/home/heejin/ASCAT/ASCAT2.1/ascat.R")
  ascat.bc = ascat.loadData(inLogRFile,inBafFile)
  ascat.plotRawData(ascat.bc)
  source("/data1/home/heejin/ASCAT/ASCAT2.1/predictGG.R")
  platform = platformName # "Illumina610k","AffySNP6"
  ascat.gg = ascat.predictGermlineGenotypes(ascat.bc, platform)
  ascat.bc = ascat.aspcf(ascat.bc,ascat.gg=ascat.gg)
  ascat.plotSegmentedData(ascat.bc)
  ascat.output = ascat.runAscat(ascat.bc)
  
  frac = ascat.output$aberrantcellfraction
  ploidy = ascat.output$ploidy
  sampN = ascat.bc$samples
  
  cat(sprintf('%s\t%s\t%s',sampN,frac,ploidy),file=outFile,append=TRUE,sep='\n')
  # output: sample name, fraction, ploidy
  
}

args <- commandArgs(TRUE)

runascat(args[1],args[2],args[3],args[4],args[5],args[6])