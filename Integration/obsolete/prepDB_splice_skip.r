main <- function(

inFile,
outFile,
geneL

)
{

options(warn=-1)

data <- read.table(inFile, header=TRUE, sep='\t')

attach(data)

gender <- as.character(gender)
gender[gender == 'FEMALE'] <- 'F'
gender[gender == 'MALE'] <- 'M'

days_to_death <- as.character(days_to_death)
days_to_death[days_to_death == '[Not Applicable]'] <- '-1'
days_to_death <- as.numeric(days_to_death)

days_to_tumor_progression <- as.character(days_to_tumor_progression)
days_to_tumor_progression[days_to_tumor_progression == '[Pending]'] <- 'Inf'
days_to_tumor_progression <- as.numeric(days_to_tumor_progression)

days_to_tumor_recurrence <- as.character(days_to_tumor_recurrence)
days_to_tumor_recurrence[days_to_tumor_recurrence == '[Pending]'] <- 'Inf'
days_to_tumor_recurrence <- as.numeric(days_to_tumor_recurrence)

followup <- pmax(days_to_death, prog_or_recur, days_to_last_followup)
followup[followup <= 0] <- -1

output <- data.frame(bcr_patient_barcode,age_at_initial_pathologic_diagnosis,gender,days_to_death,followup,prog_or_recur)

write.table(output, file=outFile, sep='\t', quote=FALSE, row.names=FALSE, col.names=TRUE)

}

main('/EQL1/NSL/RNASeq/alignment/splice_skipping_NSL36.txt', '/EQL1/NSL/RNASeq/alignment/.txt', c('EGFR'))
