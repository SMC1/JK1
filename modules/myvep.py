#!/usr/bin/python

import sys, os, re
import mybasic

FORMAT = "Allele|Gene|Feature|Feature_type|Consequence|cDNA_position|CDS_position|Protein_position|Amino_acids|Codons|Existing_variation|AA_MAF|EA_MAF|RefSeq|EXON|INTRON|MOTIF_NAME|MOTIF_POS|HIGH_INF_POS|MOTIF_SCORE_CHANGE|DISTANCE|CLIN_SIG|CANONICAL|SYMBOL|SIFT|PolyPhen|GMAF|DOMAINS|HGVSc|HGVSp|AFR_MAF|AMR_MAF|ASN_MAF|EUR_MAF"
#CHROM  POS ID  REF ALT QUAL    FILTER  INFO
#outField = ('Consequence','cDNA_position','CDS_position','Protein_position','Amino_acids','Codons','EXON','INTRON','DISTANCE','SYMBOL','Existing_variation','MOTIF_NAME','MOTIF_POS','HIGH_INF_POS','MOTIF_SCORE_CHANGE','DOMAINS','SIFT','PolyPhen','GMAF','AA_MAF','EA_MAF','AFR_MAF','AMR_MAF','ASN_MAF','EUR_MAF','CLIN_SIG','CANONICAL','HGVSc','HGVSp')
outField = ('SYMBOL','Consequence','HGVSc','HGVSp','EXON','INTRON','DISTANCE','Existing_variation','MOTIF_NAME','MOTIF_POS','HIGH_INF_POS','MOTIF_SCORE_CHANGE','DOMAINS','SIFT','PolyPhen','GMAF','AA_MAF','EA_MAF','AFR_MAF','AMR_MAF','ASN_MAF','EUR_MAF','CLIN_SIG','CANONICAL')

excField = ('Allele','Feature_type','Gene','Feature', 'RefSeq')
sglField = ('SYMBOL','Existing_variation','GMAF','AA_MAF','EA_MAF','AFR_MAF','AMR_MAF','ASN_MAF','EUR_MAF','DOMAINS')

#REFSEQ = sorted(map(lambda x: x[:-1], os.popen('cut -f 1 /data1/Sequence/ucsc_hg19/annot/refFlat.txt | sort | uniq').readlines()))

def parse_info(info, ref, indexH):
	itemL = info.split(',')
	resH = {}
	for item in itemL:
		arr = item.split('|')
		if arr[indexH['Feature_type']] == 'RegulatoryFeature':
			gene = '-'
			if gene not in resH:
				resH[gene] = {}
			mybasic.pushHash(resH[gene], 'ch_type', arr[indexH['Consequence']])

		elif arr[indexH['Feature_type']] == 'MotifFeature' and (arr[indexH['Consequence']] == 'TF_binding_site_variant' or 'TFBS_' in arr[indexH['Consequence']]):
			gene = '-'
			if gene not in resH:
				resH[gene] = {}
			mybasic.pushHash(resH[gene], 'ch_type', arr[indexH['Consequence']])

		elif arr[indexH['Feature_type']] == 'Transcript':
			csq = arr[indexH['Consequence']]
			if ('non_coding_exon_variant' in csq or 'nc_transcript_variant' in csq) and 'splice_' not in csq:
				continue ## non-coding scripts other than miRNA
			if ('upstream_gene_variant' in csq or 'downstream_gene_variant' in csq or 'intergenic_variant' in csq) and 'splice_' not in csq:
				continue ## outside of gene
			if 'intron_variant' in csq and 'splice_' not in csq:
				continue ## intron

			gene = arr[indexH['SYMBOL']]
			if gene not in resH:
				resH[gene] = {}
			ch_dna = arr[indexH['HGVSc']]
			if len(ch_dna.split(':')) > 1:
				ch_dna = ch_dna.split(':')[1]
			prot_pos = arr[indexH['Protein_position']]
			aa = arr[indexH['Amino_acids']]
			if len(aa) < 1:
				if len(prot_pos) > 0:
					print 'AA:%s' % item
					raise Exception
				ch_aa = ''
			elif len(aa) < 2:
				ch_aa = 'p.%s%s%s' % (aa, prot_pos, aa)
			else:
				(aa1, aa2) = aa.split('/')
				ch_aa = 'p.%s%s%s' % (aa1, prot_pos, aa2)
			codon = arr[indexH['Codons']]
			if len(codon) > 0:
				(nt1,nt2) = re.match('[acgt]*([ACGT])[acgt]*/[acgt]*([ACGT])[acgt]*', codon).group(1,2)
				if ref != nt1:
					strand = '-'
				else:
					strand = '+'
			else:
				strand = '*'
			mybasic.pushHash(resH[gene], 'strand', strand)
			if len(csq) > 0:
				if len(arr[indexH['CANONICAL']]) > 0:
					mybasic.pushHash(resH[gene], 'ch_type_C', csq)
				mybasic.pushHash(resH[gene], 'ch_type', csq)
			if len(ch_aa) > 0:
				if len(arr[indexH['CANONICAL']]) > 0:
					mybasic.pushHash(resH[gene], 'ch_aa_C', ch_aa)
				mybasic.pushHash(resH[gene],'ch_aa', ch_aa)
			if len(ch_dna) > 0:
				if len(arr[indexH['CANONICAL']]) > 0:
					mybasic.pushHash(resH[gene], 'ch_dna_C', ch_dna)
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
		tmpH = parse_info(csq, ref, idxH)
		if len(tmpH) > 0:
			outH[(chr,pos,ref,alt)] = tmpH
	inFile.close()
	return outH

