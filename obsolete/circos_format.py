#simple test2
#ex) chr12	345	6789 pair name +

import sys, re

if len(sys.argv) >= 3:
	inFileName = sys.argv[1]
	outFileName = sys.argv[2]
else:
	inFileName = '/Data2/RNASeq_SMC1_S02_result_unpaired_proc.txt'
	outFileName = '/Data2/RNASeq_SMC1_S02_result_unpaired_circos.txt'
	
outFile = open(outFileName, 'w')
inFile = open(inFileName)


for x in inFile:

	sp = x.split('\t\t')
	
	pair_name[0] = sp[1][:sp[1].find(':')]
	pair_name[1] = sp[0][:sp[0].find(':')]

	for y in range(2):

		locL = []

		for loc in sp[y].split(','):
			locL.append(re.match('([^;]+):([0-9]+)-([0-9]+)([-+])',loc).groups())

		outFile.write('chr'+locL[0][0]+'\t'+locL[0][1]+'\t'+locL[0][2]+'\t+'pair_name[y]+locL[0][3]+'\n')

inFile.close()
