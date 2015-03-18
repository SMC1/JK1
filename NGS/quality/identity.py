#!/usr/bin/python

import sys, os, getopt
import mybasic
from glob import glob
from datetime import datetime

def parse_info(tag):
	termL = tag.split(';')
	infoH = {}
	for term in termL:
		if '=' in term:
			[key,val] = term.split('=')
			infoH[key] = val
		else:
			infoH[term] = True
	return(infoH)

def clean_var(chrom,pos,ref,alt):
	len_tail = -1 * min(len(ref)-1, len(alt)-1)
	if alt[0]==ref[0] and alt[len_tail:] == ref[len_tail:]:
		alt = alt[:len_tail]
		ref = ref[:len_tail]
		return (chrom,pos,ref,alt)
	
	if len(ref)==len(alt) and ref[:-1]==alt[:-1]:
		pos = pos + len(ref) - 1
		ref = ref[-1:]
		alt = alt[-1:]
		return (chrom,pos,ref,alt)

	max_n = min(len(ref), len(alt))
	for i in range(max_n,0,-1):
		if alt[:i] == ref[:i]:
			alt = alt[(i-1):]
			ref = ref[(i-1):]
			pos = pos + i - 1
			return (chrom,pos,ref,alt)
	
	return (chrom,pos,ref,alt)

def filter_dbsnp(dbsnp='/data1/Sequence/ucsc_hg19/annot/dbsnp_135.hg19.sort.vcf'):
	inFile = open(dbsnp, 'r')
	outFile = open('/data1/Sequence/ucsc_hg19/annot/dbsnp_135.hg19.G5A_snv.sort.vcf', 'w')
	for line in inFile:
		if line[0] == '#':
			continue
		colL = line.rstrip().split('\t')
		chrom = colL[0]
		pos = int(colL[1])
		id = colL[2]
		ref = colL[3]
		altL = colL[4].split(',')

		infoH = parse_info(colL[7])
		if 'G5A' not in infoH: ## <5% in any populations
			continue
		## use common snps only (>5% in all populations)
		for alt in altL:
			if len(ref)==1 and len(alt)==1: #SNV
				outFile.write('%s\t%s\t%s\t%s\t%s\t.\t.\t%s\n' % (chrom,pos,id,ref,alt,colL[7]))
			elif len(ref)>1 and len(alt)>1: ## complex variants
				(chrom1,pos1,ref1,alt1) = clean_var(chrom,pos,ref,alt)
				if len(ref1)==1 and len(alt1)==1:
					outFile.write('%s\t%s\t%s\t%s\t%s\t.\t.\t%s\n' % (chrom1,pos1,id,ref1,alt1,colL[7]))
		##for alt
	##for line
	outFile.flush()
	outFile.close()
#bedtools intersect -wa -u -a /data1/Sequence/ucsc_hg19/annot/dbsnp_135.hg19.G5A_snv.sort.vcf -b /data1/Sequence/ucsc_hg19/annot/refFlat_exon.bed > /data1/Sequence/ucsc_hg19/annot/dbsnp_135.hg19.G5A_snv.Exon.sort.vcf

def get_snps(dbsnp='/data1/Sequence/ucsc_hg19/annot/dbsnp_135.hg19.G5A_snv.Exon.sort.vcf'):
	snpH = {}
	inFile = open(dbsnp, 'r')
	for line in inFile:
		colL = line.rstrip().split('\t')
		chrom = colL[0]
		pos = int(colL[1])
		ref = colL[3]
		alt = colL[4]
		if chrom in snpH:
			if pos in snpH[chrom]:
				snpH[chrom][pos].add(alt)
			else:
				snpH[chrom][pos] = set(alt)
		else:
			snpH[chrom] = {}
			snpH[chrom][pos] = set(alt)
	return(snpH)

def get_alt_frac_mutscan(sampN, snpH, fileL):
	outH = {}

	for chrom in snpH:
		for pos in snpH[chrom]:
			outH[(chrom, pos)] = {}
			for alt in snpH[chrom][pos]:
				outH[(chrom,pos)][alt] = 'NA'
	
	chromL = snpH.keys()
	chromL.sort()

	for file in fileL:
		inFile = open(file, 'r')
		prevChr = ''
		posL = []
		for line in inFile:
			colL = line.rstrip().split('\t')
			chrom = colL[0]
			pos = int(colL[1])
			alt = colL[3]
			r1 = int(colL[4])
			r2 = int(colL[5])
			frac = float(colL[6])
			if chrom == 'chrM' or (r1 + r2) < 15:
				continue
			if prevChr != chrom:
				prevChr = chrom
				posL = snpH[chrom].keys()
				posL.sort()
			idx = mybasic.index(posL, pos)
			if idx >= 0 and alt in snpH[chrom][pos]: ## mutation is in dbsnp
				outH[(chrom,pos)][alt] = frac
		##for line
	##for file
				
	for chrom in chromL:
		posL = snpH[chrom].keys()
		posL.sort()
		for pos in posL:
			altL = list(snpH[chrom][pos])
			for alt in altL:
				sys.stdout.write('%s\t%s:%s:%s\t%s\n' % (sampN, chrom,pos,alt, outH[(chrom,pos)][alt]))

def get_alt_frac(sampN, snpH, pileup_procL):
	outH = {} ## alternative allele fractions

	for chrom in snpH:
		for pos in snpH[chrom]:
			outH[(chrom, pos)] = {}
			for alt in snpH[chrom][pos]:
				outH[(chrom,pos)][alt] = 'NA'
	
	chromL = snpH.keys()
	chromL.sort()

	for chrom in chromL:
		posL = snpH[chrom].keys()
		posL.sort()
		fileN = filter(lambda x: '_%s.pileup_proc' % chrom in x, pileup_procL)[0]
		inFile = open(fileN, 'r')
		for line in inFile:
			colL = line.rstrip().split(',')
			[chrom, pos] = colL[0].split(':')
			pos = int(pos)
			if len(posL) < 1:
				break
			if pos < posL[0]:
				continue
			elif pos == posL[0]:
				del posL[0]
				cov = int(colL[1])
				if cov < 1:
					continue
				ref = colL[2]
				n_ref = int(colL[3])
				for alt in snpH[chrom][pos]:
					n_alt = colL[4].count(alt)
					frac = float(n_alt)/float(cov)
					outH[(chrom,pos)][alt] = frac
			elif pos > posL[0]:
				del posL[0]
		##for line
	##for chrom

	for chrom in chromL:
		posL = snpH[chrom].keys()
		posL.sort()
		for pos in posL:
			altL = list(snpH[chrom][pos])
			for alt in altL:
				sys.stdout.write('%s\t%s:%s:%s\t%s\n' % (sampN, chrom,pos,alt, outH[(chrom,pos)][alt]))

if __name__ == '__main__':
#	filter_dbsnp() ## run only once when 'dbsnp' changed
	optL, argL = getopt.getopt(sys.argv[1:],'s:i:',[])
	optH = mybasic.parseParam(optL)

	snpH = get_snps()
	if optH['-i'][-11:] == 'pileup_proc':
		get_alt_frac(sampN=optH['-s'], snpH=snpH, pileup_procL=glob(optH['-i']))
	elif optH['-i'][-7:] == 'mutscan':
		get_alt_frac_mutscan(sampN=optH['-s'], snpH=snpH, fileL=glob(optH['-i']))
