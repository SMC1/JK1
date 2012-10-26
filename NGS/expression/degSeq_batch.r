degSeq_batch <- function(

inDir,
outDir,
refFlatPath = '/data1/Sequence/ucsc_hg19/annot/refFlat.txt'

)
{

library('DEGseq')

fileL <- list.files(inDir,'.*[.]bed')

for (fileN in fileL) {

	if (fileN %in% c('G17224.TCGA-06-0139-01A-01R-1849-01.2_30nt_chr1.bed')) {
		getGeneExp(sprintf('%s/%s',inDir,fileN),refFlat=refFlatPath,output=sprintf('%s/%s.rpkm',outDir,fileN))
	}
}

}

degSeq_batch('/data1/TCGA/GBM/RNASeq/coverage','/data1/TCGA/GBM/RNASeq/expression','/data1/Sequence/ucsc_hg19/annot/refFlat_NTRK1.txt')
