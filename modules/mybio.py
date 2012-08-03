#!/usr/bin/python_epd

import sys
import os
import re
import types
import string
import MySQLdb
import random
import math
import sets
import matplotlib.pyplot as plt
import numpy as np


	
dnaAlpha = ['A','T','G','C']
rnaAlpha = ['A','U','G','C']

ntHash = {'A':1,'C':2,'G':3,'T':4}

expandDnaAlpha = {'A':'A', 'T':'T', 'G':'G', 'C':'C',
    'S':'CG', 'W':'AT', 'Y':'CT', 'R':'AG', 'M':'AC', 'K':'GT',
    'N':'ATGC'}

expandRnaAlpha = {'A':'A', 'U':'U', 'G':'G', 'C':'C',
    'S':'CG', 'W':'AU', 'Y':'CU', 'R':'AG', 'M':'AC', 'K':'GU',
    'N':'AUGC'}

hg18_chrLen = ('247249719','242951149','199501827','191273063','180857866','170899992',
    '158821424','146274826','140273252','135374737','134452384','132349534',
	'114142980','106368585','100338915','88827254','78774742','76117153',
	'63811651','62435964','46944323','49691432','154913754','57772954','16571')

huGeVer = 'hg18'

dataDir = '/Users/jinkuk/Data'
codeDir = '/Users/jinkuk/Codes'

		 
## Context Score paramters

meanValue = {(1,1):-0.31, (0,1):-0.161, (1,0):-0.099, (0,0):-0.015}

pairing_s = {(1,1):-0.0041, (0,1):-0.031, (1,0):-0.0211, (0,0):-0.00278}
pairing_y = {(1,1):-0.299, (0,1):-0.094, (1,0):-0.053, (0,0):-0.0091}

au_s = {(1,1):-0.64, (0,1):-0.50, (1,0):-0.42, (0,0):-0.241}
au_y = {(1,1):0.055, (0,1):0.108, (1,0):0.137, (0,0):0.115}

dist_s = {(1,1):0.000172, (0,1):0.000091, (1,0):0.000072, (0,0):0.000049}
dist_y = {(1,1):-0.38, (0,1):-0.198, (1,0):-0.131, (0,0):-0.033}


## DB

mysqlCommand = 'mysql -h canna -u jinkuk --password=privid -D jinkuk '

 

## functions

def connectDB():

	con = MySQLdb.connect(host="localhost", user="", passwd="", db="bio")
	con.autocommit = True
	cursor = con.cursor()
	return (con,cursor)


def connectML():
	
	return (np,plt)


def toRNA(seq):

	if not isinstance(seq,types.StringType):
		print "error: string type required!"
		sys.exit(1)

	seq_ret = seq.upper()

	tab = string.maketrans('T','U')
	seq_ret = seq_ret.translate(tab)

	return seq_ret


def toDNA(seq):

	if not isinstance(seq,types.StringType):
		print "error: string type required!"
		sys.exit(1)

	seq_ret = seq.upper()

	tab = string.maketrans('U','T')
	seq_ret = seq_ret.translate(tab)

	return seq_ret


def swapTuple((a,b)):
	return (b,a)


def optH(optL):

	h = {}

	for (k,v) in optL:
		h[k] = v

	return h

#def loadFileAsHash(baseDir,fileNamePattern,keyIdx,valueIdxL,condFun):
#
#	expDir = '%s/%s/Expression-%s/%s' % ((TCGA.dataDir,)+exp[:3])
#
#	inFile = os.popen('find %s -name "*TCGA*.txt" -print | xargs tail +2 -q' % expDir,'r')
#
#	if not gId_spec:
#		outFile = open('%s/%s_%s_%s_stats.dat' % (expDir,exp[0],exp[1],exp[2]), 'w')
#
#	resultH_n = {}
#	resultH_c = {}
#
#	for line in inFile:
#
#		(sId,gId,value) = line[:-1].split('\t')
#
#		if value in ('null','NULL'):
#			continue
#
#		if sId[13:15] in code_normal:
#			mybio.addHash(resultH_n,gId,float(value))
#		else:
#			mybio.addHash(resultH_c,gId,float(value))
#
#	if len(resultH_n) != len(resultH_c):
#		raise Exception


def count(fun,l):

	c = 0

	for e in l:
		
		if apply(fun,(e,)):
			c += 1

	return c


def index(fun,l):

	for i in range(len(l)):

		if apply(fun,l[i]):
			
			return i
	
	return -1


def indexL(dataL, queryL):

	result = []

	for q in queryL:

		try:
			result.append(dataL.index(q))
		except:
			result.append(-1)

	return result


def overlap((c1,s1,e1),(c2,s2,e2)):

	if c1 != c2 or e2<=s1 or e1<=s2:
		return 0

	s = max(s1,s2)
	e = min(e1,e2)

	if s < e:
		return e-s
	else:
		return 0


def txnOverlap(trans,region):

	return overlap((trans.chrNum,trans.txnSta,trans.txnEnd),region)


def cdsOverlap(trans,region):

	total = 0

	for (cdsS,cdsE) in trans.cdsL:

		total += overlap((trans.chrNum,cdsS,cdsE),region)

	return total


def exnOverlap(trans,region):

	total = 0

	for (exnS,exnE) in trans.exnL:

		total += overlap((trans.chrNum,exnS,exnE),region)

	return total


def corr(x, y, b=1000):

	sampL = [np.array(x), np.array(y)]

	r = np.corrcoef(x,y)[0][1]
	rL = [0.] * b

	l = len(x)

	for i in range(b):

		bootSampL = []

		for j in range(2):

			try:
				bootIdxL = np.random.randint(l,size=l)
			except:
				print l
			bootSampL.append(sampL[j].take(bootIdxL))
		
		rL[i] = np.corrcoef(bootSampL[0],bootSampL[1])[0][1]

	return (r, len(filter(lambda x: x>abs(r) or x<abs(r)*-1, rL)) / float(b))


def rev(seq):

	if not isinstance(seq,types.StringType):
		print "error: string type required!"
		print type(seq)
		sys.exit(1)

	seq_rev = ""

	for i in range(0,len(seq)):
		seq_rev = seq[i] + seq_rev

	return seq_rev


