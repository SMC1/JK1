zNormalize <- function(

inGctFileName,
outDir,
zMin=-1000,
zMax=1000

)
{

#inGctFileName <- '/Users/jinkuk/Downloads/clustering/GBH/NSL_GBM_46_4grpGenes.gct'
#inGctFileName <- '/Users/jinkuk/Data/NSL/clustering/NSL_GBM_58table1_NTRsorted_forHM.gct'
#inGctFileName <- '/Users/jinkuk/Data/NSL/NSL_GBM_93_invasionSig_HM.gct'
#zMin <- -2
#zMax <- 2

inGctFile <- file(inGctFileName, "rt") 

header1 <- readLines(inGctFile, 1)
header2 <- readLines(inGctFile, 1)
header3 <- readLines(inGctFile, 1)
numLines <- as.integer(strsplit(header2,'\t')[[1]][1])

tokL <- strsplit(inGctFileName,'/')[[1]]
dataName <- strsplit(tokL[length(tokL)],'.gct')[[1]]
outGctFileName <- sprintf('%s/%s_zNorm.gct', outDir,dataName)
outCsvFileName <- sprintf('%s/%s_zNorm.csv', outDir,dataName)

outGctFile <- file(outGctFileName,'wt')
outCsvFile <- file(outCsvFileName,'wt')

writeLines(header1, outGctFile)
writeLines(header2, outGctFile)

tokL <- strsplit(header3,'\t')[[1]]
tokL_len <- length(tokL)

writeLines(header3, outGctFile)
writeLines(sprintf('NAME,%s',paste(tokL[3:tokL_len],collapse=',')), outCsvFile)

for (i in 1:numLines){

	tokL <- strsplit(readLines(inGctFile, 1),'\t')[[1]]

	valueL <- scale(sapply(tokL[3:tokL_len], as.double))

	for (i in 1:length(valueL)){
		valueL[i] <- min(valueL[i],zMax)
		valueL[i] <- max(valueL[i],zMin)
	}

	valueL <- sapply(valueL, as.character)

	writeLines(sprintf('%s\t"%s"\t%s', tokL[1],tokL[2],paste(valueL,collapse='\t')), outGctFile)
	writeLines(sprintf('%s,%s', tokL[1],paste(valueL,collapse=',')), outCsvFile)
}

close(inGctFile)
close(outGctFile)
close(outCsvFile)

}

#zNormalize('/data1/IRCR/JW/NRP/TGFb_ft.gct','/data1/IRCR/JW/NRP',-2,2)
zNormalize('/EQL1/TCGA/GBM/array_gene/TCGA_GBM_gene_BI_sIdClps.gct','/EQL1/TCGA/GBM/array_gene',-2,2)
