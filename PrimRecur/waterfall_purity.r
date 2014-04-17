comp_P = data.frame(v=c(84,64,90,90,90,62,47,66,81,88,63,89,42),n='P')
comp_R = data.frame(v=c(92,81,90,78,97,80,86,62,88,63,80,93,88),n='R')
comp_diff = comp_R$v - comp_P$v

sorted = comp_diff[order(comp_diff,decreasing=F)]  
barplot(sorted, space=0,col="white", names.arg=dataT[,1], cex.names=0.7, las=3, ylim=c(-100,100),ylab="% IOD Chnage")
