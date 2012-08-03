#python
#overlap del

import os, sys, re

if len(sys.argv) >= 3:
	inFileName = sys.argv[1]
	outFileName = sys.argv[2]
else:
    inFileName = '/home/gye_hyeon/RNASeq/code_jk/SMC1_S02_result_mismatch_unpaired_pro.txt'
    outFileName = '/home/gye_hyeon/RNASeq/SMC1_S02_result_mismatch_unpaired_pro_overlap.txt'

inFile = open(inFileName)
outFile = open(outFileName, 'w')

lines = inFile.readlines()
#cnt = 0
#alikesum = 0
#samesum = 0
#for line in lines:
#	num = []
#	loc = line.strip()
#	num = (re.search('same ([0-9]+), alike ([0-9]+)',loc).groups())
#	alikesum  += int(num[1])
#	samesum += int(num[0])
#	cnt += 1
#	print '%s line, sameSum: %s, alikeSum: %s' %(cnt,samesum,alikesum)
#	break
inFile.seek(0)
ss = []
ss = list(set(lines))
for line in ss:
#	cnt += 1
	outFile.write(line,)

inFile.close()




