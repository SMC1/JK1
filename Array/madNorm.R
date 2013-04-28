madNormalize <- function(
  
  inGctFileName,
  outGctFileName

)
{
  
  inGctFile <- file(inGctFileName, "rt") 
  
  header1 <- readLines(inGctFile, 1)
  header2 <- readLines(inGctFile, 1)
  header3 <- readLines(inGctFile, 1)
  numLines <- as.integer(strsplit(header2,'\t')[[1]][1])
  
  outGctFile <- file(outGctFileName,'wt')
  
  writeLines(header1, outGctFile)
  writeLines(header2, outGctFile)
  
  tokL <- strsplit(header3,'\t')[[1]]
  tokL_len <- length(tokL)
  
  writeLines(header3, outGctFile)
  
  for (i in 1:numLines){
    
    tokL <- strsplit(readLines(inGctFile, 1),'\t')[[1]]
	dataL <- sapply(tokL[3:tokL_len],as.double)
    
	valueL <- dataL-median(dataL)
    
	mad = median(abs(valueL))
    
    for (i in 1:length(valueL)){
      valueL[i] <- valueL[i]/mad
    }
    
    valueL <- sapply(valueL, as.character)
    
    writeLines(sprintf('%s\t"%s"\t%s', tokL[1],tokL[2],paste(valueL,collapse='\t')), outGctFile)
  }
  
  close(inGctFile)
  close(outGctFile)
  
}

madNormalize('/EQL1/NSL/array_gene/NSL_GBM_93.gct','/EQL1/NSL/array_gene/NSL_GBM_93_madNorm.gct')
