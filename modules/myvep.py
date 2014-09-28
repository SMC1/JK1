#!/usr/bin/python

import sys, os, re
from glob import glob

FORMAT = "Allele|Gene|Feature|Feature_type|Consequence|cDNA_position|CDS_position|Protein_position|Amino_acids|Codons|Existing_variation|AA_MAF|EA_MAF|RefSeq|EXON|INTRON|MOTIF_NAME|MOTIF_POS|HIGH_INF_POS|MOTIF_SCORE_CHANGE|DISTANCE|CLIN_SIG|CANONICAL|SYMBOL|SIFT|PolyPhen|GMAF|DOMAINS|HGVSc|HGVSp|AFR_MAF|AMR_MAF|ASN_MAF|EUR_MAF"

def shorten_csq(csq):
	map = {'splice_region_variant&intron_variant': 'splice_region_variant', 'splice_region_variant&non_coding_exon_variant&nc_transcript_variant': 'nc_transcript_variant',\
			'non_coding_exon_variant&nc_transcript_variant':'nc_transcript_variant', 'intron_variant&nc_transcript_variant':'nc_transcript_variant',
			'splice_region_variant&intron_variant&nc_transcript_variant':'nc_transcript_variant','splice_donor_variant&nc_transcript_variant':'nc_transcript_variant',
			'splice_acceptor_variant&nc_transcript_variant':'nc_transcript_variant'
		}
	#res = csq.replace('&NMD_transcript_variant', '').replace('&nc_transcript_variant','').replace('&non_coding_exon_variant','')
	res = csq.replace('&NMD_transcript_variant', '').replace('&splice_region_variant','').replace('&feature_truncation','').replace('&feature_elongation','').replace('&intron_variant','')

	if res in map:
		res = map[res]
	else:
		res = res
	
	return res

def parse_vcf(infoS):
	itemL = infoS.split(';')
	item_newL = []
	old = ''
	for i in range(len(itemL)):
		item = itemL[i]
		if item[:2] == 'DB' or item[:4] == 'KGPF' or item[:4]:
			if old != '':
				item_newL.append(old)
	infoH = {}
	for item in itemL:
		if '=' in item:
			tag = item.split('=')[0]
			val = item.split('=')[1]
			infoH[tag] = val
		else:
			infoH[item] = True
	return(infoH)

def change_AA(inS):
	codonH = {'Phe':'F', 'Leu':'L', 'Ile':'I', 'Met':'M', 'Val':'V', 'Ser':'S', 'Pro':'P', 'Thr':'T', 'Ala':'A', 'Tyr':'T', 'Ter':'*', 'His':'H', 'Gln':'G', 'Asn':'A', 'Lys':'K', 'Asp':'D', 'Glu':'E', 'Cys':'C', 'Trp':'W', 'Arg':'R', 'Gly':'G'}
	outS = inS
	for aa in codonH:
		outS = outS.replace(aa, codonH[aa])
	return(outS)

def parse_info(info, ref, indexH):
	itemL = info.split(',')
	resL = []
	for item in itemL:
		cur = {'gene':'-','tid':'','ch_type':'','ch_dna':'','ch_prot':'','canonical':'NO', 'strand':'*', 'refseq':'-'}
		arr = item.split('|')
#		print item
		cur['gene'] = arr[indexH['SYMBOL']]
		cur['tid'] = arr[indexH['Feature']]
		if arr[indexH['CANONICAL']] == 'YES':
			cur['canonical'] = arr[indexH['CANONICAL']]
			cur['refseq'] = arr[indexH['RefSeq']]
		cur['ch_type'] = shorten_csq(arr[indexH['Consequence']])
		if len(arr[indexH['HGVSc']]) > 0:
			cur['ch_dna'] = arr[indexH['HGVSc']].split(':')[1]
		if len(arr[indexH['HGVSp']]) > 0:
			cur['ch_prot'] = change_AA(arr[indexH['HGVSp']].split(':')[1])

		resL.append(cur)
	return(resL)

def get_vep_format():
	format = FORMAT.split('|')
	idxH = {}
	for i in range(0,len(format)):
		idxH[format[i]] = i
	return(idxH)

def process_vep_vcf(inFileN, sampN, outFileN):
	inFile = open(inFileN)
	outFile = open(outFileN, 'w')
	idxH = get_vep_format()
	for line in inFile:
		if line[0] == '#' or 'REJECT' in line:
			continue

		colL = line.rstrip().split('\t')
		chr = colL[0]
		if chr.upper() == 'MT':
			chr = 'M'
		pos = int(colL[1])
		ref = colL[3]
		alt = colL[4]
		formatL = colL[8].split(':')
		idx_t = 9
		idx_n = 10
		t_datL = colL[idx_t].split(':')
		AD = t_datL[formatL.index('AD')]
		if AD == '0,0': ## find more elegant way to distinguish tumor & normal
			idx_t = 10
			idx_n = 9
			t_datL = colL[idx_t].split(':')
			AD = t_datL[formatL.index('AD')]

		t_nRef = int(AD.split(',')[0])
		t_nAlt = int(AD.split(',')[1])
		n_nRef = 0
		n_nAlt = 0
		if len(colL) > 10:
			n_datL = colL[idx_n].split(':')
			n_AD = n_datL[formatL.index('AD')]
			n_nRef = int(n_AD.split(',')[0])
			n_nAlt = int(n_AD.split(',')[1])

		infoH = parse_vcf(colL[7])
		annotH = parse_info(infoH['CSQ'], ref, idxH)
		for annot in annotH:
			outFile.write('%s\tchr%s\t%s\t%s\t%s' % (sampN, chr, pos, ref, alt))
			outFile.write('\t%s\t%s\t%s\t%s' % (n_nRef, n_nAlt, t_nRef, t_nAlt))
			outFile.write('\t%s\t%s\t%s\t%s\t%s\t%s\n' % (annot['gene'], annot['ch_dna'], annot['ch_prot'], annot['ch_type'], annot['canonical'], annot['refseq']))
	#line
	outFile.flush()
	outFile.close()

if __name__ == '__main__':
	process_vep_vcf('/EQL5/pipeline/CS_mut/IRCR_GBM14_479_T_CS/IRCR_GBM14_479_T_CS_mutect_vep.vcf', 'IRCR_GBM14_479_T_CS', 'hhhh')
