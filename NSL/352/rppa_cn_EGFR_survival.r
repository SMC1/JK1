library(survival)

inDirName = '/data1/IRCR/352'

df = read.table(sprintf('%s/EGFR_cn_rppa_clin.txt',inDirName),header=T)
df$phospho <- pmax(df$Y1068,df$Y1173,df$Y992)

df$event <- (df$days_death == df$days_followup)
df[df$event==T,"event"] <- 1
df[df$event==F,"event"] <- 0

## grouping by EGFR copy number

df$group <- 1
df$group[df$cn>1.5] <- 2
df$group[df$cn>3] <- '3'

par(mfrow=c(1,1))
par(oma=c(1,1,1,0), mar=c(4,3,2,2),mgp=c(2,1,0))

data.surv <- survfit(Surv(df$days_followup, df$event) ~ df$group)
plot(data.surv,col=c('red','blue','green'))

data.survdiff <- survdiff(Surv(df$days_followup, df$event) ~ df$group)
legend('topright', c(sprintf('EGFR CN-norm N=%s', data.surv$n[1]),sprintf('EGFR CN>1.5 N=%s', data.surv$n[2]),sprintf('EGFR CN>3 N=%d', data.surv$n[3])), col=c('red','blue','green'), lty=c(1,1,1))

## grouping by EGFR copy number & p-EGFR

df$group <- 1
df$group[df$cn>1.5 & df$phospho>-0.72] <- 2

par(mfrow=c(1,1))
par(oma=c(1,1,1,0), mar=c(4,3,2,2),mgp=c(2,1,0))

data.surv <- survfit(Surv(df$days_followup, df$event) ~ df$group)
plot(data.surv,col=c('red','blue'))
legend('topright', c(sprintf('EGFR other N=%s', data.surv$n[1]),sprintf('EGFR CN>1.5 & p>-0.72 N=%s', data.surv$n[2])), col=c('red','blue'), lty=c(1,1))

data.survdiff <- survdiff(Surv(df$days_followup, df$event) ~ df$group)
pv  <- 1 - pchisq(data.survdiff$chisq, length(data.survdiff$n) - 1)
title(sprintf('P=%.1E',pv))

## grouping by EGFR copy number & p-EGFR

df$group <- 1
df$group[df$cn>1.5 & df$phospho>1] <- 2

par(mfrow=c(1,1))
par(oma=c(1,1,1,0), mar=c(4,3,2,2),mgp=c(2,1,0))

data.surv <- survfit(Surv(df$days_followup, df$event) ~ df$group)
plot(data.surv,col=c('red','blue'))
legend('topright', c(sprintf('EGFR other N=%s', data.surv$n[1]),sprintf('EGFR CN>1.5 & p>1 N=%s', data.surv$n[2])), col=c('red','blue'), lty=c(1,1))

data.survdiff <- survdiff(Surv(df$days_followup, df$event) ~ df$group)
pv  <- 1 - pchisq(data.survdiff$chisq, length(data.survdiff$n) - 1)
title(sprintf('P=%.1E',pv))

## grouping by EGFR copy number & p-EGFR

df$group <- 1
df$group[df$cn>3 & df$phospho>-0.72] <- 2

par(mfrow=c(1,1))
par(oma=c(1,1,1,0), mar=c(4,3,2,2),mgp=c(2,1,0))

data.surv <- survfit(Surv(df$days_followup, df$event) ~ df$group)
plot(data.surv,col=c('red','blue'))
legend('topright', c(sprintf('EGFR other N=%s', data.surv$n[1]),sprintf('EGFR CN>3 & p>-0.72 N=%s', data.surv$n[2])), col=c('red','blue'), lty=c(1,1))

data.survdiff <- survdiff(Surv(df$days_followup, df$event) ~ df$group)
pv  <- 1 - pchisq(data.survdiff$chisq, length(data.survdiff$n) - 1)
title(sprintf('P=%.1E',pv))

## grouping by EGFR copy number & p-EGFR

df$group <- 1
df$group[df$cn>3 & df$phospho>1] <- 2

par(mfrow=c(1,1))
par(oma=c(1,1,1,0), mar=c(4,3,2,2),mgp=c(2,1,0))

data.surv <- survfit(Surv(df$days_followup, df$event) ~ df$group)
plot(data.surv,col=c('red','blue'))
legend('topright', c(sprintf('EGFR other N=%s', data.surv$n[1]),sprintf('EGFR CN>3 & p>1 N=%s', data.surv$n[2])), col=c('red','blue'), lty=c(1,1))

data.survdiff <- survdiff(Surv(df$days_followup, df$event) ~ df$group)
pv  <- 1 - pchisq(data.survdiff$chisq, length(data.survdiff$n) - 1)
title(sprintf('P=%.1E',pv))

