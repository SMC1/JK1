#!/usr/bin/python

import sys, os, re, getopt
import mybasic

def main_pool(inputDirN, outputDirN, minCount=10, pool='/EQL1/NSL/WXS/results/CNA/CS_B_pool.rpkm', pbs=False):
	inputFileNL = os.listdir(inputDirN)
	inputFileNL = filter(lambda x: re.match('.*\.rpkm', x), inputFileNL)

	print 'Files: %s' % inputFileNL
	
	sampNL = list(set([re.match('(.*)\.rpkm',inputFileN).group(1) for inputFileN in inputFileNL]))
	sampNL.sort()

	print 'Samples: %s' % sampNL

	for sampN in sampNL:
		print sampN

		cmd = '~/JK1/NGS/copynumber/rpkm2cn.py -i %s/%s.rpkm -n %s -s %s -o %s/%s.copynumber -m %s' % (inputDirN,sampN, pool, sampN, outputDirN,sampN, minCount)
		log = '%s/%s.cn.log' % (outputDirN,sampN)
		if pbs:
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, tumorSampN, log))

		else:
			os.system('(%s) 2> %s' % (cmd, log))

def main(inputDirN, outputDirN, minCount=10, pbs=False):

	inputFileNL = os.listdir(inputDirN)
	inputFileNL = filter(lambda x: re.match('.*\.rpkm', x), inputFileNL)

	print 'Files: %s' % inputFileNL

	sampNL = list(set([re.match('(.*)\.rpkm',inputFileN).group(1) for inputFileN in inputFileNL]))
	sampNL.sort()

	print 'Samples: %s' % sampNL

	tumorSampNL = filter(lambda x: re.match('.*_T_.*',x), sampNL)
	tumorSampNL.sort()

	normalSampNL = list(set(sampNL).difference(set(tumorSampNL)))
	normalSampNL.sort()

	for tumorSampN in tumorSampNL:

		if len(normalSampNL) == 1:
			normalSampN = normalSampNL[0]
		else:
			continue

		print tumorSampN, normalSampN

		cmd = '~/JK1/NGS/copynumber/rpkm2cn.py -i %s/%s.rpkm -n %s/%s.rpkm -s %s -o %s/%s.copynumber -m %s' % (inputDirN, tumorSampN, inputDirN,normalSampN, tumorSampN, outputDirN,tumorSampN, minCount)
		log = '%s/%s.cn.log' % (outputDirN,tumorSampN)
		if pbs:
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, tumorSampN, log))

		else:
			os.system('(%s) 2> %s' % (cmd, log))



if __name__ == '__main__':
	optL, argL = getopt.getopt(sys.argv[1:],'i:o:p:',[])

	optH = mybasic.parseParam(optL)

	main('/home/heejin/practice/cn_xsq/S641_T_SS','/home/heejin/practice/cn_xsq/S641_T_SS', False)
