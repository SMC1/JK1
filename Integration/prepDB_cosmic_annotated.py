#!/usr/bin/python

import os, sys, getopt, re, glob
import mybasic, myvep

#	nameL = ('Mutation GRCh37 genome position', 'Mutation GRCh37 strand','Gene name','ID_sample','ID_tumour','Primary site', \
#		'Site subtype','Primary histology','Histology subtype','Genome-wide screen','Mutation ID','Mutation CDS','Mutation AA', \
#		'Mutation Description','Mutation zygosity','Mutation somatic status','Pubmed_PMID','Sample source','Tumor origin','Comments')
nameL = ('Gene name','Mutation CDS','Mutation AA','Mutation Description','Mutation GRCh37 genome position','Mutation GRCh37 strand','Mutation somatic status','Mutation ID')

def read_vcf(ver=66):
	codFileN = glob.glob('/data1/Sequence/cosmic/CosmicCodingMuts_v%s*.vcf' % ver)[0]
	ncdFileN = glob.glob('/data1/Sequence/cosmic/CosmicNonCodingVariants_v%s*.vcf' % ver)[0]

	dataH = {}

	codFile = open(codFileN, 'r')
	for line in codFile:
		if len(line.rstrip()) < 1:
			break
		if line[0] == '#':
			continue

		cols = line.rstrip().split('\t')
		chr = cols[0]
		pos = cols[1]
		id = cols[2]
		ref = cols[3]
		alt = cols[4]
		dataH[id] = (chr,pos,ref,alt)
	codFile.close()

	ncdFile = open(ncdFileN, 'r')
	for line in ncdFile:
		if len(line.rstrip()) < 1:
			break
		if line[0] == '#':
			continue

		cols = line.rstrip().split('\t')
		chr = cols[0]
		pos = cols[1]
		id = cols[2]
		ref = cols[3]
		alt = cols[4]
		dataH[id] = (chr,pos,ref,alt)
	ncdFile.close()
	return dataH

def read_cosmic(inFileName, geneList=[]):
	dbH = read_vcf()

	inFile = open(inFileName)
	headerL = inFile.readline()[:-1].split('\t')
	idxH = dict([(x, headerL.index(x)) for x in nameL])
	dataH = {}

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
		chr = chrNum
		if chr == '23':
			chr = 'X'
		elif chr == '24':
			chr = 'Y'
		elif chr == '25':
			chr = 'M'

		cds = valueL[idxH['Mutation CDS']]	
		aa = valueL[idxH['Mutation AA']]	
		desc = valueL[idxH['Mutation Description']]	

		rm = re.match('c\.[\+\-_0-9]+([atgcATGC]*)(>|ins|del)([atgcATGC]*)',cds)
		if rm:
			(ref,vtype,alt) = rm.groups()
		else:
			ref,alt = '',''

		strand = valueL[idxH['Mutation GRCh37 strand']]	
		if strand == '-':
			ref = mybasic.rc(ref)
			alt = mybasic.rc(alt)

		id = valueL[idxH['Mutation ID']]
		if vtype == 'del':
			ref = alt
			alt = ''

		if 'COSM'+id in dbH:
			(dbChr,dbPos,dbRef,dbAlt) = dbH['COSM'+id]
			if (chr != dbChr) or (chrSta != dbPos and chrSta != str(int(dbPos)+1)) or (ref != '' and ref != dbRef and ref != dbRef[1:]) or (alt != '' and alt != dbAlt and alt != dbAlt[1:]):
				print '%s <-> %s' % ((chr,chrSta,ref,alt), (dbChr,dbPos,dbRef,dbAlt))
		elif 'COSN'+id in dbH:
			(dbChr,dbPos,dbRef,dbAlt) = dbH['COSN'+id]
			if (chr != dbChr) or (chrSta != dbPos and len(dbRef)==len(dbAlt)) or (ref != '' and ref != dbRef and ref != dbRef[1:]) or (alt != '' and alt != dbAlt and alt != dbAlt[1:]):
				print '%s <-> %s' % ((chr,chrSta,ref,alt), (dbChr,dbPos,dbRef,dbAlt))

		key = (chr, chrSta, chrEnd, strand, ref, alt)
		if key in dataH:
			mybasic.pushHash(dataH[key],'geneN',geneN)
			mybasic.pushHash(dataH[key],'cds',cds)
			mybasic.pushHash(dataH[key],'aa',aa)
			mybasic.pushHash(dataH[key],'desc',desc)
		else:
			dataH[key] = {'geneN':set([geneN]), 'cds':set([cds]), 'aa':set([aa]), 'desc':set([desc])}
	
	return dataH

def annotate(tabH):
	outFile = open('tmp','w')
	for (chr, pos, end, strand, ref, alt) in tabH:
		if ref != '' and alt != '':
			outFile.write('%s\t%s\t.\t%s\t%s\t.\t.\t.\n' % (chr, pos, ref.upper(), alt.upper()))
	outFile.flush()
	outFile.close()
	os.system('sort -k1d,1 -k2n,2 -k4d,4 -k5d,5 tmp | uniq > tmp2')
	os.system('rm -f tmp')
	os.system('perl /home/tools/VEP/variant_effect_predictor.pl --no_progress --config /home/tools/VEP/vep_config --format vcf -i tmp2 -o /data1/Sequence/cosmic/cosmic_confirmed_somatic_v63.vcf --no_stats --vcf')
	os.system('rm -f tmp2')

def main(inFileName, geneList=[]):
	dataH = read_cosmic(inFileName, geneList)
#	annotate(dataH)

#	infoH = myvep.parse_vep('/data1/Sequence/cosmic/cosmic_confirmed_somatic_v63.vcf')
	## print SQL table

def main1(inFileName,geneList=[]):

	tmpFile.flush()
	tmpFile.close()
	os.system('sort -k1n,1 -k2n,2 -k4n,4 -k5n,5 prepDB.tmp | uniq > /data1/Sequence/cosmic/cosmic_confirmed_somatic_v63.vcf')
	os.system('rm -f prepDB.tmp')

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
	os.system('ln -s /data1/Sequence/cosmic/cosmic_v63_annotated.dat /data1/Sequence/cosmic/cosmic_annotated.dat')

optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

#if '-i' in optH and '-o' in optH:
#	main(optH['-i'], optH['-o'])

#main('/data1/Sequence/cosmic/CosmicCompleteExport_v63_300113.tsv',['EGFR'])
#main('/data1/Sequence/cosmic/CosmicCompleteExport_v63_300113.tsv')
main('/data1/Sequence/cosmic/CosmicCompleteExport_v66_250713.tsv')
