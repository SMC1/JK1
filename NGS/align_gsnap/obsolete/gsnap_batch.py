import os

runLogFile = open('log.txt','a')

for x in range(2,3): 

	dataDir = '/Data1/RNASeq_LymphNK/00_Sequence_fastq/SMC%s' % (x)

	for i in range(23,28):

		runLogFile.write('SMC %s  FILE %s START\n' % (x,i))
		runLogFile.flush()

		if i < 10 :
			os.system('gsnap --db=hg19 --batch=5 --nthreads=30 --npath=1 --novelsplicing=1 --use-splicing=refGene_knownGene_splicesites %s/S0%s_sequence_R1.txt %s/S0%s_sequence_R2.txt > /Data2/GH/RNASeq_SMC%s_S0%s_result.txt 2> /Data2/GH/RNASeq_SMC%s_S0%s_result_log.txt' % (dataDir,i,dataDir,i,x,i,x,i))
		else :
			os.system('gsnap --db=hg19 --batch=5 --nthreads=30 --npath=1 --novelsplicing=1 --use-splicing=refGene_knownGene_splicesites %s/S%s_sequence_R1.txt %s/S%s_sequence_R2.txt > /Data2/GH/RNASeq_SMC%s_S%s_result.txt 2> /Data2/GH/RNASeq_SMC%s_S%s_result_log.txt' % (dataDir,i,dataDir,i,x,i,x,i))

		runLogFile.write('SMC %s  FILE %s END\n' % (x,i))
		runLogFile.flush()

runLogFile.close()
