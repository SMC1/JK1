#!/usr/bin/python

import sys, os, re, getopt
import mybasic

def lift19to18_sort_tdf(inputDirN,outputDirN,hg19to18_list,pbs):

	changelist=[]
	for line in open(hg19to18_list):
		changelist.append(line)
	
	inputFileNL = os.listdir(inputDirN)
	
	inputFileNL = filter(lambda x: re.match('.*\.bedgraph', x),inputFileNL)
	
	for inputFileN in inputFileNL:
		
		sampN = re.match('(.*)\.bedgraph', inputFileN).group(1)

		if sampN in changelist:
			os.rename('%s/%s'%(inputDirN,inputFileN),'%s_hg19.bedgraph'%sampN)
	
	for sampN in changelist:

		if pbs:

			os.system('echo "python fixBed.py -i %s/%s_hg19.bedgraph; ~/home/tools/ucsc/liftOver %s/%s_hg19.bedgraph hg19to18chain %s/%s.bedgraph %s_unmapped.bed; sort -k1 1 -k2 2n < %s/%s.bedgraph > %s/%s.bedgraph; igvtools to TDF -z 4 %s/%s.bedgraph %s/%s.tdf hg18" | qsub -N %s -o %s/%s_exchange.qlog -j oe'%(inputDirN,sampN,inputDirN,sampN,outputDirN,sampN,sampN,outputDirN,sampN,outputDirN,sampN,outputDirN,sampN,outputDirN,sampN,sampN,outputDirN,sampN))

		else:

			print sampN
			os.system('python fixBed.py -i %s/%s_hg19.bedgraph; ~/home/tools/ucsc/liftOver %s/%s_hg19.bedgraph hg19to18chain %s/%s.bedgraph %s_unmapped.bed; sort -k1 1 -k2 2n < %s/%s.bedgraph > %s/%s.bedgraph; igvtools to TDF -z 4 %s/%s.bedgraph %s/%s.tdf hg18 2> %s/%s_exchange.qlog'%(inputDirN,sampN,inputDirN,sampN,outputDirN,sampN,sampN,outputDirN,sampN,outputDirN,sampN,outputDirN,sampN,outputDirN,sampN,outputDirN,sampN))

						
optL, argL = getopt.getopt(sys.argv[1:],'i:o:j:p',[])

optH = mybasic.parseParam(optL)

inputDirN=optH['-i']

if '-o' in optH:
	outputDirN = optH['-o']
else:
	outputDirN = inputDirN

hg19to18_list=optH['-j']


