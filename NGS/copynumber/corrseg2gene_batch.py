#!/usr/bin/python

import sys, os, re, getopt
import mybasic

def main(inputDirN, outputDirN, inRefFlatFileName='/data1/Sequence/ucsc_hg19/annot/refFlat.txt', geneNameL=[], assembly='hg19', pbs=False):

	inputFileNL = os.listdir(inputDirN)
	inputFileNL = filter(lambda x: re.match('.*\.corr\.ngCGH.seg', x), inputFileNL)

	print 'Files: %s' % inputFileNL

	sampNL = list(set([re.match('(.*)\.corr\.ngCGH.seg',inputFileN).group(1) for inputFileN in inputFileNL]))
	sampNL.sort()

	print 'Samples: %s' % sampNL

	geneNames = ','.join(geneNameL)
	
	for sampN in sampNL:

		print sampN

		if len(geneNameL) > 0:
			cmd = '~/JK1/NGS/copynumber/seg2gene.py -i %s/%s.corr.ngCGH.seg -o %s/%s.corr.cn_gene.dat -r %s -g %s -a %s' % \
				(inputDirN, sampN, outputDirN,sampN, inRefFlatFileName, geneNames, assembly)
		else:
			cmd = '~/JK1/NGS/copynumber/seg2gene.py -i %s/%s.corr.ngCGH.seg -o %s/%s.corr.cn_gene.dat -r %s -a %s' % \
				(inputDirN, sampN, outputDirN,sampN, inRefFlatFileName, assembly)
		print cmd
		log = '%s/%s.corr.cn_gene.log' % (outputDirN,sampN)
		if pbs:
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, sampN, log))

		else:
			os.system('(%s) &> %s' % (cmd, log))



if __name__ == '__main__':
	optL, argL = getopt.getopt(sys.argv[1:],'i:o:p:',[])

	optH = mybasic.parseParam(optL)

	main('/home/heejin/practice/cn_xsq/S641_T_SS','/home/heejin/practice/cn_xsq/S641_T_SS', '/data1/Sequence/ucsc_hg19/annot/refFlat.txt',[], 'hg19', False)
