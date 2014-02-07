#!/usr/bin/python

import sys, os, re, getopt
import mybasic

def main(inputDirN, outputDirN, pbs=False):

	inputFileNL = os.listdir(inputDirN)
	inputFileNL = filter(lambda x: re.match('(.*)\.mutscan', x),inputFileNL)

	print 'Files: %s' % inputFileNL

	sampNL = list(set([re.match('(.*)\.mutscan',inputFileN).group(1) for inputFileN in inputFileNL]))
	sampNL.sort()

	print 'Samples: %s' % sampNL

	tSampNL = filter(lambda x: re.match('.*_T_.*',x), sampNL)
	nSampNL = list(set(sampNL).difference(set(tSampNL)))

	for sampN in tSampNL:

		if len(nSampNL) ==1:
			nSampN = nSampNL[0]
		else:
			continue
		
		print 'Tumor Sample: %s, Normal Sample: %s' % (sampN, nSampN)
		
		cmd = '~/JK1/NGS/purity/delta_baf_mutscan.py -i %s/%s.mutscan -t %s/%s.mutscan -o %s/%s.dbaf.txt' % (inputDirN,nSampN, inputDirN,sampN, outputDirN,sampN)
		log = '%s/%s.dbaf.log' % (outputDirN,sampN)
		if pbs:
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, sampN, log))

		else:
			os.system('(%s) 2> %s' % (cmd, log))



if __name__ == '__main__':
	optL, argL = getopt.getopt(sys.argv[1:],'i:o:p:',[])

	optH = mybasic.parseParam(optL)

