data = read.csv('/data1/IRCR/FGFR/AVATAR_MET_expr.csv',header=T)

plot.new()
par(mfrow=c(1,1))
par(oma=c(1,1,1,1))
par(mar=c(2,2,2,1))  

plot(1:length(data[[1]]),data[[1]][length(data[[1]]):1],pch=16,cex=1)