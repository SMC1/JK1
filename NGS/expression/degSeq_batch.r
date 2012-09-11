degSeq_batch <- function(

inDir,
outDir,
refFlatPath = '/data1/Sequence/ucsc_hg19/annot/refFlat.txt'

)
{

library('DEGseq')

fileL <- list.files(inDir,'.*[.]bed')

for (fileN in fileL) {

	if (fileN %in% c('G17189.TCGA-06-0132-01A-02R-1849-01.2_30nt_chr1.bed','G17500.TCGA-27-1831-01A-01R-1850-01.2_30nt_chr1.bed','G17501.TCGA-27-2528-01A-01R-1850-01.2_30nt_chr1.bed','G17502.TCGA-14-0871-01A-01R-1849-01.2_30nt_chr1.bed')) {
		getGeneExp(sprintf('%s/%s',inDir,fileN),refFlat=refFlatPath,output=sprintf('%s/%s.rpkm',outDir,fileN))
	}
}

}

degSeq_batch('/data1/TCGA/GBM/RNASeq/density','/data1/TCGA/GBM/RNASeq/expression','/data1/Sequence/ucsc_hg19/annot/refFlat_NTRK1.txt')
