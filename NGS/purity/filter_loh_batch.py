#!/usr/bin/python

import sys, os, re, getopt
import mybasic

def main(inputDirN, outputDirN, pattern, pbs=False):

	inputFileNL = os.listdir(inputDirN)

	sampNL = list(set([re.match('.*/(.*).snp.qlog:Normal.*',line).group(1) for line in os.popen('grep "Normal Pileup" %s/*.qlog' % inputDirN)]))
	sampNL.sort()

	print 'Samples: %s' % sampNL

	for sampN in sampNL:

		print sampN
		
		sId = re.match(pattern,sampN).group(1)

		cmd = '~/JK1/NGS/purity/filter_loh.py -i %s/%s.snp -o %s/S%s_LOH_af.txt' % (inputDirN,sampN, outputDirN,sId)
		log = '%s/S%s.loh.log' % (outputDirN,sId)
		if pbs:
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, sampN, log))

		else:
			os.system('(%s) 2> %s' % (cmd, log))



if __name__ == '__main__':
	optL, argL = getopt.getopt(sys.argv[1:],'i:o:p:',[])

	optH = mybasic.parseParam(optL)

	main('/EQL1/NSL/exome_bam/mutation', '/EQL1/NSL/exome_bam/purity', '.*([0-9]{3}).*', False)
