#!/usr/bin/python

import sys, os, getopt
from glob import glob

import mypipe, mybasic, mysetting

def genSpec(baseDir, server='smc1', genome='hg19'):

	mybasic.add_module_path(['NGS/align','NGS/fastq','NGS/coverage','NGS/expression'])
	import trim_batch, gsnap_sam_batch, bam2sortedBed_batch, sortedBed2tdf_batch, degSeq_batch ## MODULES
	import fastqc_batch
	
	return [ ## PARAMETERS
		{
		'name': 'FastQC',
		'desc': 'QC for fastq',
		'fun': fastqc_batch.fastqc_batch,
		'paramL': (baseDir, '(.*)\.[12]\.fq\.gz', baseDir, baseDir),
		'paramH': {},
		'logPostFix': '.fastqc.qlog',
		'logExistsFn': lambda x: len(x)>0 and 'Analysis complete' in x[-1],
		'outFilePostFix': ['_fastqc.zip'],
		'outLinkPostFix': ['_fastqc/fastqc_report.html'],
		'clean': False,
		'rerun': False
		},

		{
		'name': 'Trim',
		'desc': 'fq.gz -> trim -> fq',
		'fun': trim_batch.trim_batch,
		'paramL': (baseDir, '(.*)\.[12]\.fq\.gz', baseDir, 30),
		'paramH': {},
		'logPostFix': '.trim.log',
		'logExistsFn': lambda x: len(x)==0,
		'outFilePostFix': ['t1.fq.gz', 't2.fq.gz'],
		'clean': False,
		'rerun': False
		},

		{
		'name': 'Mapping',
		'desc': 'fq -> bam',
		'fun': gsnap_sam_batch.align,
		'paramL': (baseDir, baseDir, False, 'sanger', '%s_nh' % (genome)),
		'paramH': {},
		'logPostFix': '.gsnap.qlog',
		'logExistsFn': lambda x: len(x)>0 and 'Processed' in x[-1],
		'outFilePostFix': ['bam'],
		'clean': False,
		'rerun': False
		},

		{
		'name': 'Formet Conversion and sorting',
		'desc': 'bam -> sort -> sorted.bed',
		'fun': bam2sortedBed_batch.sam2bed_batch,
		'paramL': (baseDir, baseDir, '', False),
		'paramH': {},
		'logPostFix': '.sorted.bed.qlog',
		'logExistsFn': lambda x: len(x)==0,
		'outFilePostFix': ['sorted.bed'],
		'clean': False,
		'rerun': False
		},

		{
		'name': 'TDFgen',
		'desc': 'sorted.bed -> bedgraph -> tdf',
		'fun': sortedBed2tdf_batch.main,
		'paramL': (baseDir, baseDir, False, '%s/chromsizes_%s.txt' % (mysetting.ucscSeqDir[server][genome], genome), genome),
		'paramH': {},
		'logPostFix': '.tdf.qlog',
		'logExistsFn': lambda x: len(x)>0 and 'Done' in x[-9],
		'outFilePostFix': ['bedgraph','tdf'],
		'clean': False,
		'rerun': False
		},

		{
		'name': 'RPKMgen',
		'desc': 'sorted.bed -> rpkm',
		'fun': degSeq_batch.main,
		'paramL': (baseDir, baseDir, mysetting.refFlatH[server][genome], False),
		'paramH': {},
		'logPostFix': '.degSeq.qlog',
		'logExistsFn': lambda x: len(x)>0 and 'ZZZ3' in x[-1],
		'outFilePostFix': ['rpkm'],
		'clean': False,
		'rerun': False
		},

#		{
#		'name': 'Cleanup',
#		'desc': 'remove all, but logs and designated result file',
#		'fun': cleanup.main,
#		'paramL': (baseDir,),
#		'paramH': {},
#		'logPostFix': 'cleanup.qlog',
#		'logExistsFn': lambda x: False,
#		'outFilePostFix': ['pileup']
#		},

		]

if __name__ == '__main__':

	optL, argL = getopt.getopt(sys.argv[1:],'i:n:p:c:s:g:',[])

	optH = mybasic.parseParam(optL)

	pathL = optH['-i']
	sN = optH['-n']
	pN = optH['-p']
	clean = optH['-c']
	server = optH['-s']
	genome = optH['-g']

	mypipe.main(inputFilePathL=glob(pathL), genSpecFn=genSpec, sampN=sN, projectN=pN, clean=clean, server=server, genome=genome)
	#mypipe.main(inputFilePathL=glob('/home/heejin/practice/pipeline/fusion/S436_RSq_test.*.fq.gz'), genSpecFn=genSpec, sampN='S436_RSq_test', projectN='test_rpkm', clean=False)
