#!/usr/bin/python

import sys, os, re, getopt
import mybasic
import mymysql
from glob import glob

def coverage_calc_batch(inputDirNL,outputDirN,pbs=False,refFileName='/data1/Sequence/ucsc_hg19/annot/refFlat_exon_autosome_NM_merged.txt'):

	con,cursor = mymysql.connectDB(db='ircr1')
	cursor.execute('select distinct samp_id from sample_tag_paperfreeze')
	sampNameL = [x[0] for x in cursor.fetchall()]
	sampNameL = sampNameL + ['S641','S140']

	inputFileNL = [re.match('.*\/(S[0-9]{1}.*S$)', x).group(1) for x in inputDirNL]
	inDirSampNameL = [re.match('(S.*)_T_[TS]S$', x).group(1) for x in inputFileNL]
	
	sampNameS = set(sampNameL).intersection(inDirSampNameL)
	sampNameL = list(sampNameS)
	sampNameL.sort()

	print 'Samples: %s (%s)' % (sampNameL,len(sampNameL))
	
	fileNameL = []

	for fileN in inputDirNL:
		
		sampN = re.match('(S.*)_T_[TS]S$',fileN.split('/')[-1]).group(1)

		if sampN not in sampNameL:
			continue

		fileNameL = fileNameL + glob(fileN+'/*_[TB]_[TS]S*.bam')
		fileNameL.sort()

	procL = []

	for fileN in fileNameL:

		sampN = re.match('(.*).recal.bam',fileN.split('/')[-1]).group(1)

		if sampN in procL:
			continue

		print sampN
		
		cmd = 'samtools depth -b %s %s > %s/%s.recal.depth.txt' % \
			(refFileName,fileN, outputDirN,sampN)
		log = '%s/%s.depth.qlog' % (outputDirN,sampN)

		if pbs:
			cmd = "%s; awk '{cnt[\$3]+=1}END{for (x in cnt){print x,cnt[x]}}' %s/%s.recal.depth.txt | sort -n -k1 > %s/%s.recal.depth_hash.txt" % \
				(cmd, outputDirN,sampN, outputDirN,sampN)
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd,sampN,log))
		else:
			cmd = '%s; awk "{cnt[\$3]+=1}END{for (x in cnt){print x,cnt[x]}}" %s/%s.recal.depth.txt | sort -n -k1 > %s/%s.recal.depth_hash.txt' % \
				(cmd, outputDirN,sampN, outputDirN,sampN)
			os.system('(%s) 2> %s' % (cmd, log))

		procL.append(sampN)

if __name__ == '__main__':
	
	#coverage_calc_batch(glob('/EQL3/pipeline/CNA/S*S'),'/EQL1/NSL/WXS/coverage/TCGA_GBM_mutsig_coverage',pbs=False, refFileName='/data1/Sequence/ucsc_hg19/annot/refFlat_exon_autosome_NM_TCGA_mutsig.txt')
	#coverage_calc_batch(glob('/EQL3/pipeline/CNA/S*S'),'/EQL1/NSL/WXS/coverage/COSMIC_coverage',pbs=False, refFileName='/data1/Sequence/ucsc_hg19/annot/refFlat_exon_autosome_NM_cosmic.txt')
	coverage_calc_batch(glob('/EQL3/pipeline/CNA/S*S'),'/EQL1/NSL/WXS/coverage/average_coverage',pbs=False)
