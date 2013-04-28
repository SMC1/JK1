library('DEGseq')

args <- commandArgs(TRUE)

getGeneExp(args[1],refFlat=args[3],output=args[2])
