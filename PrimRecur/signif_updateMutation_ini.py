#!/usr/bin/python

import sys, os, re, getopt
import mybasic, mygenome

def parse_line(datH, idH, lineS):
	colL = lineS.rstrip().split('\t')
	resH = {}
	for col in ['strand','ch_dna','ch_aa','ch_type','cosmic','mutsig','p_mt','p_wt','r_mt','r_wt','n_mt','n_wt']:
		resH[col] = colL[idH[col]]
	
	pair = colL[idH['sId_pair']]
	rm = re.match('(chr[^:]*):([0-9]*)~([0-9]*)',colL[idH['locus']])
	(chrom,chrSta,chrEnd) = rm.groups()
	ref = colL[idH['ref']]
	alt = colL[idH['alt']]
	key = (chrom, chrSta, chrEnd, ref, alt)
	gene = colL[idH['gene_symL']]
	if pair in datH:
		if key in datH[pair]:
			if gene in datH[pair][key]:
				pass # duplicated lines -- do nothing
			else:
				datH[pair][key][gene] = resH
		else:
			datH[pair][key] = {}
			datH[pair][key][gene] = resH
	else:
		datH[pair] = {}
		datH[pair][key] = {}
		datH[pair][key][gene] = resH

def main(inFileName,outFileName,pileupDirL,mutectDirL=[]):

	inFile = open(inFileName)
	if outFileName == '':
		outFile = sys.stdout
	else:
		outFile = open(outFileName,'w')

	header = inFile.readline()
	hcolL = header.rstrip().split('\t')
	idxH = {}
	for i in range(len(hcolL)):
		idxH[hcolL[i]] = i
	outFile.write(header)

	outH = {}
	for line in inFile:

		tokL = line[:-1].split('\t')
		pair = tokL[idxH['sId_pair']]
		rm = re.match('(chr[^:]*):([0-9]*)~([0-9]*)',tokL[2])
		(chrom,chrSta,chrEnd) = rm.groups()
		refAllele = tokL[3]
		altAllele = tokL[4]

		if pair not in outH:
			print_dat(outH, outFile)
			outH = {}

		if tokL[-3]==tokL[-4]=='0':
			flag = 0 # Recur
		elif tokL[-5]==tokL[-6]=='0':
			flag = 1 # Prim
		else:
			parse_line(outH, idxH, line)
			continue
			
		if int(chrEnd)-int(chrSta)!=0:
			parse_line(outH, idxH, line)
			continue

		#print tokL[1], tokL[2], refAllele, '>', altAllele, tokL[-4:],

		sId = tokL[1].split('-')[1-flag]

		if tokL[-1] != '0' or tokL[-2] != '0': ##has matched normal 
			fileNL = []
			for mutDir in mutectDirL:
				fileNL += filter(lambda x: 'backup' not in x, os.popen('find %s -name *%s*union_pos.mutect' % (mutDir, sId[1:])).readlines())
			if len(fileNL) > 1:
				print 'Mutiple files: %s' % ','.join(fileNL)
				sys.exit(1)
			fileN = fileNL[0].rstrip()
			lines = os.popen('grep -w %s %s | grep -w %s | cut -f 1,2,4,5,21,22' % (chrom, fileN, chrSta)).readlines()
			for ln in lines:
				colL = ln.rstrip().split('\t')
				ref = colL[2]
				alt = colL[3]
				if ref == refAllele and alt == altAllele:
					result = []
					result.append(colL[5])
					result.append(colL[4])
		else:
			result = mygenome.lookupPileup(pileupDirL,sId,chrom,chrSta,refAllele,altAllele)
		
		if result:

			tokL[-1-flag*2-2] = str(result[1])
			tokL[-2-flag*2-2] = str(result[0])
			parse_line(outH, idxH, '\t'.join(tokL) + '\n')
		else:
			parse_line(outH, idxH, line)
	print_dat(outH, outFile)

