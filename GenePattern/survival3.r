survival <- function(

inFile, # input multi-variate cox file
graphicsFormat='pdf',
legendPos='topright'

)
{

tokL <- strsplit(inFile,'/')[[1]]
dataSigName <- strsplit(tokL[length(tokL)],'.mvc')[[1]]
tokL <- strsplit(dataSigName,'__by__')[[1]]
dataName <- tokL[1]
sigName <- tokL[2]

library(survival)

data <- read.table(inFile, header=TRUE)
attach(data)

data_ft = data[priority==1 | priority==2 ,]

sink(sprintf('%s_stat.txt', dataSigName))

data.survdiff <- survdiff(Surv(data_ft$time, data_ft$event) ~ data_ft$label, rho=0)
print(data.survdiff)

print('---------------------------------------------------------')

data.cox <- summary(coxph(Surv(time, event) ~ value, , method="breslow"))
print(data.cox)

sink()

data.survdiff.p <- 1 - pchisq(data.survdiff$chisq, length(data.survdiff$n) - 1)
data.cox.hr <- data.cox$coefficients[2]
data.cox.p <- data.cox$waldtest[3]
data.cox.z <- data.cox$coefficients[4]

writeLines(sprintf('%f\t%f\t%f',data.cox.z,data.cox.p,data.survdiff.p))

if (graphicsFormat == 'png') {
	png(sprintf("%s_km.png", dataSigName))
} else {
	pdf(sprintf("%s_km.pdf", dataSigName))
}

clrH <- data.frame(priority=c(1,2,9), color=c('blue','red','grey'))

priorityF <- levels(factor(data$priority))

data.surv <- survfit(Surv(time, event) ~ priority)

legendT <- c()
legendC <- c()

for (i in priorityF) {

	idx <- sprintf("priority=%s",i)

	legendT[length(legendT)+1] <- sprintf('%s (n=%d)', data[priority==i, 'label'][1], data.surv[idx]$n)
	legendC[length(legendC)+1] <- as.character(clrH[clrH$priority==i,'color'])

}

plot(data.surv, main='', xlab="Days", ylab="Survival Fraction", col=legendC)

legend(legendPos, legendT, inset=0.1, col=legendC, lty=c(1,1,1))

title(main=list(sprintf('%s (Log-rank: p=%.1e; Cox: p=%.1e)',dataName,data.survdiff.p,data.cox.p), font=1))
#title(main=list(sprintf('%s (Log-rank: p=%.1e; Cox: HR=%.2f, p=%.1e)',dataName,data.survdiff.p,data.cox.hr,data.cox.p), font=1))

dev.off()

}

#args <- commandArgs(trailingOnly = T)

#print(args)

#survival(args[1])
#survival('/Users/jinkuk/Codes/GenePattern/Rembrandt_death__by__NSL_invasion.mvc')
