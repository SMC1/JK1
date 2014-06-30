args <- commandArgs(TRUE)

inFileN = args[1]
outDirN = args[2]
sampN = args[3]

inFile = read.delim(inFileN,header=T)

outFileN = sprintf("%s/%s.tumor_frac.txt", outDirN,sampN)

if (nrow(inFile) > 100){

frac = inFile[,5]
myden = density(frac,na.rm=T,bw=0.02)#bw="sj")
peak = myden$x[which.max(myden$y)]
tFrac = 1-peak

cat(sprintf("%s\t%.4f\t%.4f",sampN,peak,tFrac),file=outFileN,append=FALSE,sep='\n')

pdf(sprintf("%s/%s.frac_density.pdf",outDirN,sampN))
plot(myden,main=sprintf("%s normal fraction: %.4f", sampN,peak))
dev.off()
print("Done")
} else {
  cat(sprintf("%s\t-1\t-1",sampN),file=outFileN,append=FALSE,sep='\n')
  print("Done")
}
