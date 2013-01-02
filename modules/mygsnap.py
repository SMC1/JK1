#!/usr/bin/python

import sys, re, numpy
import mygenome




class segInfo:

	def __init__(self,seg):
		
		self.seg = seg
		self.staOffset,self.endOffset = map(int,seg[1].split('..'))
		self.span = self.endOffset - self.staOffset + 1
		self.numMatch = int(re.search('matches:([0-9]*),',seg[3]).group(1))
		self.len = len(seg[0])

		self.percMatch = float(self.numMatch) / self.span * 100. # deprecated
		self.numMismatch = self.span - self.numMatch # deprecated

		rm = re.search('label_[12]:([^,\t]*)',seg[3])
		if rm:
			self.label = rm.group(1)
		else:
			self.label = ''

	def __print__(self):
		print self.seg
		

class seqMatch:

	def __init__(self,segL): # take newline- and tab-delimited list
		'''
		__init__
		'''

		self.segL = segL
		self.locusL = [mygenome.locus(s[2]) for s in segL]

	def getSegInfo(self):

		return [segInfo(seg) for seg in self.segL]

	def mergedLocusL(self,gap=10):

		return mygenome.mergeLoci(self.locusL, gap)

	def pairInfo(self):

		insertLen, pairType = None, None

		if len(self.segL[0]) >= 6:

			infoL = self.segL[0][5].split(',')

			insertLen = int(infoL[1].split(':')[1])

			if len(infoL) >= 3:
				pairType = infoL[2].split(':')[1]

		return insertLen, pairType

	def score(self):

		return int(re.search('align_score:([0-9]*)',self.segL[0][4]).group(1))

	def numMatch(self,seq_read):

		return sum(self.posProfile(seq_read)) - len(self.segL) + 1
		#return sum([int(re.search('matches:([0-9]*)',seg[3]).group(1)) for seg in self.segL])

	def posProfile(self,seq_read):

		seqLen = len(seq_read)

		profile = [0,]*seqLen
		
		for seg in self.segL:

			seq_match = seg[0]

			for p in range(min(seqLen,len(seq_match))):

				if seq_match[p] == '-':
					continue

				profile[p] = int(seq_match[p].isupper() and seq_read[p]!='N')

		return profile

#	def fun():
#	'''
#	fun: returns list of xxx
#
#	fewqfewq
#	fewqfewq
#	fqewfewq
#	'''
#		
#		return ([(t1,e1),(t2,e2)...],[(t1,e1),(t2,e2)...])


class seqRead:
	
	def __init__(self,l): # take newline- and tab-delimited list

		self.raw = l
		self.nLoci = int(l[0][1].split(' ')[0])

		if ' ' in l[0][1]:
			self.pairRel = l[0][1][l[0][1].find(' ')+1:]
		else:
			self.pairRel = ''

	def seq(self):
		return self.raw[0][0][1:]

	def rawText(self):
		return '\t'.join(self.raw[0][:2])+'\n' + '\n'.join(['\t'.join(t) for t in self.raw[1:]])+'\n'

	def matchL(self):
		return [seqMatch([l.split('\t') for l in m.lstrip().split('\n,')]) for m in '\n'.join(['\t'.join(t) for t in self.raw[1:]]).split('\n ')]

	def pairInfo(self):
		return self.matchL()[0].pairInfo()


class gsnapFile(file):

	def __init__(self, fileName, paired=True):

		self.paired = paired

		return super(gsnapFile,self).__init__(fileName)
	
	def next(self):

		l1 = []

		while 1:

			line = file.next(self)

			if line=='\n':
				break

			l1.append(line[:-1].split('\t'))
				
		if self.paired:

			l2 = []

			while 1:

				line = file.next(self)

				if line=='\n':
					break

				l2.append(line[:-1].split('\t'))
					
			return seqRead(l1), seqRead(l2)

		else:

			return seqRead(l1)
