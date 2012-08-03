PhenotypicSignatureAnalysis_perm <- function(

gp,

trainGctFile = "/home/jinkuk/Codes/NSL/NSL_GBM_46.gct",
phenoFile = "/home/jinkuk/Codes/NSL/pheno_NSL.txt",
phenoName = "invasion",
pvCutoff = "0.05",
weighting = "t.score",

testGctFile = "/home/jinkuk/Codes/NSL/Rembrandt_GBM.gct",
resamplings = "1",
clnFile = "/home/jinkuk/Codes/NSL/clinical_Rembrandt.txt",

sigName = "NSL_invasion",
dataName = "Rembrandt",
endPoint = "death",
ntpCutoff = "1.",
format = "pdf",
legendPos = "topright",

resultDir = '/home/jinkuk/Codes/NSL/tmp'

)
{

m1.result <- run.analysis(gp, "sig_pheno", inGctFile=trainGctFile, inPhenoFile=phenoFile, phenoName=phenoName) 
print("m: 1/3")

m2.result <- run.analysis(gp, "procSig", inFile=job.result.get.url(m1.result,"sig"), cutoff=pvCutoff, sortby="p.value") 
print("m: 2/3")

m3.result <- run.analysis(gp, "ntpSig", inFile=job.result.get.url(m2.result,"sig"), weighting=weighting) 
print("m: 3/3")


n1.result <- run.analysis(gp, "filterSigGct_HJ", input.gct.file=testGctFile, input.sig.file=job.result.get.url(m3.result,"nsg"))
print("n: 1/4")

n2.result <- run.analysis(gp, "NearestTemplatePrediction2", input.exp.filename=job.result.get.url(n1.result,"gct"), input.features.filename=job.result.get.url(n1.result,"nsg"), output.name="NTP", distance.selection="cosine", weight.genes="T", num.resamplings=resamplings, GenePattern.output="F", random.seed="7392854") 
print("n: 2/4")

n3.result <- run.analysis(gp, "pred2surv", input.pred.file=job.result.get.url(n2.result,"ntp"), input.clinical.file=clnFile, sigName=sigName, dataName=dataName, endPoint=endPoint, cutoff=ntpCutoff) 
print("n: 3/4")

n4.result <- run.analysis(gp, "survival", inFile=job.result.get.url(n3.result,"mvc"), graphicsFormat=format, legendPos=legendPos) 
print("n: 4/4")


jobNum <- job.result.get.job.number(n4.result)

print(sprintf('[%d]', jobNum))

job.result.download.files(n4.result, resultDir)

}


args <- commandArgs(TRUE)

servername <- "http://localhost:8080"
username <- "jinkuk"
password <- ""

library(methods)
library(rJava)
library(GenePattern)
gp <- gp.login(servername, username, password)

phenoFile = "/home/jinkuk/Codes/NSL/pheno_NSL.txt"
pheno <- read.table(phenoFile, header=TRUE, sep='\t')

permPhenoFile <- "/home/jinkuk/Codes/NSL/tmp/permPheno.txt"

resultDir <- "/home/jinkuk/Codes/NSL/tmp"
stdoutFile <- sprintf("%s/stdout.txt", resultDir)
zScoreFile <- sprintf("%s/zScore.txt", resultDir)

zF <- file(zScoreFile,'wt')
writeLines('index\tz_wald\tp_wald\tp_logrank', zF)

for(i in 1:1000) {

	pheno$invasion <- pheno$invasion[sample(length(pheno$invasion))]

	write.table(pheno, file=permPhenoFile, row.names=FALSE, col.names=TRUE, sep='\t')

	PhenotypicSignatureAnalysis_perm(gp=gp, phenoFile=permPhenoFile, resultDir=resultDir) 

	f <- file(stdoutFile,'rt')
	l <- strsplit(readLines(f,1),'\t')[[1]][1:3]
	close(f)

	print(sprintf('** %dth execution  z:%s, p(wald):%s, p(logrank):%s',i,l[1],l[2],l[3]))

	writeLines(sprintf('%d\t%s\t%s\t%s', i,l[1],l[2],l[3]), zF)
}

close(zF)
