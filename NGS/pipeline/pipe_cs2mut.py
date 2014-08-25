#!/usr/bin/python

import sys, os, re, getopt
import mybasic, mypipe, mysetting
from glob import glob

def main(inputFilePathL, projectN, clean=False, pbs=False, server='smc1', genome='hg19'):

	baseDir = mypipe.prepare_baseDir(projectN, mkdir=True)

	for inputFileP in inputFilePathL:

		inputFileP2 = inputFileP[:-7] + '\*.fq.gz'
		inputFileN = inputFileP.split('/')[-1]
		sampN = inputFileN.split('.')[0]

		print sampN, inputFileP2
		cmd = '/usr/bin/python %s/NGS/pipeline/pipe_s_cs2mut.py -i %s -n %s -p %s -c %s -s %s -g %s' % (mysetting.SRC_HOME, inputFileP2, sampN, projectN, False, server, genome)
		if pbs:
			log = '%s/%s.Xsq.qlog' % (baseDir+'/'+sampN, sampN)
			os.system('echo "%s" | qsub -q %s -N %s -o %s -j oe' % (cmd, server, sampN, log))

		else:
			log = '%s/%s.Xsq.qlog' % (baseDir, sampN)
			os.system('(%s) 2> %s' % (cmd, log))


if __name__ == '__main__':
## old pipeline (without indel caller)
#	main(glob('/EQL2/CS_20140613/WXS/fastq/link/*.1.fq.gz'), projectN='test_cs2mut', clean=False, pbs=False, server='smc1', genome='hg19')
#	main(glob('/EQL2/CS_20140613/WXS/fastq/link/*.1.fq.gz'), projectN='CS20140613_xsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#	main(glob('/EQL2/CS_20140618/WXS/fastq/link/*.1.fq.gz'), projectN='CS20140618_xsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#	main(glob('/EQL2/CS_20140623/WXS/fastq/link/*.1.fq.gz'), projectN='CS20140623_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
	## batch for old samples
#	main(glob('/EQL2/CS_201403*/WXS/fastq/link/*.1.fq.gz'), projectN='CS_mut', clean=False, pbs=True, server='smc1', genome='hg19')
#	main(glob('/EQL2/CS_201404*/WXS/fastq/link/*.1.fq.gz'), projectN='CS_mut', clean=False, pbs=True, server='smc1', genome='hg19')
#	main(glob('/EQL2/CS_201405*/WXS/fastq/link/*.1.fq.gz'), projectN='CS_mut', clean=False, pbs=True, server='smc1', genome='hg19')
#	main(glob('/EQL2/CS_201406*/WXS/fastq/link/*.1.fq.gz'), projectN='CS_mut', clean=False, pbs=True, server='smc1', genome='hg19')
#	main(glob('/EQL2/CS_201407*/WXS/fastq/link/*.1.fq.gz'), projectN='CS_mut', clean=False, pbs=True, server='smc1', genome='hg19')
	
#	main(glob('/EQL2/CS_20140714/WXS/fastq/link/*.1.fq.gz'), projectN='CS_mut', clean=False, pbs=True, server='smc1', genome='hg19')
#	main(glob('/EQL2/CS_20140728/WXS/fastq/link/*.1.fq.gz'), projectN='CS_mut', clean=False, pbs=True, server='smc1', genome='hg19')
#	main(glob('/EQL2/CS_20140805/WXS/fastq/link/*.1.fq.gz'), projectN='CS_mut', clean=False, pbs=True, server='smc1', genome='hg19')
	main(glob('/EQL2/CS_20140819/WXS/fastq/link/*.1.fq.gz'), projectN='CS_mut', clean=False, pbs=True, server='smc2', genome='hg19')
