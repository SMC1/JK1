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

def shorten_csq(csq):
	map = {'splice_region_variant&intron_variant': 'splice_region_variant', 'splice_region_variant&non_coding_exon_variant&nc_transcript_variant': 'nc_transcript_variant',\
			'non_coding_exon_variant&nc_transcript_variant':'nc_transcript_variant', 'intron_variant&nc_transcript_variant':'nc_transcript_variant',
			'splice_region_variant&intron_variant&nc_transcript_variant':'nc_transcript_variant','splice_donor_variant&nc_transcript_variant':'nc_transcript_variant',
			'splice_acceptor_variant&nc_transcript_variant':'nc_transcript_variant'
		}
	#res = csq.replace('&NMD_transcript_variant', '').replace('&nc_transcript_variant','').replace('&non_coding_exon_variant','')
	res = csq.replace('&NMD_transcript_variant', '')

	if res in map:
		res = map[res]
	else:
		res = res
	
	return res

def parse_info(info, ref, indexH):
	itemL = info.split(',')
	resH = {}
	for item in itemL:
		arr = item.split('|')
		if arr[indexH['Feature_type']] == 'RegulatoryFeature':
			gene = '-'
			if gene not in resH:
				resH[gene] = {'ch_type':''}
			mybasic.pushHash(resH[gene], 'ch_type', arr[indexH['Consequence']])
			mybasic.pushHash(resH[gene], 'strand', '*')

		elif arr[indexH['Feature_type']] == 'MotifFeature' and (arr[indexH['Consequence']] == 'TF_binding_site_variant' or 'TFBS_' in arr[indexH['Consequence']]):
			gene = '-'
			if gene not in resH:
				resH[gene] = {'ch_type':''}
			mybasic.pushHash(resH[gene], 'ch_type', arr[indexH['Consequence']])
			mybasic.pushHash(resH[gene], 'strand', '*')

		elif arr[indexH['Feature_type']] == '' and (arr[indexH['Consequence']] == 'intergenic_variant'):
			gene = '-'
			if gene not in resH:
				resH[gene] = {'ch_type':''}
			mybasic.pushHash(resH[gene], 'ch_type', arr[indexH['Consequence']])
			mybasic.pushHash(resH[gene], 'strand', '*')

		elif arr[indexH['Feature_type']] == 'Transcript':
			csq = arr[indexH['Consequence']]
#			if ('non_coding_exon_variant' in csq or 'nc_transcript_variant' in csq) and 'splice_' not in csq and 'miRNA' not in csq:
#				continue ## non-coding scripts other than miRNA
			if ('upstream_gene_variant' in csq or 'downstream_gene_variant' in csq) and 'splice_' not in csq:
				gene = '-'
				if gene not in resH:
					resH[gene] = {'ch_type':''}
				## treat up-, down-stream gene variants as intergenic
				mybasic.pushHash(resH[gene], 'strand', '*')
				mybasic.pushHash(resH[gene], 'ch_type', 'intergenic_variant')
				continue
#			if 'intron_variant' in csq and 'splice_' not in csq:
#				continue ## intron

			csq = shorten_csq(csq)

			gene = arr[indexH['SYMBOL']]
			if gene not in resH:
				resH[gene] = {'ch_type':''}
			ch_dna = arr[indexH['HGVSc']]
			if len(ch_dna.split(':')) > 1:
				ch_dna = ch_dna.split(':')[1]
			prot_pos = arr[indexH['Protein_position']]
			aa = arr[indexH['Amino_acids']]
			if len(aa) < 1:
#				if len(prot_pos) > 0:
#					print info
#					print 'AA:%s' % item
#					raise Exception
				ch_aa = ''
			elif '/' not in aa:
