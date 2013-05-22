inDirName <- '/data1/IRCR/WY'

inFileName <- 'human_afterMax.txt'; dsetName <- 'human'
#inFileName <- 'mouse_afterMax.txt'; dsetName <- 'mouse'

groupL = list(list(c(2),c(3),'S827_AVA',1.58),list(c(6),c(7),'S448_AVA',0.64),list(c(10),c(11),'S559_AVA',1.57),list(c(14),c(15),'S464_AVA',0.48))

data = read.table(sprintf('%s/%s',inDirName,inFileName),header=T)

for (exp in groupL){
  
  grp1 <- data[,exp[[1]]]
  grp2 <- data[,exp[[2]]]
  
  fc <- log2(grp2/exp[[4]]/grp1)
  
  data_out <- data.frame(gN=data[,1],fc=fc)
  
  write.table(data_out[order(data_out$fc),],sprintf('%s/%s_%s.rnk',inDirName,dsetName,exp[[3]]),sep='\t',quote=F,row.names=F,col.names=F)
}