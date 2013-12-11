#!/usr/bin/python

import sys, os, re
import mybasic

FORMAT = "Allele|Gene|Feature|Feature_type|Consequence|cDNA_position|CDS_position|Protein_position|Amino_acids|Codons|Existing_variation|AA_MAF|EA_MAF|RefSeq|EXON|INTRON|MOTIF_NAME|MOTIF_POS|HIGH_INF_POS|MOTIF_SCORE_CHANGE|DISTANCE|CLIN_SIG|CANONICAL|SYMBOL|SIFT|PolyPhen|GMAF|DOMAINS|HGVSc|HGVSp|AFR_MAF|AMR_MAF|ASN_MAF|EUR_MAF"
#CHROM  POS ID  REF ALT QUAL    FILTER  INFO
#outField = ('Consequence','cDNA_position','CDS_position','Protein_position','Amino_acids','Codons','EXON','INTRON','DISTANCE','SYMBOL','Existing_variation','MOTIF_NAME','MOTIF_POS','HIGH_INF_POS','MOTIF_SCORE_CHANGE','DOMAINS','SIFT','PolyPhen','GMAF','AA_MAF','EA_MAF','AFR_MAF','AMR_MAF','ASN_MAF','EUR_MAF','CLIN_SIG','CANONICAL','HGVSc','HGVSp')
outField = ('SYMBOL','Consequence','HGVSc','HGVSp','EXON','INTRON','DISTANCE','Existing_variation','MOTIF_NAME','MOTIF_POS','HIGH_INF_POS','MOTIF_SCORE_CHANGE','DOMAINS','SIFT','PolyPhen','GMAF','AA_MAF','EA_MAF','AFR_MAF','AMR_MAF','ASN_MAF','EUR_MAF','CLIN_SIG','CANONICAL')

excField = ('Allele','Feature_type','Gene','Feature', 'RefSeq')
sglField = ('SYMBOL','Existing_variation','GMAF','AA_MAF','EA_MAF','AFR_MAF','AMR_MAF','ASN_MAF','EUR_MAF','DOMAINS')

REFSEQ = sorted(map(lambda x: x[:-1], os.popen('cut -f 1 /data1/Sequence/ucsc_hg19/annot/refFlat.txt | sort | uniq').readlines()))

def parse_info(info, ref, indexH):
	itemL = info.split(',')
	resH = {}
	for item in itemL:
		arr = item.split('|')
		if arr[indexH['Feature_type']] != 'Transcript':
			continue

		aa = arr[indexH['Amino_acids']]
		if aa == '':
			continue

		gene = arr[indexH['SYMBOL']]
		if gene not in REFSEQ:
			continue
		if arr[indexH['RefSeq']] == '':
			continue
		if gene not in resH:
			resH[gene] = {}
		cds_pos = arr[indexH['CDS_position']]
		codon = arr[indexH['Codons']]
		(nt1,nt2)=re.match('[acgt]*([ACGT])[acgt]*/[acgt]*([ACGT])[acgt]*', codon).group(1,2)
		ch_dna = 'c.%s%s>%s' % (cds_pos, nt1, nt2)
		if ref != nt1:
			strand = '-'
		else:
			strand = '+'
		prot_pos = arr[indexH['Protein_position']]
		if len(aa) < 2:
			ch_aa = 'p.%s%s%s' % (aa, prot_pos, aa)
		else:
			AAs = aa.split('/')
			ch_aa = 'p.%s%s%s' % (AAs[0], prot_pos, AAs[1])
		csq = arr[indexH['Consequence']]
		mybasic.pushHash(resH[gene], 'strand', strand)
		mybasic.pushHash(resH[gene], 'ch_type', csq)
		mybasic.pushHash(resH[gene], 'ch_aa', ch_aa)
		mybasic.pushHash(resH[gene], 'ch_dna', ch_dna)
	return resH

def parse_vep(inFileName):
	format=FORMAT.split('|')
	idxH = {}
	for i in range(0,len(format)):
		idxH[format[i]] = i

	outH = {}
	inFile = open(inFileName, 'r')
	cnt = 0
	while True:
		line = inFile.readline().rstrip()
		if len(line) < 1:
			break
		if line[0] == '#':
			continue

		cnt += 1
		cols = line.split('\t')
		chr = cols[0]
		if chr.upper() == 'MT':
			chr = 'M'
		pos = cols[1]
		ref = cols[3]
		alt = cols[4]
		info = cols[7].split(';')
		if len(info) > 1:
			csq = info[1].split('=')[1]
		else:
			csq = info[0].split('=')[1]
		#outH[(chr,pos,ref,alt)] = parse_info_old(csq, idxH)
		outH[(chr,pos,ref,alt)] = parse_info(csq, ref, idxH)
	inFile.close()
	return outH