def print_vep(vepH, outFileN=''):
	if outFileN != '':
		outF = open(outFileN, 'w')
	else:
		outF = sys.stdout
	
	for var in vepH:
		(chr, pos, ref, alt) = var
		if '-' in vepH[var]:
			hasReg = True
		else:
			hasReg = False
		if 'ch_type_C' in vepH[var] or 'ch_dna_C' in vepH[var] or 'ch_aa_C' in vepH[var]:
			hasCanonical = True
		else:
			hasCanonical = False

		if hasReg and len(vepH[var]) == 1: ## regulatory only
			ch_type = ','.join(vepH[var]['-']['ch_type'])
			if 'TF_binding_site_' in ch_type or 'TFBS_' in ch_type:
				out_type = 'TF_binding_site_variant'
			else:
				out_type = ch_type

			outF.write('%s\t%s\t%s\t%s\t' % (chr, pos, ref, alt))
#			outF.write('\t\t\t\t\t\t%s\n' % (out_type))
			outF.write('\t\t\t%s\n' % out_type)
		else:
			for gene in vepH[var]:
				if gene == '-':
					continue
				ch_type = ','.join(vepH[var][gene]['ch_type'])
				if 'ch_type_C' in vepH[var][gene]:
					ch_type_c = ','.join(vepH[var][gene]['ch_type_C'])
				else:
					ch_type_c = ''
				if hasReg:
					if 'TF_binding_site_' in ch_type or 'TFBS_' in ch_type:
						reg_type = 'TF_binding_site_variant'
					else:
						reg_type = 'regulatory_region_variant'
					ch_type = '%s,%s' % (ch_type, reg_type)
					ch_type_c = '%s,%s' % (ch_type_c, reg_type)
				outF.write('%s\t%s\t%s\t%s\t%s' % (chr, pos, ref, alt, gene))
				if 'ch_dna' in vepH[var][gene]:
					ch_dna = ','.join(vepH[var][gene]['ch_dna'])
				else:
					ch_dna = ''
				if 'ch_aa' in vepH[var][gene]:
					ch_aa = ','.join(vepH[var][gene]['ch_aa'])
				else:
					ch_aa = ''
				outF.write('\t%s\t%s\t%s\n' % (ch_dna, ch_aa, ch_type))
			#for gene
		#else

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
	print_vep(tmp)
	#/EQL3/pipeline/somatic_mutect/S012_T_SS.mutect_vep_out.vcf
#	temp=parse_vep('/home/ihlee/JK1/modules/test_out.vcf')
#	print_vep(temp)
