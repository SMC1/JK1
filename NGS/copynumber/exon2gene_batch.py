#!/usr/bin/python

import sys, os, re, getopt
import mybasic, mysetting

def main(inputDirN, outputDirN, inRefFlatFileName='/data1/Sequence/ucsc_hg19/annot/refFlat.txt', geneNameL=[], assembly='hg19', pbs=False):
	inputFileNL = os.listdir(inputDirN)
	inputFileNL = filter(lambda x: re.match('.*copynumber', x), inputFileNL)

	print 'Files: %s' % inputFileNL

	sampNL = list(set([re.match('(.*)\.copynumber',inputFileN).group(1) for inputFileN in inputFileNL]))
	sampNL.sort()

	print 'Samples: %s' % sampNL

	geneNames = ','.join(geneNameL)

	for sampN in sampNL:
		print sampN

		if (len(geneNameL) > 0):
			cmd = '~/JK1/NGS/copynumber/exon2gene.py -i %s/%s.copynumber -o %s/%s.cn_gene.dat -r %s -g %s -a %s' % \
				(inputDirN,sampN, outputDirN,sampN, inRefFlatFileName, geneNames, assembly)
		else:
			cmd = '~/JK1/NGS/copynumber/exon2gene.py -i %s/%s.copynumber -o %s/%s.cn_gene.dat -r %s -a %s' % \
				(inputDirN,sampN, outputDirN,sampN, inRefFlatFileName, assembly)
		
		print cmd

		log = '%s/%s.cn_gene.log' % (outputDirN,sampN)
		if pbs:
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, sampN, log))
		else:
			os.system('(%s) &> %s' % (cmd, log))

if __name__ == '__main__':
	optL, argL = getopt.getopt(sys.argv[1:],'i:o:p:',[])

	optH = mybasic.parseParam(optL)

#	main('/home/heejin/practice/cn_xsq/S641_T_SS','/home/heejin/practice/cn_xsq/S641_T_SS', '/data1/Sequence/ucsc_hg19/annot/refFlat.txt',[], 'hg19', False)
	main('/EQL3/pipeline/SGI20140410_xsq2mut/S364_T_SS', '/EQL3/pipeline/SGI20140410_xsq2mut/S364_T_SS', mysetting.cs_gene, 'hg19', False)
