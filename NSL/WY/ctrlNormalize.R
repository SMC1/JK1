inDirName <- '/data1/IRCR/WY'

inFileName <- 'human_afterMax.txt'; dsetName <- 'human'
#inFileName <- 'mouse_afterMax.txt'; dsetName <- 'mouse'

groupL = list(list(c(2),3:5,'S827'),list(c(6),7:9,'S448'),list(c(10),11:13,'S559'),list(c(14),15:17,'S464'))

data = read.table(sprintf('%s/%s',inDirName,inFileName),header=T)
data_out = read.table(sprintf('%s/%s',inDirName,inFileName),header=T)
ctrlCols = c()

for (exp in groupL){
  
#   for (i in 1:nrow(data)){
#     
#     fc <- log2(data[i,exp[[2]]] / data[i,exp[[1]]])
#     
#     data_out[i,exp[[2]]] <- as.vector(fc)
#     
#   }    
  
    data_out[,exp[[2]]] <- log2(data[,exp[[2]]] / data[,exp[[1]]])
    
  }
  
  ctrlCols <- c(ctrlCols,exp[[1]])
}

write.table(data_out[,-ctrlCols],sprintf('%s/%s_max_ctrl.txt',inDirName,dsetName),sep='\t',quote=F,row.names=F,col.names=T)
