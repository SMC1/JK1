#!/usr/bin/python

import sys, os, re
import mymysql, mysetting
from mybasic import rc
from mybasic import compl

def mutation_signature(inDirN, outDirN, outName=''):
	sampN = os.path.basename(inDirN)
	if outName == '':
		outName = '%s/%s.mutation_signature.txt' % (outDirN, sampN)
	outFile = open(outName, 'w')
	outFile.write('samp_id\tmutation\tcontext\tfreq\tn_mut\tn_total\n') # header

	mutFileNL = map(lambda x: x.rstrip(), os.popen('ls %s/*mutect*filter.vcf' % inDirN).readlines())
	if mutFileNL != []:
		mutH = {}
		for mutFileN in mutFileNL:
			(id, postfix) = re.search('(.*)_([A-Z0-9]{1,})_[TKNCS]{2}', sampN).groups()
			if postfix != 'T':
				sid = '%s_%s' % (id, postfix)
			else:
				sid = id

			mutFile = open(mutFileN, 'r')
			for line in mutFile:
				if line[0] == '#':
					continue

				colL = line.rstrip().split('\t')
				chr = colL[0]
				pos = colL[1]
				ref = colL[3]
				alt = colL[4]
				mutH[(chr,pos,ref,alt)] = 1
			#for line
		#for mutFileN
	#if there's mutation vcf
	
	mutFileNL = map(lambda x: x.rstrip(), os.popen('ls %s/*mutect' % inDirN).readlines())
	if mutFileNL == []:
		mutFileNL = map(lambda x: x.rstrip(), os.popen('ls %s/*mutect_rerun' % inDirN).readlines())
	if mutFileNL != []:
		sigH = {}
		cntH = {}
		total = 0
		for mutFileN in mutFileNL:
			mutFile = open(mutFileN, 'r')
			mutFile.readline()
			headerL = mutFile.readline().rstrip().split('\t')
			idxH = {}
			for i in range(len(headerL)):
				idxH[headerL[i]] = i
			for line in mutFile:
				colL = line.rstrip().split('\t')
				chr = colL[idxH['contig']]
				pos = colL[idxH['position']]
				context = colL[idxH['context']]
				ref = colL[idxH['ref_allele']]
				alt = colL[idxH['alt_allele']]
				if (chr,pos,ref,alt) in mutH:
					total += 1
					tri = context[2] + ref + context[4]
					if ref == 'C' or ref == 'T':
						nt_ch = ref + '>' + alt
					else:
						nt_ch = rc(ref) + '>' + rc(alt)
						tri = rc(tri)
					if (nt_ch, tri) in sigH:
						sigH[(nt_ch, tri)] += 1
					else:
						sigH[(nt_ch, tri)] = 1
					if nt_ch in cntH:
						cntH[nt_ch] += 1
					else:
						cntH[nt_ch] = 1
				# if not filtered out
			#for line
		#for mutFileN

		for key in sigH:
			(type, tri) = key
			freq = sigH[key]
			outFile.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (sid, type, tri, freq, cntH[type], total))
	#if raw mutect call
	outFile.flush()
	outFile.close()

if __name__ == '__main__':
#	mutation_signature('/EQL3/pipeline/somatic_mutect', '/EQL1/NSL/WXS/results/mutation/mutation_signature_mutect_20140227.txt')
#	mutation_signature('/EQL3/pipeline/somatic_mutect', '')
#	for id in ['IRCR_GBM10_038_T_SS','IRCR_GBM12_199_T_SS','IRCR_GBM14_412_T_SS','IRCR_GBM_363_TM_SS','IRCR_GBM_363_TD_SS','IRCR_GBM14_366_T_SS','IRCR_GBM14_476_T03_SS','S171_T_SS','S302_T_SS']:
#		print id
#		mutation_signature('/EQL3/pipeline/somatic_mutation/%s' % id, '/EQL3/pipeline/somatic_mutation/%s' % id)
	for id in filter(lambda x: os.path.isdir('/EQL3/pipeline/somatic_mutation/%s' % x), os.listdir('/EQL3/pipeline/somatic_mutation/')):
		if id in ['IRCR_GBM14_460_T_CS']:
			continue
		if not os.path.isfile('/EQL3/pipeline/somatic_mutation/%s/%s.mutation_signature.txt' % (id, id)):
			print id
			mutation_signature('/EQL3/pipeline/somatic_mutation/%s' % id, '/EQL3/pipeline/somatic_mutation/%s' % id)
	#for id