def compl(seq, seqType):

	if not isinstance(seq,types.StringType):
		print "error in mybio.compl: string type required!"
		print "you entered:%s" % (seq,)
		print type(seq)
		sys.exit(1)

	seq_ret = seq.upper()

	if seqType == 'RNA':
		tab = string.maketrans('ATUGCRYSW-','UAACGYRSW-')
	else:
		tab = string.maketrans('ATUGCRYSW-','TAACGYRSW-')
	
	seq_ret = seq_ret.translate(tab)

	return seq_ret


def rc(seq,type):

	if not isinstance(seq,types.StringType):
		print "error: string type required!"
		sys.exit(1)

	seq = rev(seq)
	seq = compl(seq,type)

	return seq


def tet2nt(tet,length):

	ntAlphaH = {0:'A', 1:'C', 2:'G', 3:'T'}

	outS = ''

	for i in range(length):

		outS = ntAlphaH[tet % 4] + outS
		tet /= 4

	return outS


def nt2code(seq):

	return ''.join(map(lambda x: str(ntHash[x]), list(seq)))


def codeSeq(seq,maxLen):

	outL = []

	for i in range(maxLen):

		if i < len(seq):
			outL.append('%s' % ntHash[seq[i]])
		else:
			outL.append('0')

	return '\t'.join(outL)


def fillZero(num,dig):

	retStr = ''

	for d in range(dig):

		retStr = str(num%10) + retStr
		num = num // 10

	return retStr


def dynamicBin(xyL,bSize):

	xyL.sort(lambda x,y: cmp(x[0],y[0]))

	avgL = []
	avg = np.zeros(2)

	for i in range(len(xyL)):

		avg += np.array(xyL[i])

		if (i+1) % bSize == 0:
			avgL.append(tuple(avg/bSize))
			avg = np.zeros(2)

	#avgL.append(tuple(avg/(len(xyL) % bSize)))

	return avgL


def ntContent(seq):

	seq = toDNA(seq)

	agCon = 0.
	gcCon = 0.

	for i in range(len(seq)):

		if seq[i] in ['A','G']:
			agCon += 1

		if seq[i] in ['G','C']:
			gcCon += 1

	return (agCon/len(seq)*100, gcCon/len(seq)*100)


def asymmetry(seq):

	if len(seq)<4:
		print seq, 'mybio.assymetry: seq should be longer than 4'
		sys.exit(1)

	hash = {'A':-1, 'T':-1 ,'G':1 ,'C':1}

	overlapSeq = toDNA(seq)

	halfLen = len(overlapSeq)/2

	halfSeqW = rev(overlapSeq[:halfLen])
	halfSeqS = overlapSeq[-1*halfLen:]

	rawScore = 0
	maxScore = 0.

	for i in range(halfLen):

		rawScore += hash[halfSeqS[i]] * (i+1)
		rawScore += hash[halfSeqW[i]] * (i+1) *-1

		maxScore += 2 * (i+1)

	return rawScore/maxScore


def asymmetry_nnm(seq):

	if len(seq)<4:
		print 'mybio.assymetry: seq should be longer than 4'
		sys.exit(1)

	hash = {'AA':-0.93, 'AT':-1.10, 'TA':-1.33, 'CT':-2.08, 'CA':-2.11, 'GT':-2.24, 'GA':-2.35, 'CG':-2.36, 'GG':-3.26, 'GC':-3.42}

	for (k,v) in hash.copy().items():
		hash[rc(k,'DNA')] = v
		
	hash_end = {'A':0.45, 'T':0.45, 'G':0, 'C':0}

	overlapSeq = toDNA(seq)

	halfLen = int(math.ceil(len(overlapSeq)/float(2)))

	halfSeqW = rc(overlapSeq[:halfLen],'DNA')
	halfSeqS = overlapSeq[-1*halfLen:]

	rawScore = 0
	maxScore = 0.

	for i in range(halfLen-1):

		rawScore += hash[halfSeqS[i:i+2]] * (i+1) *-1
		rawScore += hash[halfSeqW[i:i+2]] * (i+1)

		maxScore += (3.42-0.93) * (i+1)

	rawScore += hash_end[halfSeqS[-1]] * (halfLen-1) *-1
	rawScore += hash_end[halfSeqW[-1]] * (halfLen-1)

	maxScore += 0.45 * (halfLen-1)

	return rawScore/maxScore


def addTuple(tup1,tup2):
	
	return map(sum,zip(tup1,tup2))

def incHash(hash,key,val=1):
 
	try:
		hash[key] += val
	except:
		hash[key] = val


def addHash(hash,key,val):
 
	if hash.has_key(key):
		hash[key].append(val)
	else:
		hash[key] = [val]


def allocHash(hash,key,val):

	if hash.has_key(key):
		print "error in mybio.allocHash: previously existing key"
		sys.exit(0)
	else:
		hash[key] = val


def addMultiLevelHash(h,keyL,value):

	if len(keyL) == 1:
		addHash(h,keyL[0],value)
		return

	if not keyL[0] in h:
		h[keyL[0]] = {}

	addMultiLevelHash(h[keyL[0]],keyL[1:],value)


def incMultiLevelHash(h,keyL,value=1):

	if len(keyL) == 1:
		incHash(h,keyL[0],value)
		return

	if not keyL[0] in h:
		h[keyL[0]] = {}

	incMultiLevelHash(h[keyL[0]],keyL[1:],value)


def setMultiLevelHash(h,keyL,value):

	if len(keyL) == 1:
		h[keyL[0]] = value
		return

	if not keyL[0] in h:
		h[keyL[0]] = {}

	setMultiLevelHash(h[keyL[0]],keyL[1:],value)


def m2idx(motif,type):

	if type == 'RNA':
		alphabet = rnaAlpha
	else:
		alphabet = dnaAlpha

	idx=0

	for i in range(len(motif)):

		if not (motif[i] in alphabet):
			print 'error in m2idx'
			sys.exit(1)

		idx = (idx << 2) + alphabet.index(motif[i])

	return idx

 
def idx2m(idx,mlen,type):

	if type == 'RNA':
		alphabet = rnaAlpha
	else:
		alphabet = dnaAlpha

	motif=""

	for i in range(mlen):
		motif = alphabet[idx % 4] + motif
		idx = idx >> 2
	return motif

def int_custom(x):
 
	if not x:
		return 0
	else:
		return int(x)

def type_custom(fun,x):
 
	if not x:
		return apply(fun,0)
	else:
		return apply(fun,x)
  
def tmDNA_lessThan11nt(seq):

	tm = 0

	for base in list(seq):

		if base in ['A','T']:
			tm += 2
		elif base in ['G','C']:
			tm += 4

	return tm


