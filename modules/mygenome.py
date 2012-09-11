# mygenome

import sys, os, copy, re
import mybasic


def loadRefFlatByChr(refFlatFileName='/data1/Sequence/ucsc_hg19/annot/refFlat.txt'):

	h = {}

	for line in open(refFlatFileName):
	
		r = processRefFlatLine(line)

		mybasic.addHash(h, r['chrNum'], r)
	
	return h


def processRefFlatLine(line):

	tokL = line.rstrip().split('\t')

	h = {}

	h['geneName'] = tokL[0]
	h['refSeqId'] = tokL[1]
	h['chrom'] = tokL[2]
	h['chrNum'] = tokL[2][3:]
	h['strand'] = tokL[3]
	h['txnSta'] = int(tokL[4])
	h['txnEnd'] = int(tokL[5])
	h['txnLen'] = h['txnEnd'] - h['txnSta']
	h['cdsSta'] = int(tokL[6])
	h['cdsEnd'] = int(tokL[7])
	h['exnList'] = map(lambda x,y: (int(x),int(y)), tokL[9].split(',')[:-1], tokL[10].split(',')[:-1])
	h['exnLen'] = sum([e-s for (s,e) in h['exnList']])

	h['cdsList'] = []

	for (s,e) in h['exnList']:

		if s<=h['cdsSta'] and h['cdsSta']<=e:
			s = h['cdsSta']

		if s<=h['cdsEnd'] and h['cdsEnd']<=e:
			e = h['cdsEnd']

		if h['cdsSta']<=s and e<=h['cdsEnd']:
			h['cdsList'].append((s,e))
	
	h['cdsLen'] = sum([e-s for (s,e) in h['cdsList']])

	return h


def overlap((c1,s1,e1),(c2,s2,e2)):

	if c1 != c2 or e2<=s1 or e1<=s2:
		return 0

	s = max(s1,s2)
	e = min(e1,e2)

	if s < e:
		return e-s
	else:
		return 0


def mergeLoci(locusL,gap=10):

	if len(set([x.strand for x in locusL]))>1 or len(set([x.chrNum for x in locusL]))>1:
		return locusL

	locusL.sort(lambda a,b: cmp(a.chrSta,b.chrSta))

	locusMergedL = []

	i = 0

	while i < len(locusL):

		chrS1, chrE1 = locusL[i].chrSta, locusL[i].chrEnd

		curE = chrE1

		j = i+1

		while j < len(locusL):

			chrS2, chrE2 = locusL[j].chrSta, locusL[j].chrEnd

			if curE + gap < chrS2:
				break

			curE = max(curE,chrE2)
			j += 1

		newLocus = copy.deepcopy(locusL[i])
		newLocus.chrEnd = locusL[j-1].chrEnd

		locusMergedL.append(newLocus)

		i = j

	return locusMergedL


class InitationFailureException(Exception): pass


