#!/usr/bin/python

import sys, os, re, getopt
import mybasic

def main(inputDirN, outputDirN, pbs=False):

	inputFileNL = os.listdir(inputDirN)
		
	inputTFileNL = filter(lambda x: re.match('.*\.loh\.mutscan', x),inputFileNL)
	inputNFileNL = filter(lambda x: re.match('.*[^loh].mutscan', x),inputFileNL)

	inputFileNL = inputTFileNL + inputNFileNL

	print 'Files: %s' % inputFileNL

	tSampNL = list(set([re.match('(.*)\.loh\.mutscan',inputFileN).group(1) for inputFileN in inputTFileNL]))
	nSampNL = list(set([re.match('(.*)\.mutscan',inputFileN).group(1) for inputFileN in inputNFileNL]))

	sampNL = tSampNL + nSampNL
	sampNL.sort()

	print 'Samples: %s' % sampNL

	for sampN in tSampNL:

		if len(nSampNL) ==1:
			nSampN = nSampNL[0]
		else:
			continue
		
		print 'Tumor Sample: %s, Normal Sample: %s' % (sampN, nSampN)
		
		cmd = '~/JK1/NGS/loh/delta_baf_mutscan.py -i %s/%s.mutscan -t %s/%s.loh.mutscan -o %s/%s.dbaf.txt' % (inputDirN,nSampN, inputDirN,sampN, outputDirN,sampN)
		log = '%s/%s.dbaf.log' % (outputDirN,sampN)
		if pbs:
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, sampN, log))

		else:
			os.system('(%s) 2> %s' % (cmd, log))



if __name__ == '__main__':
	optL, argL = getopt.getopt(sys.argv[1:],'i:o:p:',[])

	optH = mybasic.parseParam(optL)