def matchNmer(seq,nmer):
 
	matchList = []

	for i in range(len(seq)-len(nmer)+1):
		if seq[i:i+len(nmer)] == nmer:
			matchList.append(i)

	return matchList


def countOccurrence(seq,spec):
 
    count = 0
 
    for i in range(len(seq)-len(spec)+1):
        if seq[i:i+len(spec)] == spec:
            count += 1
 
    return count


def expandNmer(nmer,type):
 

	if type == 'RNA':
		expandAlpha = expandRnaAlpha
	else:
		expandAlpha = expandDnaAlpha

	if(len(nmer)==0):
		return []
 
	if(len(nmer)==1):
		return list(expandAlpha[nmer])
 
	prevResult = expandNmer(nmer[1:],type)

	result = []

	for nt in list(expandAlpha[nmer[0]]):
		for p_nmer in prevResult:
			result.append(nt+p_nmer)

	return result
 

def diff(seq1,seq2):
 
	variantList = []

	if len(seq1)==len(seq2):

		for i in range(len(seq1)):
			if seq1[i] != seq2[i]:
				variantList.append((i+1,seq1[i],seq2[i]))

	else:
		
		print 'error in mybio.diff: input length inconsistency'
		sys.exit(1)

	return variantList


def genRandSeq(len,type,num=1):

	if type == 'RNA':
		alpha = rnaAlpha
	else:
		alpha = dnaAlpha

	list = []

	for i in range(num):

		seq = ""

		for j in range(len):

			seq += alpha[int(random.random()*4)]

		list.append(seq)

	return list


def randVarDic(pdfDic):
 
	tot = sum(pdfDic.values())

 	if tot==0:
		print "error!"
		sys.exit(1)

	r = random.random() * tot

	for k in pdfDic.keys():

		if r < pdfDic[k]:
			return k

		r = r - pdfDic[k]

	return k


def randVar(pdf):
 
	tot = sum(pdf)

 	if tot==0:
		print "error!"
		sys.exit(1)

	r = random.random() * tot

	for a in range(len(pdf)-1):

		if r < pdf[a]:
			return a

		r = r - pdf[a]

	return len(pdf)-1


## staPos: start position of the target sequence
## endPos: end position of the target sequence

def nibFrag(nibFileName,staPos,endPos,strand):

	nibFragFile = os.popen('nibFrag -name="" %s %s %s %s stdout' % (nibFileName, staPos-1, endPos,strand), 'r')

	nibFragFile.readline()

	seq = nibFragFile.read().replace('\n','').rstrip().upper()

	return seq


## refSeqFilePath: COLLAPSED fasta format file containing multiple entries
## refSeqLociList = [(refSeqID_v,refSeqStaPos) ...]
## return plus sequence of length "seqLen" that matches any of the coordinates in "refSeqLociList"

def faFrag_refSeq(refSeqFilePath,refSeqLociHash,seqLen):

	ro = re.compile('%s%s%s' % ('\|(','|'.join(refSeqLociHash.keys()),')\|'))

	faFile = open(refSeqFilePath,"r")

	refSeqID_v = ''

	while 1:

		header = faFile.readline()

		if not header:
			break

		rm = ro.search(header)

		if rm:

			refSeqID_v = rm.group(1)
			staPos = refSeqLociHash[refSeqID_v]

			refSeq = faFile.readline()[:-1]
			returnSeq = refSeq[staPos-1:staPos+seqLen-1]

			break

		else:

			faFile.readline()

	faFile.close()

	if refSeqID_v != '':
		return ((refSeqID_v,staPos),returnSeq)
	else:
		return None


## filePath: COLLAPSED fasta format file containing multiple entries

def faFrag(filePath,seqName,seqSta,seqEnd):

	faFile = open(filePath,"r")

	returnSeq = ''

	while 1:

		header = faFile.readline()

		if not header:
			break

		if header[1:-1]==seqName:

			returnSeq = faFile.readline()[:-1][seqSta:seqEnd]

			break

		else:

			faFile.readline()

	return returnSeq



def loadFasta(seqFilePath):
 
    returnHash = {}
 
    file = open(seqFilePath,"r")
 
    while 1:

		header = file.readline()

		if not header:
			break

		if(header[0] != '>'):
			print header
			raise Exception

		id = header[:-1].split(' ')[0][1:]
		tok = header[:-1].split(' ')[1:]

		seq = file.readline()[:-1]

		if id in returnHash:
			print id
			raise Exception

		returnHash[id] = (seq,' '.join(tok))
 
    file.close()
 
    return returnHash


def load_refSeq(seqFilePath):
 
    returnHash = {}
 
    file = open(seqFilePath,"r")
 
    while 1:

		header = file.readline()

		if not header:
			break

		if(header[0] != '>'):
			print header
			raise Exception

		id = header[:-1].split('|')[3]

		if id[:3] != 'NM_':
			file.readline()
			continue

		seq = file.readline()[:-1]

		if id in returnHash:
			print header
			raise Exception

		returnHash[id] = seq
 
    file.close()
 
    return returnHash


def mean(list):

	return float(sum(list))/len(list)


def meanSd(list):

	llen = len(list)

	sum = 0.

	for i in range(llen):
		sum += list[i]

	mean = sum / llen

	diffSqSum = 0.

	for i in range(llen):
		diffSqSum += pow(list[i]-mean, 2)

	sd = math.sqrt(diffSqSum/(llen-1))

	return (mean,sd)


def deviation(data,option='mean'):

	if option=='mean':
		m = float(mean(data))
	elif option=='median':
		m = float(median(data))
	else:
		raise Error

	results = []

	for d in data:
		results.append(d-m)

	return results


def cdf(data):

	hash = {}

	for d in data:
		incHash(hash,d)

	items = hash.items()
	items.sort(lambda x,y: cmp(x,y))
	items = items

	x = [k for (k,v) in items]
	y = np.hstack((np.zeros(1),np.cumsum([v for (k,v) in items])))

	return (np.array(x+[x[-1]]), y/float(y[-1]))


# median devidation median

def mdm(data):

	return median(map(abs,deviation(data,'median')))


