degSeq_batch <- function(

inDir,
outDir,
refFlatPath = '/data1/Sequence/ucsc_hg19/annot/refFlat.txt'

)
{

library('DEGseq')

fileL <- list.files(inDir,'.*[.]bed')

xL <- list.files(inDir,'.*bed.')

fileL <- setdiff(fileL, xL)

print(fileL)

for (fileN in fileL[151:170]) {

	getGeneExp(sprintf('%s/%s',inDir,fileN),refFlat=refFlatPath,output=sprintf('%s/%s.rpkm',outDir,fileN))
	
}

}

degSeq_batch('/EQL2/TCGA/GBM/RNASeq/coverage','/data1/TCGA/GBM/RNASeq/expression/knownGene/EGFR','/data1/Sequence/ucsc_hg19/annot/knownGene_EGFR.txt')
