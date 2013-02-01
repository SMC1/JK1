#!/usr/bin/python

import sys, os, re, getopt
import mybasic

def lift19to18_sort_tdf(inputDirN,outputDirN,hg19to18_list,pbs):

	changelist=[]

	for line in open(hg19to18_list):
		changelist.append(line[:-1])
	
	for sampN in changelist:

		if pbs:

			os.system('echo "~/JK1/NGS/coverage/fixBed.py < %s/%s_hg19.bedgraph > %s/%s_hg19.bedgraph.tmp1; \
				/home/tools/ucsc/liftOver %s/%s_hg19.bedgraph.tmp1 /home/tools/ucsc/hg19ToHg18.over.chain %s/%s.bedgraph.tmp2 %s/%s_unmapped.bed; \
				sort -k1,1 -k2,2n < %s/%s.bedgraph.tmp2 > %s/%s.bedgraph; igvtools toTDF -z 4 %s/%s.bedgraph %s/%s.tdf hg18" \
				| qsub -N %s -o %s/%s_exchange.qlog -j oe' % \
				(inputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, \
				outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, sampN, outputDirN,sampN))

		else:

			print sampN

			os.system('(~/JK1/NGS/coverage/fixBed.py < %s/%s_hg19.bedgraph > %s/%s_hg19.bedgraph.tmp1; \
				liftOver %s/%s_hg19.bedgraph.tmp1 /home/tools/ucsc/hg19ToHg18.over.chain %s/%s.bedgraph.tmp2 %s/%s_unmapped.bed; \
				sort -k1,1 -k2,2n < %s/%s.bedgraph.tmp2 > %s/%s.bedgraph; igvtools toTDF -z 4 %s/%s.bedgraph %s/%s.tdf hg18) 2> %s/%s_exchange.qlog' % \
				(inputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, \
				outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN))

						
optL, argL = getopt.getopt(sys.argv[1:],'i:o:j:p',[])

optH = mybasic.parseParam(optL)

inputDirN=optH['-i']

if '-o' in optH:
	outputDirN = optH['-o']
else:
	outputDirN = inputDirN

hg19to18_list=optH['-j']

lift19to18_sort_tdf(inputDirN,outputDirN,hg19to18_list,'-p' in optH)
