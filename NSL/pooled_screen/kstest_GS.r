data=read.table("/EQL6/NSL/Barcode/NY/pooled_screeen_2.txt",sep='\t',header=T)
n=nrow(data)
data[,-1]=log(data[,-1])
data464=data[,c('X464_2','X464_4','X464_6')]
data827=data[,c('X827_1','X827_2','X827_3','X827_4','X827_5','X827_6')]
genelist=list(seq(1,7),seq(8,14),seq(15,19),seq(20,23),seq(24,28),seq(29,34),seq(35,40),seq(41,47),seq(48,54),seq(55,62),seq(63,68),seq(69,77),seq(78,84),seq(85,89),seq(90,95),seq(96,103),seq(104,111),seq(112,123),seq(124,131),seq(132,139),seq(140,149),seq(150,156))
pval464=matrix(nrow=n,ncol=1)
pval464_2=matrix(nrow=n,ncol=1)
pval827=matrix(nrow=n,ncol=1)
pval827_2=matrix(nrow=n,ncol=1)
for (i in 1:n){
	pval464[i]=ks.test(data464,as.numeric(data464[i,]))$p.value
	pval827[i]=ks.test(data827,as.numeric(data827[i,]))$p.value
}
for (j in genelist){
	pval464_2[j[1]]=ks.test(data464,as.matrix(data464[j,]))$p.value
	pval827_2[j[1]]=ks.test(data827,as.matrix(data827[j,]))$p.value
}
result464=cbind(data[,c('X','X464Ctrl')],data464,pval464,pval464_2)
result827=cbind(data[,c('X','X827Ctrl')],data827,pval827,pval827_2)

write.table(result464)
write.table(result827)
