#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def main(inputDirN, outputDirN, pbs=False):

	inputFileNL = os.listdir(inputDirN)
	inputFileNL = filter(lambda x: re.match('(.*)\.pileup', x),inputFileNL)

	print 'Files: %s' % inputFileNL

	sampNL = list(set([re.match('(.*)\.pileup',inputFileN).group(1) for inputFileN in inputFileNL]))

	sampNL.sort()

	print 'Samples: %s' % sampNL

	tSampNL = filter(lambda x: re.match('.*_T_.*',x), sampNL)
	tSampNL.sort()

	nSampNL = list(set(sampNL).difference(set(tSampNL)))
	nSampNL.sort()

	for tSampN in tSampNL:

		if len(nSampNL) == 1:
			nSampN = nSampNL[0]
		else:
			continue

		print 'Tumor Sample: %s, Normal Sample: %s' % (tSampN, nSampN)

		if pbs:

			os.system('echo "java -jar /home/tools/VarScan/VarScan.v2.3.3.jar somatic %s/%s.pileup %s/%s.pileup %s/%s --min-var-freq 0.10" | \
				qsub -N %s -o %s/%s.snp.qlog -j oe' % \
				(inputDirN,nSampN, inputDirN,tSampN, outputDirN,tSampN, tSampN, outputDirN,tSampN))

		else:

			os.system('java -jar /home/tools/VarScan/VarScan.v2.3.3.jar somatic %s/%s.pileup %s/%s.pileup %s/%s --min-var-freq 0.10 2> %s/%s.snp.qlog' % \
				(inputDirN,nSampN, inputDirN,tSampN, outputDirN,tSampN, outputDirN,tSampN))


if __name__ == '__main__':

	optL, argL = getopt.getopt(sys.argv[1:],'i:o:p:',[])

	optH = mybasic.parseParam(optL)

	main('/EQL1/NSL/Exome/mutation', '/EQL1/NSL/Exome/mutation', True)
