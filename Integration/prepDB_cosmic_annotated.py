#!/usr/bin/python

import os, sys, getopt, re
import mybasic

def parse_info(str, indexH):
	itemL = str.split(',')
	resH = {}
	for item in itemL:
		arr = item.split('|')
		if arr[indexH['Feature_type']] != 'Transcript':
			continue
		key = (arr[indexH['Gene']], arr[indexH['Feature']])
		if key in resH.keys():
			print 'Something wrong!!!!!'
			print resH[key]
			print item
			sys.exit(1)
		else:
			## add new info as (gene, trans)
			resH[key] = {}
			for k in indexH.keys():
				if k not in ['Allele','Feature_type','Gene','Feature']:
					resH[key][k] = arr[indexH[k]]
	return resH

def main(inFileName,geneList=[]):

	dataH = {}

#	nameL = ('Mutation GRCh37 genome position', 'Mutation GRCh37 strand','Gene name','ID_sample','ID_tumour','Primary site', \
#		'Site subtype','Primary histology','Histology subtype','Genome-wide screen','Mutation ID','Mutation CDS','Mutation AA', \
#		'Mutation Description','Mutation zygosity','Mutation somatic status','Pubmed_PMID','Sample source','Tumor origin','Comments')

	nameL = ('Gene name','Mutation CDS','Mutation AA','Mutation Description','Mutation GRCh37 genome position','Mutation GRCh37 strand','Mutation somatic status')

	inFile = open(inFileName)

	headerL = inFile.readline()[:-1].split('\t')

	idxH = dict([(x, headerL.index(x)) for x in nameL])

	badH = {}
	tmpFile = open('prepDB.tmp', 'w')
	for line in inFile:

		valueL = line[:-1].split('\t')

		geneN = valueL[idxH['Gene name']]

		if '_ENST' in geneN:
			geneN = geneN.split('_ENST')[0]

		if len(geneList)>0 and geneN not in geneList:
			continue

		coord = valueL[idxH['Mutation GRCh37 genome position']]	

		if not coord:
			continue

		somatic = valueL[idxH['Mutation somatic status']]	

		if not 'somatic' in somatic:
			continue

		(chrNum,chrSta,chrEnd) = re.search('([^:-]+):([^:-]+)-([^:-]+)', coord).groups()

		cds = valueL[idxH['Mutation CDS']]	
		aa = valueL[idxH['Mutation AA']]	
		desc = valueL[idxH['Mutation Description']]	
		strand = valueL[idxH['Mutation GRCh37 strand']]	

		rm = re.match('c\.[\+\-_0-9]+([atgcATGC]*)(>|ins|del)([atgcATGC]*)',cds)

		if rm:
			(ref,vtype,alt) = rm.groups()
		else:
			ref,alt = '',''

		if strand == '-':
			ref = mybasic.rc(ref)
			alt = mybasic.rc(alt)

		chr = chrNum
		if chr == '23':
			chr = 'X'
		elif chr == '24':
			chr = 'Y'
		elif chr == '25':
			chr = 'M'

		if vtype == 'del':
			rm = re.search('([ACGT]+)', alt.upper())
			## if deleted bases are specified
			if alt != '' and rm:
				## check if deleted bases are the same as reference sequences at the location
				new_ref = os.popen('samtools faidx /data1/Sequence/ucsc_hg19/hg19.fa chr%s:%s-%s' % (chr,chrSta,chrEnd)).readlines()[1:]
				new_ref = "".join(map(lambda x: x.rstrip().upper(), new_ref))
				if new_ref == alt.upper():
					chrSta = str(int(chrSta) - 1)
					ref = os.popen('samtools faidx /data1/Sequence/ucsc_hg19/hg19.fa chr%s:%s-%s' % (chr,chrSta,chrEnd)).readlines()[1:]
					ref = "".join(map(lambda x: x.rstrip().upper(), ref))
					alt = ref[0]
					tmpFile.write('%s\t%s\t.\t%s\t%s\t.\t.\tConfirmed_somatic\tGT\t./.\n' % (chr,chrSta,ref,alt))
		elif vtype == 'ins':
			## skip insertion (can't check if the information is true)
			pass
		else:
			if (chrNum,chrSta,chrEnd,strand,ref,alt) not in badH and (chrNum,chrSta,chrEnd,strand,ref,alt) not in dataH:
				if ref == '' or alt == '':
					badH[(chrNum,chrSta,chrEnd,strand,ref,alt)] = 0
				else:
					new_ref = os.popen('samtools faidx /data1/Sequence/ucsc_hg19/hg19.fa chr%s:%s-%s' % (chr,chrSta,chrEnd)).readlines()[1:]
					new_ref = "".join(map(lambda x: x.rstrip().upper(), new_ref))
					if new_ref != ref:
						badH[(chrNum,chrSta,chrEnd,strand,ref,alt)] = 0
					else:
						tmpFile.write('%s\t%s\t.\t%s\t%s\t.\t.\tConfirmed_somatic\tGT\t./.\n' % (chr,chrSta,ref,alt))

		key = (chrNum,chrSta,chrEnd,strand,ref,alt)

		if key in dataH:
			mybasic.pushHash(dataH[key],'geneN',geneN)
			mybasic.pushHash(dataH[key],'cds',cds)
			mybasic.pushHash(dataH[key],'aa',aa)
			mybasic.pushHash(dataH[key],'desc',desc)
		else:
			dataH[key] = {'geneN':set([geneN]), 'cds':set([cds]), 'aa':set([aa]), 'desc':set([desc])}

	tmpFile.flush()
	tmpFile.close()
	os.system('sort -k1n,1 -k2n,2 -k4n,4 -k5n,5 prepDB.tmp | uniq > /data1/Sequence/cosmic/cosmic_confirmed_somatic_v63.vcf')
	os.system('rm -f prepDB.tmp')
	os.system('perl /home/tools/VEP/variant_effect_predictor.pl --no_progress --fork 10 --config /home/tools/VEP/vep_config --format vcf -i /data1/Sequence/cosmic/cosmic_confirmed_somatic_v63.vcf -o prepDB.tmp --no_stats --vcf')

	format="Allele|Gene|Feature|Feature_type|Consequence|cDNA_position|CDS_position|Protein_position|Amino_acids|Codons|Existing_variation|AA_MAF|EA_MAF|RefSeq|EXON|INTRON|MOTIF_NAME|MOTIF_POS|HIGH_INF_POS|MOTIF_SCORE_CHANGE|DISTANCE|CLIN_SIG|CANONICAL|SYMBOL|SIFT|PolyPhen|GMAF|DOMAINS|AFR_MAF|AMR_MAF|ASN_MAF|EUR_MAF".split('|')
	idxH = {}
	for i in range(0,len(format)):
		idxH[format[i]] = i

	outField=('Consequence','cDNA_position','CDS_position','Protein_position','Amino_acids','Codons','EXON','INTRON','DISTANCE','SYMBOL','Existing_variation','MOTIF_NAME','MOTIF_POS','HIGH_INF_POS','MOTIF_SCORE_CHANGE','DOMAINS','SIFT','PolyPhen','GMAF','AA_MAF','EA_MAF','AFR_MAF','AMR_MAF','ASN_MAF','EUR_MAF','CLIN_SIG','CANONICAL')
	outH = {}
	tmpFile = open('prepDB.tmp', 'r')
	while True:
		line = tmpFile.readline().rstrip()
		if len(line) < 1:
			break
		if line[0] == '#':
			continue

		cols = line.split('\t')
		chr = cols[0]
		if chr.upper() == 'X':
			chr = '23'
		elif chr.upper() == 'Y':
			chr = '24'
		elif chr.upper() == 'M' or chr.upper() == 'MT':
			chr = '25'
		pos = cols[1]
		ref = cols[3]
		alt = cols[4]
		csq = cols[7].split(';')[1].split('=')[1]
		outH[(chr,pos,ref,alt)] = parse_info(csq, idxH)
	tmpFile.close()

	outFile = open('/data1/Sequence/cosmic/cosmic_v63_annotated.dat', 'w')
	for ((chrNum,chrSta,chrEnd,strand,ref,alt),infoH) in dataH.iteritems():
		if ref == '' or alt == '' or (chrNum,chrSta,ref,alt) not in outH.keys():
			outFile.write('chr%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (chrNum,chrSta,chrEnd,strand, ref,alt,\
				','.join(filter(lambda x: not x.startswith('ENSG'), list(infoH['geneN']))), ','.join(infoH['cds']), ','.join(infoH['aa']), ','.join(infoH['desc'])))
			for col in outField:
				outFile.write('\t')
			outFile.write('\n')
		else:
			annotH = outH[(chrNum,chrSta,ref,alt)]
			for key in annotH.keys():
				outFile.write('chr%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (chrNum,chrSta,chrEnd,strand, ref,alt,\
					','.join(filter(lambda x: not x.startswith('ENSG'), list(infoH['geneN']))), ','.join(infoH['cds']), ','.join(infoH['aa']), ','.join(infoH['desc'])))
				outFile.write('\t%s\t%s' % (key[0], key[1]))
				for col in outField:
					outFile.write('\t%s' % annotH[key][col])
				outFile.write('\n')
	outFile.flush()
	outFile.close()
	os.system('rm prepDB.tmp')

optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

#if '-i' in optH and '-o' in optH:
#	main(optH['-i'], optH['-o'])

#main('/data1/Sequence/cosmic/CosmicCompleteExport_v63_300113.tsv',['EGFR'])
main('/data1/Sequence/cosmic/CosmicCompleteExport_v63_300113.tsv')
