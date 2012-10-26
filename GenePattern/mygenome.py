# mygenome

import sys, os, copy
import mybasic


def loadRefFlatByChr(refFlatFileName):

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


class locus:

	def __init__(self,loc,fmt='gsnap'): # convert coordinates into UCSC-type

		self.strand = loc[0]
		self.chrom = loc[1:loc.find(':')]
		self.chrNum = loc[4:loc.find(':')]

		chrPosL = [int(loc[loc.find(':')+1:loc.find('..')]), int(loc[loc.find('..')+2:])]

		self.chrSta = min(chrPosL) - 1
		self.chrEnd = max(chrPosL) 

	def toString(self):

		return '%s:%s-%s%s' % (self.chrNum,self.chrSta,self.chrEnd,self.strand)

	def overlap(self,region):

		return overlap((self.chrNum,self.chrSta,self.chrEnd),region)

	def overlappingGeneL(self,refFlatH=None,refFlatFileName=''):

		gL = []

		if refFlatH == None and refFlatFileName != '':
			refFlatH = loadRefFlatByChr(refFlatFileName)
		
		for l in refFlatH[self.chrNum]:

			if self.overlap((l['chrNum'],l['txnSta'],l['txnEnd'])) > 0:
				gL.append(l['geneName'])

		return gL


class transcript:


	def __init__(self,geneName,refFlatFileName='/Users/jinkuk/Data/DB/refFlat_hg18.txt',assembly='hg18'):  # return the longest transcript matching geneName

		rows = map(processRefFlatLine,os.popen('grep "^%s	" %s' % (geneName,refFlatFileName)).readlines())
		rows = filter(lambda x: not '_' in x['chrNum'], rows)

		if len(rows)==0:
			self.chrom = ''
			return

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
