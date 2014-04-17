#!/usr/bin/python

import sys, os, re
import mysetting, mybasic

MIN_COV = 5 ## minimum total coverage
MIN_MUT_N = 5 ## minimum # of mutation allele count

MIN_COV = 20
#MIN_MUT_N = 20
MIN_MUT_N = 5

def mutscan_signature(mode='WXS', outFileN=''):
	if outFileN == '':
		outFile = sys.stdout
	else:
		outFile = open(outFileN, 'w')
	dirLH = {'WXS': mysetting.wxsMutscanDirL, 'RSQ': mysetting.rsqMutscanDirL}
	contextH = {}
	for dir in dirLH[mode]:
		fileL = filter(lambda x: 'bak' not in x, map(lambda x: x.rstrip(), os.popen('find %s -name *dbsnp_flt' % dir).readlines()))
		for file in fileL:
			if mode=='RSQ':
				if os.path.basename(file) == 'S647_splice.mutscan.dbsnp_flt': ## duplicated files
					continue
				if 'splice_Z' in file:
					sid = re.match('(.*)_splice2.mutscan.dbsnp_flt', os.path.basename(file)).group(1)
				else:
					sid = re.match('(.*)_RSq_splice.mutscan.dbsnp_flt', os.path.basename(file)).group(1)
			else:
				sid = re.match('(.*).mutscan.dbsnp_flt', os.path.basename(file)).group(1)
			sigH = {}
			cntH = {}
			total = 0
			inFile = open(file, 'r')
			for line in inFile:
				colL = line.rstrip().split('\t')
				chrom = colL[0]
				pos = int(colL[1])
				ref = colL[2]
				alt = colL[3]
				if ref == 'N' or len(alt) > 1:
					continue
				n_ref = int(colL[4])
				n_alt = int(colL[5])

				if n_alt >= MIN_MUT_N and (n_alt+n_ref) >= MIN_COV:
					start = pos - 1
					end = pos + 1
					if chrom in contextH and pos in contextH[chrom]:
						context = contextH[chrom][pos]
					else:
						resL = os.popen('samtools faidx /data1/Sequence/ucsc_hg19/hg19.fasta %s:%s-%s' % (chrom,start,end)).readlines()
						context = resL[1].rstrip().upper()
						if chrom not in contextH:
							contextH[chrom] = {}
						contextH[chrom][pos] = context

					if ref not in ['C','T']:
						ref = mybasic.rc(ref)
						alt = mybasic.rc(alt)
						context = mybasic.rc(context)

					ch = ref + '>' + alt
					if ch in cntH:
						cntH[ch] += 1
					else:	
						cntH[ch] = 1
					if (ch,context) in sigH:
						sigH[(ch,context)] += 1
					else:
						sigH[(ch,context)] = 1
					total += 1
				#if
			##for line

			for (type,context) in sigH:
				outFile.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (sid, type, context, sigH[(type,context)], cntH[type], total))
		##for file
	#for dir
	outFile.flush()
	outFile.close()

def mutscan_signature_rsq():
	for dir in mysetting.rsqMutscanDirL:
		fileL = filter(lambda x: 'bak' not in x, map(lambda x: x.rstrip(), os.popen('find %s -name *dbsnp_flt' % dir).readlines()))
		for file in fileL:
			if 'splice_Z' in file:
				sid = re.match('(.*)_splice[2]*.mutscan.dbsnp_flt', os.path.basename(file)).group(1)
			else:
				sid = re.match('(.*)_RSq_splice.mutscan.dbsnp_flt', os.path.basename(file)).group(1)
			cntH = {}
			total = 0
			inFile = open(file, 'r')
			for line in inFile:
				colL = line.rstrip().split('\t')
				chrom = colL[0]
				ref = colL[2]
				alt = colL[3]
				if ref == 'N' or len(alt)>1:
					continue
				n_ref = int(colL[4])
				n_alt = int(colL[5])

				if n_alt >= MIN_MUT_N and (n_alt+n_ref) >= MIN_COV:
					if ref not in ['C','T']:
						ref = mybasic.rc(ref)
						alt = mybasic.rc(alt)
					if (ref,alt) in cntH:
						cntH[(ref,alt)] += 1
					else:
						cntH[(ref,alt)] = 1
					total += 1
			##for line

			for (r,a) in cntH:
				sys.stdout.write('%s\t%s>%s\t%s\t%s\n' % (sid, r,a, cntH[(r,a)], total))
		##for file
	#for dir

if __name__ == '__main__':
	mutscan_signature(mode='RSQ', outFileN='/EQL1/NSL/RNASeq/results/mutation/mutation_signature_mutscan_RSQ_20140227.txt')
	mutscan_signature(mode='WXS', outFileN='/EQL1/NSL/WXS/results/mutation/mutation_signature_mutscan_20140227.txt')