def delCommonHypen(seqAlignList):

	alignLen = len(seqAlignList[0])

	for seqAlign in seqAlignList[1:]:

		if len(seqAlign)!=alignLen:
			print seqAlignList
			raise Exception


	posWiseList_all = []

	for i in range(alignLen):
		
		posWiseList = []

		for seqAlign in seqAlignList:
			posWiseList.append(seqAlign[i])

		posWiseList_all.append(posWiseList)

	try:
		posWiseList_all.remove(['-']*len(seqAlignList))
	except:
		pass


	seqWiseList_all = []

	for i in range(len(posWiseList)):
		
		seqWiseList = []

		for posWiseList in posWiseList_all:
			seqWiseList.append(posWiseList[i])

		seqWiseList_all.append(''.join(seqWiseList))

	return seqWiseList_all


# mmSta is index starting from 0

def cons_mm9_R(mmChrNum,mmSta,mmEnd,mmSeq_input=''):

	inF = open('/lab/bartel.2/jinkuk/mm9/30way/3utr2genome_filtered/chr%s.3utr' % (mmChrNum,))

	qlen = mmEnd-mmSta

	mmAlignCoord = []
	mmAlignSeq = []
	rnAlignSeq = []

	while 1:

		line = inF.readline()

		if not line:
			break

		mmL = line.split()
		
		mmBlockSta = int(mmL[1])
		mmBlockEnd = mmBlockSta+int(mmL[2])
		mmBlockSeq = mmL[5].upper()

		if not (mmEnd<=mmBlockSta or mmBlockEnd<=mmSta):

			rnL = []

			while 1:

				line = inF.readline()

				if line == '\n':

					break

				if line[:3] == 'rn4':

					rnL = line.split()
					rnBlockSta = int(rnL[1])
					rnBlockEnd = rnBlockSta+int(rnL[2])
					rnBlockSeq = rnL[5].upper()
					continue

			if not rnL:

				break

			mmGap = 0
			rnGap = 0

			for i in range(len(mmBlockSeq)):

				if (i == 0 and mmSta<mmBlockSta) or (mmBlockSeq[i] != '-' and i==mmSta-mmBlockSta+mmGap):

					staIdx = i

					mmAlignSta = mmBlockSta+i-mmGap

					rnSta = rnBlockSta+i-rnGap

				if (i == len(mmBlockSeq)-1) or (mmBlockSeq[i] != '-' and i==mmEnd-mmBlockSta+mmGap-1):

					mmAlignEnd = mmBlockSta+i-mmGap+1

					rnEnd = rnBlockSta+i-rnGap

					mmAlignSeq.append(mmBlockSeq[staIdx:i+1])
					rnAlignSeq.append(rnBlockSeq[staIdx:i+1])

					mmAlignCoord.append((mmAlignSta,mmAlignEnd))

					break

				if mmBlockSeq[i] == '-':
					mmGap += 1

				if rnBlockSeq[i] == '-':
					rnGap += 1

		elif mmEnd <= mmBlockSta:
			break

		else:

			while inF.readline() != '\n':
				pass

	inF.close()

#	print mmAlignCoord
#	print mmAlignSeq
#	print rnAlignSeq

	if len(mmAlignCoord)>0 and mmAlignCoord[0][0]==mmSta and mmAlignCoord[-1][1]==mmEnd:

		idxContinuity = 1

		for i in range(len(mmAlignCoord)-1):

			if mmAlignCoord[i][1] != mmAlignCoord[i+1][0]:

				idxContinuity = 0
				break

		mmSeq = ''.join(mmAlignSeq).replace('-','')
		rnSeq = ''.join(rnAlignSeq).replace('-','')

		if mmSeq==rnSeq and (mmSeq_input=='' or mmSeq_input==mmSeq):

			seqIdentity = 1

		else:

			seqIdentity = 0

		if idxContinuity and seqIdentity:

			return ('Y',[mmSeq,rnSeq])

		else:

			return ('N',[mmSeq,rnSeq])

	else:

		return ('N',[])


# mmSta is index starting from 0

def cons_mm9_HRD(mmChrNum,mmSta,mmEnd,mmSeq_input=''):

	inF = open('/lab/bartel.2/jinkuk/mm9/30way/3utr4genome_filtered/chr%s.3utr' % (mmChrNum,))

	qlen = mmEnd-mmSta

	mmAlignCoord = []
	mmAlignSeq = []
	hgAlignSeq = []
	rnAlignSeq = []
	cfAlignSeq = []

	while 1:

		line = inF.readline()

		if not line:
			break

		mmL = line.split()
		
		mmBlockSta = int(mmL[1])
		mmBlockEnd = mmBlockSta+int(mmL[2])
		mmBlockSeq = mmL[5].upper()

		if not (mmEnd<=mmBlockSta or mmBlockEnd<=mmSta):

			hgL = []
			rnL = []
			cfL = []

			while 1:

				line = inF.readline()

				if line == '\n':

					break

				if line[:4] == 'hg18':

					hgL = line.split()
					hgBlockSta = int(hgL[1])
					hgBlockEnd = hgBlockSta+int(hgL[2])
					hgBlockSeq = hgL[5].upper()
					continue

				if line[:3] == 'rn4':

					rnL = line.split()
					rnBlockSta = int(rnL[1])
					rnBlockEnd = rnBlockSta+int(rnL[2])
					rnBlockSeq = rnL[5].upper()
					continue

				if line[:7] == 'canFam2':

					cfL = line.split()
					cfBlockSta = int(cfL[1])
					cfBlockEnd = cfBlockSta+int(cfL[2])
					cfBlockSeq = cfL[5].upper()
					continue

			if not (hgL and rnL and cfL):

				break

			mmGap = 0
			hgGap = 0
			rnGap = 0
			cfGap = 0

			for i in range(len(mmBlockSeq)):

				if (i == 0 and mmSta<mmBlockSta) or (mmBlockSeq[i] != '-' and i==mmSta-mmBlockSta+mmGap):

					staIdx = i

					mmAlignSta = mmBlockSta+i-mmGap

					hgSta = hgBlockSta+i-hgGap
					rnSta = rnBlockSta+i-rnGap
					cfSta = cfBlockSta+i-cfGap

				if (i == len(mmBlockSeq)-1) or (mmBlockSeq[i] != '-' and i==mmEnd-mmBlockSta+mmGap-1):

					mmAlignEnd = mmBlockSta+i-mmGap+1

					hgEnd = hgBlockSta+i-hgGap
					rnEnd = rnBlockSta+i-rnGap
					cfEnd = cfBlockSta+i-cfGap

					mmAlignSeq.append(mmBlockSeq[staIdx:i+1])
					hgAlignSeq.append(hgBlockSeq[staIdx:i+1])
					rnAlignSeq.append(rnBlockSeq[staIdx:i+1])
					cfAlignSeq.append(cfBlockSeq[staIdx:i+1])

					mmAlignCoord.append((mmAlignSta,mmAlignEnd))

					break

				if mmBlockSeq[i] == '-':
					mmGap += 1

				if hgBlockSeq[i] == '-':
					hgGap += 1

				if rnBlockSeq[i] == '-':
					rnGap += 1

				if cfBlockSeq[i] == '-':
					cfGap += 1

		elif mmEnd <= mmBlockSta:
			break

		else:

			while inF.readline() != '\n':
				pass

	inF.close()

