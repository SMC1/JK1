#!/usr/bin/python

import sys


class seqRead:
	
	def __init__(self,l):

		self.raw = l

		self.seq = l[0][0][1:]
		self.nLoci = int(l[0][1].split(' ')[0])
		self.pairRel= l[0][1].split(' ')[1]

		self.nBlocks = len(l)-1

		self.locusInfo = []

		for i in range(1,self.nBlocks+1):
			self.locusInfo.append((l[i][2],l[i][3]))

		if self.nBlocks>0 and len(l[1]) >= 6:
			self.insertLen = int(l[1][5].split(',')[1].split(':')[1])

			if self.pairRel == 'paired':
				self.pairType= l[1][5].split(',')[2].split(':')[1]


class gsnapResult(file):
	
	def next(self):

		l1 = []

		while 1:

			line = file.next(self)

			if line=='\n':
				break

			l1.append(line[:-1].split('\t'))

		l2 = []

		while 1:

			line = file.next(self)

			if line=='\n':
				break

			l2.append(line[:-1].split('\t'))

		return seqRead(l1), seqRead(l2)


if len(sys.argv) >= 3:
	inFileName = sys.argv[1]
	outFileName = sys.argv[2]
else:
	inFileName = '/Data2/GH.txt'
	outFileName = 'GH_ft.txt'

result = gsnapResult(inFileName)
outFile = open(outFileName, 'w')


for rL in result:

	if rL[0].pairRel=='unpaired' and rL[0].nBlocks<=1 and rL[1].nBlocks<=1:
		continue

	chosenForDisplay = False

	if rL[0].pairRel=='unpaired' and rL[0].nBlocks>=1 and rL[1].nBlocks>=1:
		chosenForDisplay = True

#	if (rL[0].pairRel=='paired' and rL[0].pairType!='scramble') or (rL[0].pairRel=='concordant' and (rL[0].insertLen<50 or rL[0].insertLen>1000)) or (rL[0].pairRel=='unpaired' and rL[0].nBlocks>=1 and rL[1].nBlocks>=1):
#		chosenForDisplay = True

#	maxIndelSize = 0
#
#	for i in (0,1):
#
#		if rL[i].nBlocks > 1:
#
#			for j in range(rL[i].nBlocks):
#
#				indelType, indelSize = rL[i].locusInfo[j][1].split(',')[0].split('..')[0].split(':')
#
#				if indelType in ('ins','del') and indelSize > maxIndelSize:
#					maxIndelType = indelType
#					maxIndelSize = int(indelSize)
#
#	if maxIndelSize >= 50:
#		chosenForDisplay = True

	if chosenForDisplay:

		for i in (0,1):

			outFile.write('\t'.join(rL[i].raw[0][:2])+'\n')

			for l in rL[i].raw[1:]:
				outFile.write('\t'.join(l)+'\n')

			outFile.write('\n')

			#print r1.pairRel, r1.seq, r1.nLoci, r2.seq, r2.nLoci, '\n'