#			elif len(aa) < 2:
				ch_aa = 'p.%s%s%s' % (aa, prot_pos, aa)
			else:
				(aa1, aa2) = aa.split('/')
				ch_aa = 'p.%s%s%s' % (aa1, prot_pos, aa2)
			codon = arr[indexH['Codons']]
			if len(codon) > 0:
				(nt1,nt2) = re.match('[nacgt]*([-ACGT]*)[nacgt]*/[nacgt]*([-ACGT]*)[nacgt]*', codon).group(1,2)
				if ref != nt1:
					strand = '-'
				else:
					strand = '+'
				if 'strand' in resH[gene]:
					try:
						resH[gene]['strand'].remove('*')
					except:
						pass
				mybasic.pushHash(resH[gene], 'strand', strand)
			else:
				if 'strand' not in resH[gene]:
					mybasic.pushHash(resH[gene], 'strand', '*')
			if len(csq) > 0:
				if len(arr[indexH['CANONICAL']]) > 0:
					mybasic.pushHash(resH[gene], 'ch_type_C', csq)
				mybasic.pushHash(resH[gene], 'ch_type', csq)
			if len(ch_aa) > 0 and 'nc_transcript_' not in csq and 'non_coding_' not in csq:
				if len(arr[indexH['CANONICAL']]) > 0:
					mybasic.pushHash(resH[gene], 'ch_aa_C', ch_aa)
				mybasic.pushHash(resH[gene],'ch_aa', ch_aa)
			if len(ch_dna) > 0 and 'nc_transcript_' not in csq and 'non_coding_' not in csq:
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
		csq=''
		for tag in info:
			if len(tag.split('=')) > 1 and tag.split('=')[0] == 'CSQ':
				csq = tag.split('=')[1]
		#outH[(chr,pos,ref,alt)] = parse_info_old(csq, idxH)
		tmpH = parse_info(csq, ref, idxH)
		if len(tmpH) > 0:
			outH[(chr,pos,ref,alt)] = tmpH
	inFile.close()
	return outH

def parse_vep_line(line):
	format = FORMAT.split('|')
	idxH = {}
	for i in range(0,len(format)):
		idxH[format[i]] = i
	
	cols = line.rstrip().split('\t')
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

	tmpH = parse_info(csq, ref, idxH)
	res = (chr, pos, ref, alt, tmpH)
	return(res)

def print_vep_type_item(itemH):
	if '-' in itemH:
		hasReg = True
	else:
		hasReg = False
	
	outH = {}
	if hasReg and len(itemH) == 1: ## regulatory only
		ch_type = ','.join(itemH['-']['ch_type'])
		if 'TF_binding_site_' in ch_type or 'TFBS_' in ch_type:
			out_type = 'TF_binding_site_variant'
		else:
			out_type = ch_type
		outH['-'] = out_type
		return outH
	else:
		for gene in itemH:
			if gene == '-':
				continue
			ch_type = ','.join(itemH[gene]['ch_type'])
			if hasReg:
				if 'TF_binding_site_' in ch_type or 'TFBS_' in ch_type:
					reg_type = 'TF_binding_site_variant'
				else:
					reg_type = 'regulatory_region_variant'
				ch_type = '%s,%s' % (ch_type, reg_type)
			outH[gene] = ch_type
		return outH
	##if

def print_vep_item(itemH):
	nc_type = ''

	if '-' in itemH:
		nc_type = ','.join(itemH['-']['ch_type'])
		if 'TF_binding_site_' in nc_type or 'TFBS_' in nc_type or 'regulatory_region_' in nc_type:
			hasReg = True
		else:
			hasReg = False
	else:
		hasReg = False

	outH = {}
	
	if '-' in itemH and len(itemH) == 1: ## regulatory feature or intergenic
		outH['-'] = {}
		ch_type = ','.join(itemH['-']['ch_type'])
		if 'TF_binding_site_' in ch_type or 'TFBS_' in ch_type:
			out_type = 'TF_binding_site_variant'
		elif 'regulatory_region_variant' in ch_type:
			out_type = 'regulatory_region_variant'
		else:
			out_type = 'intergenic_variant'
		outH['-']['ch_type'] = out_type
		outH['-']['ch_dna'] = ''
		outH['-']['ch_aa'] = ''
		outH['-']['strand'] = '*'
	else:
		for gene in itemH:
			if gene == '-':
				continue
			outH[gene] = {}
			ch_type = ','.join(itemH[gene]['ch_type'])
			if hasReg:
				if 'TF_binding_site_' in nc_type or 'TFBS_' in nc_type:
					ch_type = ch_type + ',TF_binding_site_variant'
				elif 'regulatory_region_variant' in nc_type:
					ch_type = ch_type + ',regulatory_region_variant'
			outH[gene]['ch_type'] = ch_type
			if 'ch_dna' in itemH[gene]:
				ch_dna = ','.join(itemH[gene]['ch_dna'])
			else:
				ch_dna = ''
			outH[gene]['ch_dna'] = ch_dna
			if 'ch_aa' in itemH[gene]:
				ch_aa = ','.join(itemH[gene]['ch_aa'])
			else:
				ch_aa = ''
			outH[gene]['ch_aa'] = ch_aa
			outH[gene]['strand'] = ','.join(itemH[gene]['strand'])
	return outH