#	print mmAlignCoord
#	print mmAlignSeq
#	print hgAlignSeq
#	print rnAlignSeq
#	print cfAlignSeq

	if len(mmAlignCoord)>0 and mmAlignCoord[0][0]==mmSta and mmAlignCoord[-1][1]==mmEnd:

		idxContinuity = 1

		for i in range(len(mmAlignCoord)-1):

			if mmAlignCoord[i][1] != mmAlignCoord[i+1][0]:

				idxContinuity = 0
				break

		mmSeq = ''.join(mmAlignSeq).replace('-','')
		hgSeq = ''.join(hgAlignSeq).replace('-','')
		rnSeq = ''.join(rnAlignSeq).replace('-','')
		cfSeq = ''.join(cfAlignSeq).replace('-','')

		if mmSeq==hgSeq==rnSeq==cfSeq and (mmSeq_input=='' or mmSeq_input==mmSeq):

			seqIdentity = 1

		else:

			seqIdentity = 0

		if idxContinuity and seqIdentity:

			return ('Y',[mmSeq,hgSeq,rnSeq,cfSeq])

		else:

			return ('N',[mmSeq,hgSeq,rnSeq,cfSeq])

	else:

		return ('N',[])


def cons_hg17_MRD(hgChr,hgSta,hgEnd,hgSeq=''):

	inF = open( \
		'/lab/bartel.2/jinkuk/hg17/8way/3utr_filtered/%s.3utr' % (hgChr,))

	qlen = hgEnd-hgSta

	hgAlignCoord = []
	hgAlignSeq = []
	mmAlignSeq = []
	rnAlignSeq = []
	cfAlignSeq = []

	while 1:

		line = inF.readline()

		if not line:
			break

		hgL = line.split()

		hgBlockSta = int(hgL[1])
		hgBlockEnd = hgBlockSta+int(hgL[2])
		hgBlockSeq = hgL[5].upper()

		if not (hgEnd<=hgBlockSta or hgBlockEnd<=hgSta):

			mmL = []
			rnL = []
			cfL = []

			while 1:

				line = inF.readline()

				if line == '\n':

					break

				if line[:2] == 'mm':

					mmL = line.split()
					mmBlockSta = int(mmL[1])
					mmBlockEnd = mmBlockSta+int(mmL[2])
					mmBlockSeq = mmL[5].upper()
					continue

				if line[:2] == 'rn':

					rnL = line.split()
					rnBlockSta = int(rnL[1])
					rnBlockEnd = rnBlockSta+int(rnL[2])
					rnBlockSeq = rnL[5].upper()
					continue

				if line[:2] == 'ca':

					cfL = line.split()
					cfBlockSta = int(cfL[1])
					cfBlockEnd = cfBlockSta+int(cfL[2])
					cfBlockSeq = cfL[5].upper()
					continue

			if not (mmL and rnL and cfL):

				break

			hgGap = 0
			mmGap = 0
			rnGap = 0
			cfGap = 0

			for i in range(len(hgBlockSeq)):

				if (i == 0 and hgSta<hgBlockSta) or (hgBlockSeq[i] != '-' and i==hgSta-hgBlockSta+hgGap):

					staIdx = i

					hgAlignSta = hgBlockSta+i-hgGap

					mmSta = mmBlockSta+i-mmGap
					rnSta = rnBlockSta+i-rnGap
					cfSta = cfBlockSta+i-cfGap

				if (i == len(hgBlockSeq)-1) or (hgBlockSeq[i] != '-' and i==hgEnd-hgBlockSta+hgGap-1):

					hgAlignEnd = hgBlockSta+i-hgGap+1

					mmEnd = mmBlockSta+i-mmGap
					rnEnd = rnBlockSta+i-rnGap
					cfEnd = cfBlockSta+i-cfGap

					hgAlignSeq.append(hgBlockSeq[staIdx:i+1])
					mmAlignSeq.append(mmBlockSeq[staIdx:i+1])
					rnAlignSeq.append(rnBlockSeq[staIdx:i+1])
					cfAlignSeq.append(cfBlockSeq[staIdx:i+1])

					hgAlignCoord.append((hgAlignSta,hgAlignEnd))

					break

				if hgBlockSeq[i] == '-':
					hgGap += 1

				if mmBlockSeq[i] == '-':
					mmGap += 1

				if rnBlockSeq[i] == '-':
					rnGap += 1

				if cfBlockSeq[i] == '-':
					cfGap += 1

		elif hgEnd <= hgBlockSta:

			break

		else:

			while inF.readline() != '\n':

				pass

	inF.close()

#	print hgSeq
#	print hgAlignCoord
#	print hgAlignSeq
#	print mmAlignSeq
#	print rnAlignSeq
#	print cfAlignSeq

	if len(hgAlignCoord)>0 and hgAlignCoord[0][0]==hgSta and hgAlignCoord[-1][1]==hgEnd:

		idxContinuity = 1

		for i in range(len(hgAlignCoord)-1):

			if hgAlignCoord[i][1] != hgAlignCoord[i+1][0]:

				idxContinuity = 0
				break

		mmSeq = ''.join(mmAlignSeq).replace('-','')
		rnSeq = ''.join(rnAlignSeq).replace('-','')
		cfSeq = ''.join(cfAlignSeq).replace('-','')

		if hgSeq==mmSeq==rnSeq==cfSeq:
			seqIdentity = 1
		else:
			seqIdentity = 0

		if idxContinuity and seqIdentity:
			return 'Y'
		else:
			return 'N'

	else:

		return 'N'


def blob2intList(blob):

	intList = ''.join(list(blob)).split(',')
	
	if '' in intList:
		intList.remove('')

	return map(int,intList)


def blob2list(blob):

	strList = ''.join(list(blob)).split(',')
	
	if '' in strList:
		strList.remove('')

	return strList


