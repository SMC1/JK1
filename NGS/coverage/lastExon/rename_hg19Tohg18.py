#!/usr/bin/python

import sys, os, re, getopt
import mybasic

def lift19to18_sort_tdf(inputDirN,outputDirN,hg19to18_list):

	changelist=[]

	for line in open(hg19to18_list):
		changelist.append(line[:-1])
	
	inputFileNL = os.listdir(inputDirN)
	
	inputFileNL = filter(lambda x: re.match('.*\.bedgraph', x),inputFileNL)
	
	for inputFileN in inputFileNL:
		
		sampN = re.match('(.*)\.bedgraph', inputFileN).group(1)

		if sampN in changelist:
			os.rename('%s/%s' % (inputDirN,inputFileN),'%s/%s_hg19.bedgraph'% (inputDirN,sampN))
					
optL, argL = getopt.getopt(sys.argv[1:],'i:o:j:p',[])

optH = mybasic.parseParam(optL)

inputDirN=optH['-i']

if '-o' in optH:
	outputDirN = optH['-o']
else:
	outputDirN = inputDirN

hg19to18_list=optH['-j']

lift19to18_sort_tdf(inputDirN,outputDirN,hg19to18_list)
