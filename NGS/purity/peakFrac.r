args <- commandArgs(TRUE)

inFileN = args[1]
outDirN = args[2]
sampN = args[3]

inFile = read.delim(inFileN)

frac = inFile[,6]
myden = density(frac,na.rm=T)
peak = myden$x[which.max(myden$y)]

outFileN = sprintf("%s/%s_normal_frac.txt", outDirN,sampN)
cat(sprintf("%s\t%.4f",sampN,peak),file=outFileN,append=FALSE,sep='\n')

pdf(sprintf("%s/%s_frac_density.pdf",outDirN,sampN))
plot(myden,main=sprintf("%s normal fraction: %.4f", sampN,peak))
dev.off()