def parse_info_old(info, indexH):
	itemL = info.split(',')
	resH = {}
	for item in itemL:
		arr = item.split('|')
		if arr[indexH['Consequence']] == 'regulatory_region_variant': ## exclude variants in regulatory region (for now)
			continue
		key = arr[indexH['Gene']]
		tid = arr[indexH['Feature']]
		if key in resH.keys():
			if tid != '':
				if tid in resH[key]['tid']:
					##something wrong!!
					print info
					sys.exit(1)
				else:
					tnum = len(resH[key]['tid']) + 1
					resH[key]['tid'][tid] = str(tnum)+":"+tid
			else:
				tnum = 1
			##
			for k in indexH.keys():
				if arr[indexH[k]] != '':
					if k in excField:
						continue
					elif k in sglField:
						mybasic.pushHash(resH[key], k, arr[indexH[k]])
					else:
						if tid == '':
							mybasic.pushHash(resH[key], k, arr[indexH[k]])
						else:
							if k == 'HGVSc' or k == 'HGVSp':
								val = arr[indexH[k]].split(':')[1]
								mybasic.pushHash(resH[key], k, str(tnum)+"="+val)
							else:
								mybasic.pushHash(resH[key], k, str(tnum)+"="+arr[indexH[k]])
		else:
			resH[key] = {}
			resH[key]['tid'] = {}
			if tid != '':
				tnum = len(resH[key]['tid'])+1
				resH[key]['tid'][tid] = str(tnum)+":"+tid
			for k in indexH.keys():
				if arr[indexH[k]] != '':
					if k in excField:
						continue
					elif k in sglField:
						mybasic.pushHash(resH[key], k, arr[indexH[k]])
					else:
						if tid == '':
							mybasic.pushHash(resH[key], k, arr[indexH[k]])
						else:
							if k == 'HGVSc' or k == 'HGVSp':
								val = arr[indexH[k]].split(':')[1]
								mybasic.pushHash(resH[key], k, str(tnum)+"="+val)
							else:
								mybasic.pushHash(resH[key], k, str(tnum)+"="+arr[indexH[k]])
	return resH

def parse_vep_old(inFileName):
	format=FORMAT.split('|')
	idxH = {}
	for i in range(0,len(format)):
		idxH[format[i]] = i

	outH = {}
	inFile = open(inFileName, 'r')
	cnt = 0
	while True:
		line = inFile.readline().rstrip()
		if len(line) < 1:
			break
		if line[0] == '#':
			continue

		cnt += 1
		cols = line.split('\t')
		chr = cols[0]
		if chr.upper() == 'MT':
			chr = 'M'
		pos = cols[1]
		ref = cols[3]
		alt = cols[4]
		info = cols[7].split(';')
		if len(info) > 1:
			csq = info[1].split('=')[1]
		else:
			csq = info[0].split('=')[1]
		outH[(chr,pos,ref,alt)] = parse_info_old(csq, idxH)
		cur = outH[(chr,pos,ref,alt)]
	inFile.close()
	return outH

def print_vep_old(inH, outFileName, colL=outField):
	outFile = open(outFileName, 'w')
	for (chr,pos,ref,alt) in inH.keys():
		for gene in inH[(chr,pos,ref,alt)].keys():
			outFile.write( 'chr%s\t%s\t%s\t%s\t%s' % (chr,pos,ref,alt,gene))
			cur = inH[(chr,pos,ref,alt)][gene]
			if len(cur['tid']) > 0:
				outFile.write('\t%s' % ','.join(cur['tid'].values()))
			else:
				outFile.write('\t')
			for col in colL:
				if col in cur.keys():
					outFile.write( '\t%s' % ','.join(cur[col]))
				else:
					outFile.write( '\t')
			outFile.write( '\n')
	outFile.flush()
	outFile.close()

if __name__ == '__main__':
	tmp = parse_vep('/EQL3/pipeline/somatic_mutect/S012_T_SS.mutect_vep_out.vcf')
	print tmp
	#/EQL3/pipeline/somatic_mutect/S012_T_SS.mutect_vep_out.vcf
#	temp=parse_vep('/home/ihlee/JK1/modules/test_out.vcf')
#	print_vep(temp)