class locus: # UCSC type

	def __init__(self,loc):

		rm = re.match('([^:]+):([0-9,]+)-([0-9,]+)([+-])',loc)

		if rm:

			self.strand = rm.group(4)
			self.chrom = rm.group(1)

			if self.chrom[:3] == 'chr':
				self.chrNum = rm.group(1)[3:]
			else:
				self.chrNum = None

			self.chrSta = int(rm.group(2))
			self.chrEnd = int(rm.group(3))

		else:

			rm = re.match('([+-])([^:]+):([0-9,]+)..([0-9,]+)',loc)

			if rm:

				self.strand = rm.group(1)
				self.chrom = rm.group(2)

				if self.chrom[:3] == 'chr':
					self.chrNum = rm.group(2)[3:]
				else:
					self.chrNum = None

				chrPosL = [int(rm.group(3)), int(rm.group(4))]

				self.chrSta = min(chrPosL) - 1
				self.chrEnd = max(chrPosL) 

			else:

				raise Exception

	def toString(self,style='UCSC'):

		if style=='gsnap':
			return '%s%s:%s..%s' % (self.strand,self.chrom,self.chrSta+1,self.chrEnd)
		else:
			return '%s:%s-%s%s' % (self.chrom,self.chrSta,self.chrEnd,self.strand)
			
			

	def overlap(self,region):

		return overlap((self.chrom,self.chrSta,self.chrEnd),region)

	def overlappingGeneL(self,refFlatH=None,refFlatFileName='/data1/Sequence/ucsc_hg19/annot/refFlat.txt',strand_sensitive=False):

		gL = set()

		if refFlatH == None and refFlatFileName != '':
			refFlatH = loadRefFlatByChr(refFlatFileName)
		
		if self.chrNum not in refFlatH:
			return []

		for l in refFlatH[self.chrNum]:

			if strand_sensitive:

				if self.overlap((l['chrNum'],l['txnSta'],l['txnEnd'])) > 0 and self.strand==l['strand']:
					gL.add(l['geneName'])

			else:

				if self.overlap((l['chrNum'],l['txnSta'],l['txnEnd'])) > 0:
					gL.add(l['geneName'])

		return tuple(gL)

	def nibFrag(self, nibFragBase, buffer5p=0, buffer3p=0):

		if self.strand == '+':
			staPos = self.chrSta - buffer5p
			endPos = self.chrEnd + buffer3p
		else:
			staPos = self.chrSta - buffer3p
			endPos = self.chrEnd + buffer5p

		nibFragFile = os.popen('nibFrag -name="" %s/%s.nib %s %s %s stdout' % (nibFragBase, self.chrom, staPos, endPos, self.strand), 'r')

		nibFragFile.readline()

		return nibFragFile.read().replace('\n','').rstrip().upper()


class transcript:


	def __init__(self,geneName,refFlatFileName='/Users/jinkuk/Data/DB/refFlat_hg18.txt',assembly='hg18'):  # return the longest transcript matching geneName

		rows = map(processRefFlatLine,os.popen('grep "^%s	" %s' % (geneName,refFlatFileName)).readlines())
		rows = filter(lambda x: not '_' in x['chrNum'], rows)

		if len(rows)==0:
			raise InitiationFailureException()

		rows.sort(lambda x,y: cmp(y['cdsLen'],x['cdsLen'])); row = rows[0] # take refSeq with longest coding region

		self.assembly = assembly

		self.geneName = row['geneName']
		self.refSeqId = row['refSeqId']
		self.chrom = row['chrom']
		self.chrNum = row['chrNum']
		self.strand = row['strand']

		self.txnLen = row['txnLen']

		self.exnList = row['exnList']
		self.exnLen = row['exnLen']

		self.cdsList = row['cdsList']
		self.cdsLen = row['cdsLen']

	def txnOverlap(self,region):

		return overlap((self.chrNum,self.exnList[0][0],self.exnList[-1][-1]),region)

	def cdsOverlap(self,region):

		total = 0

		for (cdsS,cdsE) in self.cdsList:

			total += overlap((self.chrNum,cdsS,cdsE),region)

		return total

	def exnOverlap(self,region):

		total = 0

		for (exnS,exnE) in self.exnList:

			total += overlap((self.chrNum,exnS,exnE),region)

		return total


def geneNameH(refFlatFileName='/data1/Sequence/ucsc_hg19/annot/refFlat.txt', knownToRefSeqFileName='/data1/Sequence/ucsc_hg19/annot/knownToRefSeq.txt', \
		hugoFileName='/data1/Sequence/geneinfo/hugo.txt'):

	geneNameH = {}

	for line in open(refFlatFileName):

		h = processRefFlatLine(line)

		geneNameH[h['refSeqId']] = h['geneName']
		geneNameH[h['geneName']] = h['geneName']

	for line in open(knownToRefSeqFileName):

		(knownId,refSeqId) = line[:-1].split('\t')

		try:
			geneNameH[knownId] = geneNameH[refSeqId]
		except:
			pass

	for line in open(hugoFileName):

		(geneName,geneDesc,aliases,geneCardNames,refSeqIds) = line[:-1].split('\t')

		for refSeqId in refSeqIds.split(','):
			
			if refSeqId not in geneNameH:
				geneNameH[refSeqId] = geneName

		for alias in aliases.split(','):

			if alias not in geneNameH:
				geneNameH[alias] = geneName

		for geneCardName in geneCardNames.split(','):

			geneNameH[geneCardName] = geneName

	return geneNameH