def print_vep(vepH, outFileN='', cntH={}, sampN=''):
	if sampN != '' and len(cntH) < 1:
		print 'myvep.print_vep():: You must provide count data!!'
		print 'myvep.print_vep():: ' + outFileN
		sys.exit(1)

	if outFileN != '':
		outF = open(outFileN, 'w')
	else:
		outF = sys.stdout
	
	for var in vepH:
		(chr, pos, ref, alt) = var
		summaryH = print_vep_item(vepH[var])

		if '-' in vepH[var]:
			hasReg = True
		else:
			hasReg = False

		if hasReg and len(vepH[var]) == 1: ## regulatory only
			if sampN != '':
				chr_tmp = chr
				if chr == 'M':
					chr_tmp = 'MT'
				if (chr_tmp,int(pos),ref,alt) not in cntH:
					print 'myvep.print_vep():: Conflict between VEP & count data!!'
					print 'myvep.print_vep():: Can\'t find (%s, %s, %s, %s) from count data' % var
					sys.exit(1)
				(t_ref,t_alt,n_ref,n_alt) = cntH[(chr_tmp,int(pos),ref,alt)]
				outF.write('%s\tchr%s\t%s\t%s\t%s\t%s' % (sampN, chr, pos, pos, ref, alt))
				outF.write('\t%s\t%s\t%s\t%s' % (n_ref, n_alt, t_ref, t_alt))
				outF.write('\t\t\t\t\t%s\n' % summaryH['-']['ch_type'])
			else:
				outF.write('%s\t%s\t%s\t%s\t' % (chr, pos, ref, alt))
				outF.write('\t\t\t%s\n' % summaryH['-']['ch_type'])
		else:
			for gene in vepH[var]:
				if gene == '-':
					continue
				if sampN != '':
					chr_tmp = chr
					if chr == 'M':
						chr_tmp = 'MT'
					if (chr_tmp,int(pos),ref,alt) not in cntH:
						print 'myvep.print_vep():: Conflict between VEP & count data!!'
						print 'myvep.print_vep():: Can\'t find (%s, %s, %s, %s) from count data' % var
						sys.exit(1)
					(t_ref,t_alt,n_ref,n_alt) = cntH[(chr_tmp,int(pos),ref,alt)]
					outF.write('%s\tchr%s\t%s\t%s\t%s\t%s' % (sampN, chr, pos, pos, ref, alt))
					outF.write('\t%s\t%s\t%s\t%s' % (n_ref, n_alt, t_ref, t_alt))
					outF.write('\t%s\t%s\t%s\t%s\t%s\n' % (summaryH[gene]['strand'], gene, summaryH[gene]['ch_dna'], summaryH[gene]['ch_aa'], summaryH[gene]['ch_type']))
				else:
					outF.write('%s\t%s\t%s\t%s\t%s' % (chr, pos, ref, alt, gene))
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

def process_vep(inFileN, outFileN):
	outFile = open(outFileN, 'w')
	vepH = parse_vep(inFileN)
	for (chr,pos,ref,alt) in vepH:
		cur = vepH[(chr,pos,ref,alt)]
		chr_tmp = chr
		if chr == 'M':
			chr_tmp = 'MT'
		infoH = print_vep_item(cur)
		for gene in infoH:
			outFile.write('chr%s\t%s\t%s\t%s\t%s' % (chr_tmp, pos, pos, ref, alt))
			if gene == '-':
				out_gene = ''
			else:
				out_gene = gene
			outFile.write('\t%s\t%s\t%s\t%s\t%s\n' % (infoH[gene]['strand'], out_gene, infoH[gene]['ch_dna'], infoH[gene]['ch_aa'], infoH[gene]['ch_type']))
	outFile.flush()
	outFile.close()


if __name__ == '__main__':
	tmp = parse_vep('/EQL3/pipeline/somatic_mutect/S012_T_SS.mutect_vep_out.vcf')
	print_vep(tmp)
	#/EQL3/pipeline/somatic_mutect/S012_T_SS.mutect_vep_out.vcf
#	temp=parse_vep('/home/ihlee/JK1/modules/test_out.vcf')
#	print_vep(temp)