def hashSubtr(hash1,hash2):

	returnHash = {}

	hash1_keys = hash1.keys()
	hash2_keys = hash2.keys()

	hash1_keys.sort()
	hash2_keys.sort()

	if hash1_keys != hash2_keys:

		print 'Error in mybio.hashDiv: key inconsistency'
		sys.exit(0)

	for key in hash1_keys:

		returnHash[key] = []
		
		if len(hash1[key]) != len(hash2[key]):
			
			print 'Error in mybio.hashDiv: tuple type inconsistency'
			sys.exit(0)

		for i in range(len(hash1[key])):
		
			returnHash[key].append(hash1[key][i]-hash2[key][i])

	return returnHash


def getHumanRefSeqLenHash(cursor):

	cursor.execute('select refSeqID,len from hg_refSeq_len')
	 
	refSeqLen = {}
	 
	for (refSeqID_v,length) in cursor.fetchall():
		refSeqLen[refSeqID_v] = int(length)

	return refSeqLen


## return value: (refSeqID_v, position in refSeq starting from 1)

def coordMap_refSeqConcat2refSeq(cursor,refSeqConcat_pos):

	cursor.execute('select refSeqID,refSeqSta from hg_refSeqConcat2refSeq \
		where refSeqSta<=%s and refSeqEnd>=%s' % (refSeqConcat_pos,refSeqConcat_pos))

	result = cursor.fetchone()

	if not result:
		return ('',0)
	else:
		return (result[0],refSeqConcat_pos-long(result[1])+1)


def coordMap_refSeq2hg18(refSeq2hg18_hash,refSeqId_v,inputRefSeqSize,refSeqPos):

	refSeqId = refSeqId_v.split('.')[0]

	gCoordSet = sets.Set()

	for (chr,strand_refSeqOnChr,chrRefSeqAlign,refSeqSize,numMm) in refSeq2hg18_hash[refSeqId]:

		if inputRefSeqSize != -1 and inputRefSeqSize != int(refSeqSize):
			return []

		if strand_refSeqOnChr == '-':
			refSeqPos_adj = refSeqSize-refSeqPos+1
		else:
			refSeqPos_adj = refSeqPos

		gCoord = 0

		for (chrStart,refSeqStart,blockSize) in chrRefSeqAlign:

			if refSeqStart < refSeqPos_adj <= refSeqStart+blockSize:

				chrPos = chrStart+(refSeqPos_adj-refSeqStart)
				gCoord = (chr,strand_refSeqOnChr,chrPos,'match')

				break

		if gCoord == 0:
			gCoordSet.add(('','',-1,'insert'))
		else:
			gCoordSet.add(gCoord)
		
	return list(gCoordSet)


def load_refSeq2hg18():

	cursor.execute('''select qName,tName,strand,blockSizes,qStarts,tStarts,qSize,mismatches 
		from hg18_refSeqAli_mod order by qName''')

	results = cursor.fetchall()

	refSeq2hg18_hash = {}

	for (refSeqId,chr,strand,blockSizeList,refSeqStartList,chrStartList,refSeqSize,numMm) in results:
	
		blockSizeList = blob2intList(blockSizeList)
		refSeqStartList = blob2intList(refSeqStartList)
		chrStartList = blob2intList(chrStartList)

		addHash(refSeq2hg18_hash,refSeqId,(chr,strand,zip(chrStartList,refSeqStartList,blockSizeList),refSeqSize,numMm))

	con.close()

	return refSeq2hg18_hash


def coordMap_refSeq2hg18_32mer(refSeq2hg18_hash,refSeqId_v,inputRefSeqSize,refSeqPos,strand_readOnRefSeq):

	refSeqId = refSeqId_v.split('.')[0]

	if not refSeqId in refSeq2hg18_hash:
		return []

	chrReadAlignSet = sets.Set()

	for (chr,strand_refSeqOnChr,chrRefSeqAlign,refSeqSize,numMm) in refSeq2hg18_hash[refSeqId]:

		if inputRefSeqSize != -1 and inputRefSeqSize != int(refSeqSize):
			return []

		if strand_refSeqOnChr == '-':
			refSeqPos_adj = refSeqSize-refSeqPos+1
		else:
			refSeqPos_adj = refSeqPos

		if strand_readOnRefSeq == strand_refSeqOnChr:
			strand_readOnChr = '+'
		else:
			strand_readOnChr = '-'

		remainReadLen = 32
		chrReadAlign = 0

		for (chrStart,refSeqStart_adj,blockSize) in chrRefSeqAlign:

			if remainReadLen == 32:

				if refSeqStart_adj < refSeqPos_adj <= refSeqStart_adj+blockSize:

					chrPos = chrStart+(refSeqPos_adj-refSeqStart_adj)
					remainExonLen = chrStart+blockSize-chrPos+1

					if remainExonLen >= 32:

						chrReadAlign = (chr,strand_readOnChr,[(chrPos,1,32)])
						remainReadLen = 0
						break

					else:

						chrReadAlign = (chr,strand_readOnChr,[(chrPos,1,remainExonLen)])
						remainReadLen -= remainExonLen 
						prevRefSeqEnd = refSeqStart_adj+blockSize

			else:

				remainReadLen -= refSeqStart_adj-prevRefSeqEnd

				if remainReadLen > 0:

					if blockSize >= remainReadLen:
						
						chrReadAlign[2].append((chrStart+1,32-remainReadLen+1,remainReadLen))
						remainReadLen = 0
						break

					else:

						chrReadAlign[2].append((chrStart+1,32-remainReadLen+1,blockSize))
						remainReadLen -= blockSize
						prevRefSeqEnd = refSeqStart_adj+blockSize

				else:

					break

		if chrReadAlign != 0:

			chrReadAlignBlock = ';'.join([','.join(map(str,block)) for block in chrReadAlign[2]])
			chrReadAlignSet.add('%s%s:%s' % (chrReadAlign[0],chrReadAlign[1],chrReadAlignBlock))
		
	return list(chrReadAlignSet)


