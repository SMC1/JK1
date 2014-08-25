#!/usr/bin/python

import sys, os, re, getopt
import mybasic, mysetting

def main(inputDirN, outputDirN, pbs=False, inRefFlatFileName='/data1/Sequence/ucsc_hg19/annot/refFlat.txt', assembly='hg19'):

	inputFileNL = os.listdir(inputDirN)
	inputFileNL = filter(lambda x: re.match('.*\.loh_cn\.txt', x), inputFileNL)

	print 'Files: %s' % inputFileNL

	sampNL = list(set([re.match('(.*)\.loh_cn\.txt', inFileN).group(1) for inFileN in inputFileNL]))
	sampNL.sort()

	print 'Samples: %s' % sampNL

	for sampN in sampNL:

		print sampN
		
		cmd = '%s/NGS/loh/loh2gene.py -i %s/%s.loh_cn.txt -o %s/%s.loh_gene.dat -r %s -a %s' % (mysetting.SRC_HOME, inputDirN,sampN, outputDirN,sampN, inRefFlatFileName, assembly)
		log = '%s/%s.loh_gene.log' % (outputDirN,sampN)
		if pbs:
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, sampN, log))

		else:
			os.system('(%s) 2> %s' % (cmd, log))



if __name__ == '__main__':
	optL, argL = getopt.getopt(sys.argv[1:],'i:o:p:',[])

	optH = mybasic.parseParam(optL)

#	main('/EQL1/NSL/exome_bam/mutation', '/EQL1/NSL/exome_bam/purity', '.*([0-9]{3}).*', False)
