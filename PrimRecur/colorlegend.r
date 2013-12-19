rpkm_range = 255-255* log10(c(0,9999) + 1)/4

plot.new()
par(mfrow=c(2,1))
plot(0,0)
color.legend(0,0,1,1,c(0,9999),color.gradient(1,c(1,0),c(1,0)),gradient="y")
plot(0,0)
color.legend(0,0,1,1,c(-4,0,4),c(color.gradient(c(0,1),c(0,1),1),color.gradient(1,c(1,0),c(1,0))),gradient="y")