#def scanSiteObsolete(seq,seedList):
#
#	siteList = sets.Set()
#
#	seq = seq.upper()
#	seq = toRNA(seq)
#
#	for seed in seedList:
#
#		sm = rc(seed,"RNA")
#
#		for pos in (matchNmer(seq,sm[1:])):
#
#			m8 = 0; t1 = 0
#
#			if (pos>0 and seq[pos-1]==sm[0]):
#				m8 = 1
#
#			if (pos+6<len(seq) and seq[pos+6]=='A'):
#				t1 = 1
#
#			if (m8 == 0 and t1 == 0):
#				continue
#
#			matchSeq = toDNA(seq[pos-m8:pos+6+t1])
#
#			siteList.add((seed,t1,m8,matchSeq))
#
#	return siteList	
#
#
#def scanSites_obsolete2(chr,strand,start,seq,seedList):
#
#	siteList = sets.Set()
#
#	seq = mybio.toRNA(seq)
#
#	for (seed,) in seedList:
#
#		sm = mybio.rc(seed,"RNA")
#
#		for pos in (mybio.matchNmer(seq,sm[1:])):
#
#			if pos == 0 or pos == 9:
#				continue
#
#			m8 = 0; t1 = 0
#
#			if (pos>0 and seq[pos-1]==sm[0]):
#				m8 = 1
#
#			if (pos+6<len(seq) and seq[pos+6]=='A'):
#				t1 = 1
#
#			if (m8 == 0 and t1 == 0):
#				continue
#
#			offset = pos
#
#			if (strand == '-'):
#				offset = len(seq)-(offset+6)
#
#			matchSeq = mybio.toDNA(seq[pos-1:pos+7])
#
#			siteList.add((seed,chr,strand,long(start)+offset,t1,m8,matchSeq))
#
#	return siteList


## idx: index of the 7th position of seed pairing

def scanSeedMatch(seq,seedList):

	siteList = sets.Set()

	for seed in seedList:

		sm = rc(seed,"RNA")

		for idx in (matchNmer(seq,sm[1:])):

			m8 = 0; t1 = 0

			matchSeq = toDNA(seq[idx:idx+6])

			if (idx>0 and seq[idx-1]==sm[0]):
				matchSeq = toDNA(seq[idx-1]) + matchSeq
				m8 = 1

			if (idx+6<len(seq) and seq[idx+6]=='A'):
				matchSeq = matchSeq + toDNA(seq[idx+6])
				t1 = 1

			if (m8 == 0 and t1 == 0):
				continue

			siteList.add((idx,seed,t1,m8,matchSeq))

	return siteList


## seq5p: mRNA sequence of maxium 30 nt long, up to 8th position of the seed pairing
## seq3p: mRNA sequence of maxium 30 nt long, from the 1st position of the seed pairing

def score_AUcontent(seq5p,seq3p,t1,m8):
	
	seq5p = rev(seq5p)

	l_index = 1
	score = 0
	total = 0

	if m8==1:
		denominator = float(1)
	else:
		denominator = float(2)

	for i in range(l_index,l_index+30):

		if i>=len(seq5p) or seq5p[i] in ['A','U']:
			score += 1/denominator

		total += 1/denominator
		denominator += 1

	if t1==0:
		h_index = 29
		if len(seq3p)>0 and seq3p[0] in ['A','U']:
			score += 1/2.
		total += 1/2.
	else:
		h_index = 30

	denominator = float(2)

	for i in range(1,1+h_index):

		if i>=len(seq3p) or seq3p[i] in ['A','U']:
			score += 1/denominator

		total += 1/denominator
		denominator += 1

	return score/total


## mrnaSeq: 5'->3' mRNA seq up to the 9th position from start of the seed match
## mirSeq: 5'->3' miR seq from the 9th position to the end

def score_pairing(mrnaSeq,mirSeq):

	mrnaSeq_N_RC = 'N'*7 + rc(mrnaSeq,'RNA') + 'N'*20
	globalMaxScore = 0

	for i in range(len(mrnaSeq)+7-4):

		offset = abs(7-i)
		pairing = []

		for j in range(len(mirSeq)):

			if mirSeq[j]==mrnaSeq_N_RC[i+j]:
				pairing.append(1)
			else:
				pairing.append(0)

		maxScore = 0
		region = 0  # 0: non-contiguous, 1: non-core, contiguous, 2: core, continguous

		for j in range(len(mirSeq)):

			if region >= 1:

				if pairing[j]==1:

					if 4<=j<=7:
						score += 1
						region = 2
					else:
						score += 0.5

				else:

					if region==2 and score>maxScore:
						maxScore = score

					region = 0

			else:

				if pairing[j]==1:

					if 4<=j<=7:
						score = 1
						region = 2
					else:
						score = 0.5
						region = 1

		if offset>2:
			maxScore -= (offset-2)*0.5

		if maxScore > globalMaxScore:
			globalMaxScore = maxScore

	return globalMaxScore


## pos: 8th position of seed pairing

def contextScore(mrnaSeq,(seed,t1,m8),pos,dist2end,cursor,species='hsa'):

	type = (t1,m8)

	## Distance contriubution

	cScore_dist = dist_s[type]*dist2end + dist_y[type] - meanValue[type]

	## AU richness contribution

	auScore = score_AUcontent(mrnaSeq[:pos+1],mrnaSeq[pos+7:],t1,m8)
	cScore_au = au_s[type]*auScore + au_y[type] - meanValue[type]

	## 3' pairing contribution for all members of the miR family & context score calculation

	cursor.execute('select mirID,seq from %s_mir where substring(seq,2,7)="%s"' % (species,seed,))
	
	cScore_all = {}

	for (mirID,mirSeq) in cursor.fetchall():

		cScore_pairing = \
			pairing_s[type]*score_pairing(mrnaSeq[:pos],mirSeq[8:]) + pairing_y[type] - meanValue[type]
		cScore_all[mirID] = (meanValue[type], cScore_pairing, cScore_au, cScore_dist, \
			 meanValue[type] + cScore_pairing + cScore_au + cScore_dist)

	return cScore_all


def roundup(val):

	return math.floor(val+0.5)


