#!/usr/bin/python

import sys, os, re, getopt
import mybasic, mysetting

def main(inputDirN, outputDirN, pbs=False):

	inputFileNL = os.listdir(inputDirN)

	sampNL = list(set([re.match('.*/(.*).snp.qlog:Normal.*',line).group(1) for line in os.popen('grep "Normal Pileup" %s/*.snp*' % inputDirN)]))
	sampNL.sort()

	print 'Samples: %s' % sampNL

	for sampN in sampNL:

		print sampN
		
#		sId = re.match(pattern,sampN).group(1)

		cmd = '%s/NGS/loh/delta_baf.py -i %s/%s.snp -o %s/%s.dbaf.txt' % (mysetting.SRC_HOME, inputDirN,sampN, outputDirN,sampN)
		log = '%s/%s.dbaf.log' % (outputDirN,sampN)
		if pbs:
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, sampN, log))

		else:
			os.system('(%s) 2> %s' % (cmd, log))



if __name__ == '__main__':
	optL, argL = getopt.getopt(sys.argv[1:],'i:o:p:',[])

	optH = mybasic.parseParam(optL)

#	main('/EQL1/NSL/exome_bam/mutation', '/EQL1/NSL/exome_bam/purity', '.*([0-9]{3}).*', False)