def print_dat(outH, outFile):
	for pair in outH:
		for var in outH[pair]:
			(chr, sta, end, ref, alt) = var
			annot = outH[pair][var]
			locus = chr + ':' + sta + '~' + end + ref + '>' + alt
			if len(annot) > 1: ## more than 2 genes
				geneStr = ';'.join(annot.keys())
				typeL = []
				typeSet = set()
				aaL = []
				dnaL = []
				strandSet = set()
				cosmicSet = set()
				mutsigSet = set()
				otherSet = set()
				for gene in annot:
					if annot[gene]['ch_type'] != '':
						typeL.append(gene + ':' + annot[gene]['ch_type'])
						typeSet.add(annot[gene]['ch_type'])
					if annot[gene]['ch_aa'] != '':
						aaL.append(gene + ':' + annot[gene]['ch_aa'])
					if annot[gene]['ch_dna'] != '':
						dnaL.append(gene + ':' + annot[gene]['ch_dna'])
					strandSet.add(annot[gene]['strand'])
					if annot[gene]['cosmic'] != '':
						cosmicSet.add(annot[gene]['cosmic'])
					if annot[gene]['mutsig'] != '':
						mutsigSet.add(annot[gene]['mutsig'])
					other = ''
					for col in ['p_mt','p_wt','r_mt','r_wt','n_mt','n_wt']:
						other = '%s\t%s' % (other, annot[gene][col])
					otherSet.add(other)
				if len(strandSet) > 1 and '*' in strandSet:
					strandSet.remove('*')
				outFile.write('mutation_normal\t%s\t%s\t%s\t%s' % (pair, locus, ref, alt))
				outFile.write('\t%s\t%s\t%s\t%s' % (';'.join(strandSet), geneStr, ';'.join(dnaL), ';'.join(aaL)))
				if len(typeSet) == 1:
					outFile.write('\t%s' % ','.join(typeSet))
				else:
					outFile.write('\t%s' % ';'.join(typeL))
				outFile.write('\t%s\t%s' % (','.join(cosmicSet), ','.join(mutsigSet)))
				if len(otherSet) == 1:
					outFile.write('%s' % ','.join(otherSet))
				else: ## something wrong
					print ''
					for i in otherSet:
						print i
					print 'something wrong'
					sys.exit(1)
				outFile.write('\n')
			else:
				for gene in annot:
					outFile.write('mutation_normal\t%s\t%s\t%s\t%s\t%s\t%s' % (pair, locus, ref, alt, annot[gene]['strand'], gene))
					for col in ['ch_dna','ch_aa','ch_type','cosmic','mutsig','p_mt','p_wt','r_mt','r_wt','n_mt','n_wt']:
						outFile.write('\t%s' % annot[gene][col])
					outFile.write('\n')


#optL, argL = getopt.getopt(sys.argv[1:],'i:o:l:',[])
#
#optH = mybasic.parseParam(optL)
#
#if '-i' in optH and '-o' in optH and '-l' in optH:
#
#	main(optH['-i'], optH['-o'], int(optH['-l']))

#dirN='/EQL1/PrimRecur/signif_20140107'
#dirN='/EQL1/PrimRecur/signif_20140121'
#dirN='/EQL1/PrimRecur/signif_20140204'
dirN='/EQL1/PrimRecur/signif_20140214'

#main('/EQL1/PrimRecur/signif/signif_mutation_normal_pre.txt','/EQL1/PrimRecur/signif/signif_mutation_normal.txt',['/EQL1/NSL/WXS/exome_20130529/','/EQL1/NSL/exome_bam/mutation/pileup_proc/','/EQL1/pipeline/ExomeSeq_20130723/'])
main(dirN+'/signif_mutation_normal_pre.txt',dirN+'/signif_mutation_normal.txt', ['/EQL1/NSL/WXS/exome_20130529/','/EQL1/NSL/exome_bam/mutation/pileup_proc/','/EQL1/pipeline/ExomeSeq_20130723/'],['/EQL3/pipeline/somatic_mutect'])
