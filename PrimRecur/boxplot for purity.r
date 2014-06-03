# By computation
comp_P = data.frame(v=c(84,64,90,90,90,62,47,66,81,88,63,89,42),n='P')
comp_R = data.frame(v=c(92,81,90,78,97,80,86,62,88,63,80,93,88),n='R')
comp = rbind(comp_P,comp_R)

# By pathology

plot.new()
par(mfrow=c(1,1))
par(oma=c(1,1,1,1))
par(mar=c(2,2,2,1))  

boxplot(comp$v ~ comp$n)
stripchart(comp$v ~ comp$n,vertical=T, add=T, method='jitter', pch=1)

comp_diff = comp_R$v - comp_P$v
boxplot(comp_diff)
stripchart(comp_diff,vertical=T, add=T, method='jitter', pch=1)
abline(h=0)