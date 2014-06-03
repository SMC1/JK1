absolute <- function(

seg.dat.fn,
sample.name,
results.dir

)
{

library(ABSOLUTE)

sigma.p=0
max.sigma.h=0.02
min.ploidy <- 0.95
max.ploidy <- 10
primary.disease='GBM'
platform='SNP_6.0'
max.as.seg.count <- 1500
max.non.clonal <- 0
max.neg.genome <- 0
copy_num_type <- "total"

RunAbsolute(seg.dat.fn, sigma.p, max.sigma.h, min.ploidy, max.ploidy, primary.disease, platform, sample.name, results.dir, max.as.seg.count, max.non.clonal,max.neg.genome, copy_num_type, maf.fn=NULL, min.mut.af=NULL, verbose=TRUE)
}

args <- commandArgs(TRUE)

absolute(args[1],args[2],args[3])
