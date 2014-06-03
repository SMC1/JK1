createReview <- function(

obj.name = 'TCGA_GBM_CNA_SNP6_abs',
absolute.files.dir = '/EQL1/TCGA/GBM/array_cn/absolute_results',
results.dir = '/EQL1/TCGA/GBM/array_cn/absolute_results/summary'

)
{

library(ABSOLUTE)

setwd(absolute.files.dir)

absolute.files <- list.files(absolute.files.dir,'.*[.]RData')

CreateReviewObject(obj.name, absolute.files, results.dir, "allelic", verbose=TRUE)

}

args <- commandArgs(TRUE)

#createReview(args[1],args[2],args[3])
createReview()
