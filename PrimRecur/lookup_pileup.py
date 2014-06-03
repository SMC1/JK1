#!/usr/bin/python

import sys, os, re
import mymysql


pileupDirL = ['/EQL1/NSL/WXS/exome_20130529/','/EQL1/NSL/exome_bam/mutation/pileup_proc/','/EQL1/pipeline/ExomeSeq_20130723/','/EQL3/pipeline/SGI20140103_xsq2mut/','/EQL3/pipeline/SGI20131119_xsq2mut/']

mutTypeH = { \
	'SKIP':('splice_skip_AF','delExons','nReads,nReads_w1','loc1','gene_sym'), \
	'3pDEL':('splice_eiJunc_AF','juncAlias','nReads,nReads_w','loc','gene_sym'), \
	'MUT':('mutation_normal','ch_aa','nReads_alt,nReads_ref','','gene_symL'), \
	'MUTR':('mutation_rsq','ch_aa','r_nReads_alt,r_nReads_ref','','gene_symL') \
	}


def lookupPileup(pileupDirL,sId,chrom,loc,ref,alt):

	inputFileNL = []
	
	for pileupDir in  pileupDirL:
		inputFileNL += os.popen('find %s -name %s_T_*%s.pileup_proc' % (pileupDir,sId,chrom)).readlines()

	if len(inputFileNL) > 1:
		inputFileNL = filter(lambda x: not re.match('.*KN.*', x),inputFileNL)

#	if len(set(inputFileNL)) != 1:
#		print 'Error:', list(set(inputFileNL))
#		raise Exception

	if len(inputFileNL) == 0:
		return None

	resultL = os.popen('grep -m 1 "^%s:%s," %s' % (chrom,loc,inputFileNL[0].rstrip()), 'r').readlines()

	if len(resultL)==0:
		return None
	else:
		tL = resultL[0].rstrip().split(',')
		if ref != tL[2]:
			raise Exception
		refCount = int(tL[3])
		altCount = tL[4].count(alt)
		return (altCount,refCount)


print lookupPileup(pileupDirL,'S652','chr7',55221744,'C','T')