def median(list):

	list.sort()

	n = len(list)

	if n % 2 == 0:

		return float(list[n/2-1]+list[n/2])/2

	else:

		return list[n//2]


fac = lambda n:[1,0][n>0] or fac(n-1)*n


#def percentileFromBottom(list,k):
#
#	list.sort()
#
#	n = len(list)
#
#	if n % k == 0:
#
#		return float(list[n/k-1]+list[n/k])/2
#
#	else:
#
#		return list[n//k]


def percentileFromBottom(list,kL):

	# 0 < k < 100

	list.sort()
	n = float(len(list))

	results = []

	for k in kL:

		if k in [0,100]:
			raise Error

		idx = n*k/100.
		idx_int = int(idx)

		if idx == idx_int:
			results.append((list[idx_int-1] + list[idx_int])/2.)
		else:
			results.append(list[idx_int])

	return tuple(results)


def binoTest(n,m,p,tail):

	if tail == 1:
		
		pv = 0

		for k in range(m+1):
			pv = pv + nchoosek(n,k) * (p)**k * (1-p)**(n-k)
	   
	else:
		
		m = min(m,n-m)

		pv = 0

		for k in range(m+1):
			pv = pv + nchoosek(n,k) * (p)**k * (1-p)**(n-k)

		for k in range(max(n-m,m+1),n+1):
			pv = pv + nchoosek(n,k) * (p)**k * (1-p)**(n-k)
		
	return pv


def nchoosek(n,k):

	k = min(k,n-k)

	top = 1

	for i in range(n,n-k,-1):
		top *= i

	bottom = 1

	for i in range(k,0,-1):
		bottom *= i

	return top/bottom

#def multinomialTest(f_obs,f_exp=None):
#
#	k = len(f_obs)	# number of groups
#	n = sum(f_obs)
#
#	if f_exp == None:
#		f_exp = [n/float(k)] * len(f_obs)	# create k bins with = freq.
#
#	for i in range(len(f_obs)):
#		chisq = chisq + (f_obs[i]-f_exp[i])**2 / float(f_exp[i])
#
#	return chisq, stats.chisqprob(chisq, k-1)


def mergeSegments(segmentAll,space=0):
 
	segmentAll.sort(lambda a,b: cmp(long(a[0]),long(b[0])))

	segmentAllMerged = []
		
	i = 0

	while i < len(segmentAll):

		(segmentS1,segmentE1) = segmentAll[i]

		curE = segmentE1

		j = i+1

		while j < len(segmentAll):

			(segmentS2,segmentE2) = segmentAll[j]
		
			if curE+space<segmentS2:
				break

			curE = max(curE,segmentE2)
			j += 1
		
		segmentAllMerged.append((segmentS1,curE))
		
		i = j

	return segmentAllMerged


def mergeSegmentsSum(segmentAll,space=0):
 
	segmentAll.sort(lambda a,b: cmp(long(a[0][0]),long(b[0][0])))

	segmentAllMerged = []
		
	i = 0

	while i < len(segmentAll):

		((segmentS1,segmentE1),value1) = segmentAll[i]

		curE = segmentE1
		sum = value1

		j = i+1

		while j < len(segmentAll):

			((segmentS2,segmentE2),value2) = segmentAll[j]
		
			if curE+space<segmentS2:
				break

			curE = max(curE,segmentE2)
			sum += value2
			j += 1
		
		segmentAllMerged.append(((segmentS1,curE),sum))
		
		i = j

	return segmentAllMerged


def gset2geneL(gsetName):

	gsetFileName = 'cAll.all.v3.0.symbols.gmt'

	inGsetFile = open('%s/DB/%s' % (dataDir,gsetFileName))

	for line in inGsetFile:

		tokL = line[:-1].split('\t')

		if tokL[0].upper()==gsetName:
			geneL = tokL[2:]
			break

	inGsetFile.close()

	return geneL


def gset2gsetUrl(gsetName):

	gsetFileName = 'cAll.all.v3.0.symbols.gmt'

	inGsetFile = open('%s/DB/%s' % (dataDir,gsetFileName))

	for line in inGsetFile:

		tokL = line[:-1].split('\t')

		if tokL[0].upper()==gsetName:
			url = tokL[1]
			break

	inGsetFile.close()

	return url 



## classes

(con,cursor) = connectDB()

class targetSite:

	pass

class miRNA:

	pass

# bug: fetch only the first entry, when there are more than one loci for the given refSeqId

class transcript:

	def __init__(self,refSeqId,huGeVer=huGeVer):

		cursor.execute('select geneName,chrom,txStart,txEnd,cdsStart,cdsEnd,exonStarts,exonEnds,strand from refFlat_%s where name="%s"' % (huGeVer,refSeqId))
		row = cursor.fetchone()

		if row:

			self.geneName = row[0]
			self.refSeqId = refSeqId
			self.chrom = row[1]
			self.chrNum = self.chrom[3:]
			self.txnSta = row[2]
			self.txnEnd = row[3]
			self.txnLen = self.txnEnd - self.txnSta
			self.cdsSta = row[4]
			self.cdsEnd = row[5]
			self.exnStaL = blob2intList(row[6])
			self.exnEndL = blob2intList(row[7])
			self.strand = row[8]
			self.exnL = [(self.exnStaL[i],self.exnEndL[i]) for i in range(len(self.exnStaL))]
			self.exnLen = sum([e-s for (s,e) in self.exnL])

			self.cdsL = []

			for (s,e) in self.exnL:

				if s<=self.cdsSta and self.cdsSta<=e:
					s = self.cdsSta

				if s<=self.cdsEnd and self.cdsEnd<=e:
					e = self.cdsEnd

				if self.cdsSta<=s and e<=self.cdsEnd:
					self.cdsL.append((s,e))

			self.cdsLen = sum([e-s for (s,e) in self.cdsL])

		else:
			
			raise Exception

	def txnOverlap(self,region):

		return overlap((self.chrNum,self.txnSta,self.txnEnd),region)

	def cdsOverlap(self,region):

		total = 0

		for (cdsS,cdsE) in self.cdsL:

			total += overlap((self.chrNum,cdsS,cdsE),region)

		return total


	def exnOverlap(self,region):

		total = 0

		for (exnS,exnE) in self.exnL:

			total += overlap((self.chrNum,exnS,exnE),region)

		return total



class gene:

	def __init__(self,name,huGeVer=huGeVer):

		name = name.upper()

		cursor.execute('select geneName from refFlat_%s where upper(geneName)="%s" or upper(name)="%s"' % (huGeVer,name,name))
		row = cursor.fetchone()

		self.huGeVer = huGeVer

		if row:

			self.geneName = row[0]

		else:

			cursor.execute('select geneName from hugo where upper(geneName)="%s" or find_in_set("%s",upper(oldNames))>0 or \
				find_in_set("%s",upper(otherNames))>0 or find_in_set("%s",upper(refSeqIds))>0' % (name,name,name,name))
			row = cursor.fetchone()

			if row:
				self.geneName = row[0]

	def longestRefSeqId(self):

		cursor.execute('select name from refFlat_%s where upper(geneName)="%s" order by txEnd-txStart desc' % (self.huGeVer,self.geneName))
		return cursor.fetchone()[0]