def geneSetH(biocartaFileName='/data1/Sequence/geneinfo/BIOCARTA.gmt', goFileName='/data1/Sequence/geneinfo/GO.gmt', keggFileName='/data1/Sequence/geneinfo/KEGG.gmt'):

	geneSetH = {'biocarta':{}, 'go':{}, 'kegg':{}}

	for line in open(biocartaFileName):

		tokL = line[:-1].split('\t')
		geneSetH['biocarta'][tokL[0]] = (tokL[1],tuple(tokL[2:]))

	for line in open(goFileName):

		tokL = line[:-1].split('\t')
		geneSetH['go'][tokL[0]] = (tokL[1],tuple(tokL[2:]))

	for line in open(keggFileName):

		tokL = line[:-1].split('\t')
		geneSetH['kegg'][tokL[0]] = (tokL[1],tuple(tokL[2:]))

	return geneSetH


def geneInfoH(geneNameH, geneSetH, refSeqSummaryFileName='/data1/Sequence/ucsc_hg19/annot/refSeqSummary.txt', hugoFileName='/data1/Sequence/geneinfo/hugo.txt', \
		censusFileName='/data1/Sequence/geneinfo/cancer_gene_census.txt', biocartaFileName='/data1/Sequence/geneinfo/BIOCARTA.gmt', \
		goFileName='/data1/Sequence/geneinfo/hugo.txt', keggFileName='/data1/Sequence/geneinfo/hugo.txt'):

	geneInfoH = {}

	for line in open(refSeqSummaryFileName):

		(refSeqId,status,summary) = line[:-1].split('\t')

		if refSeqId in geneNameH:

			geneName = geneNameH[refSeqId]

			if geneName not in geneInfoH:
				geneInfoH[geneName] = {}

			geneInfoH[geneName]['summary'] = summary

	for line in open(hugoFileName):

		(geneName,desc,aliases,geneCardName,refSeqIds) = line[:-1].split('\t')

		if geneName not in geneInfoH:
			geneInfoH[geneName] = {}

		geneInfoH[geneName]['desc'] = desc 
		geneInfoH[geneName]['aliases'] = aliases
		geneInfoH[geneName]['refSeqIds'] = refSeqIds

	for line in open(censusFileName):

		tokL = line[:-1].split('\t')

		(geneName,desc,somatic,germline,mutType,translocPartners) = (tokL[0],tokL[1],tokL[7],tokL[8],tokL[12],tokL[13])

		if geneName == 'Symbol':
			continue

		if geneName not in geneInfoH:
			geneInfoH[geneName] = {'desc':desc}

		geneInfoH[geneName]['census_somatic'] = somatic
		geneInfoH[geneName]['census_germline'] = germline
		geneInfoH[geneName]['census_mutType'] = mutType
		geneInfoH[geneName]['census_translocPartners'] = translocPartners


	for geneSetDB in geneSetH.keys():

		for (geneSetName,(geneSetDesc,geneNameL)) in geneSetH[geneSetDB].iteritems():

			for geneName in geneNameL:

				if geneName in geneInfoH:
					mybasic.addHash(geneInfoH[geneName],geneSetDB,(geneSetName,geneSetDesc))
				else:
					geneInfoH[geneName] = {geneSetDB:[(geneSetName,geneSetDesc)]}

	return geneInfoH


class gene:

	def __init__(self,identifier,geneNameH=None,geneSetH=None,geneInfoH=None):
	
		if geneNameH:
			self.geneNameH = geneNameH
		else:
			self.geneNameH = geneNameH()

		if geneSetH:
			self.geneSetH = geneSetH
		else:
			self.geneSetH = geneSetH()

		if geneInfoH:
			self.geneInfoH = geneInfoH
		else:
			self.geneInfoH = geneInfoH(geneNameH,geneSetH)

		try:
			self.geneName = self.geneNameH[identifier]
		except:
			self.geneName = None

		if self.geneName and self.geneName in geneInfoH:
			self.geneInfo = geneInfoH[self.geneName]
		else:
			self.geneInfo = {}

	def getAttr(self,attr):

		if attr in self.geneInfo:
			return self.geneInfo[attr]
		else:
			return ''
