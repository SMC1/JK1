import os

dataDir = '/data1/RNASeq_LymphNK/00_Sequence_fastq/SMC1'

os.system('bowtie -S hg19 -1 %s/S03_sequence_R1.txt -2 %s/S03_sequence_R2.txt /data2/FusionSeq/RNASeq_SMC1_S03_bowtie.sam' % (dataDir,dataDir))
#os.system('bowtie -S hg19 -1 %s/S03_sequence_R1.txt -2 %s/S03_sequence_R2.txt /data2/FusionSeq/RNASeq_SMC1_S03_bowtie.sam 2> /data2/FusionSeq/RNASeq_SMC1_S03_bowtie.log' % (dataDir,dataDir))
