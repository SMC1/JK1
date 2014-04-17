#!/usr/bin/python

import sys, os
import mybasic, mysetting

def get_known(fileL=['/data1/Sequence/ucsc_hg19/annot/dbsnp_138.b37.vcf','/data1/Sequence/ucsc_hg19/annot/ESP6500SI-V2-SSA137.updatedProteinHgvs.ALL.snps_indels.vcf']):
	dbsnpH = {}
	for file in fileL:
		inFile = open(file, 'r')
		for line in inFile:
			if line[0] == '#':
				continue
			colL = line.rstrip().split('\t')
			chrom = colL[0]
			if len(chrom) < 3:
				if chrom.upper() == 'MT':
					chrom = 'M'
				chrom = 'chr%s' % chrom
			pos = int(colL[1])
			id = colL[2]
			ref = colL[3]
			altL = colL[4].split(',')

			for alt in altL:
				if len(ref)==1 and len(alt)==1:
					if chrom not in dbsnpH:
						dbsnpH[chrom] = []
					dbsnpH[chrom].append(pos)
				elif len(ref)>1 and len(alt)>1:
					(chrom1,pos1,ref1,alt1) = mybasic.left_align_var(chrom,pos,ref,alt)
					if len(ref)==1 and len(alt)==1:
						if chrom not in dbsnpH:
							dbsnpH[chrom] = []
						dbsnpH[chrom].append(pos1)
		#for line
	##for file
	for chr in dbsnpH:
		pL = list(set(dbsnpH[chr]))
		pL.sort()
		dbsnpH[chr] = pL
	return(dbsnpH)

def filter_known(dbsnpH, inFileN):
	inFile = open(inFileN, 'r')
	outFile = open('%s.dbsnp_flt' % inFileN, 'w')
	for line in inFile:
		colL = line.rstrip().split('\t')
		chrom = colL[0]
		pos = int(colL[1])
		idx =  mybasic.index(dbsnpH[chrom], pos)
		if idx < 0:## not found in dbsnp
			outFile.write(line)
	outFile.flush()
	outFile.close()


if __name__ == '__main__':
	dbsnpH = get_known()
## batch process for all rsq
	for dir in mysetting.rsqMutscanDirL:
		fileL = filter(lambda x: 'bak' not in x, map(lambda x: x.rstrip(), os.popen('find %s -name *.mutscan' % dir).readlines()))
		for file in fileL:
			if file == '/EQL1/NSL/RNASeq/alignment/splice_Z/gatk_test/mutation/S647_splice.mutscan':
				continue
			print file
			filter_known(dbsnpH, file)
## batch process for all wxs
	for dir in mysetting.wxsMutscanDirL:
		fileL = map(lambda x: x.rstrip(), os.popen('find %s -name *.mutscan' % dir).readlines())
		for file in fileL:
			print file
			filter_known(dbsnpH, file)
