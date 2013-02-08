#!/usr/bin/python

import sys,getopt,re
import mybasic

optL, argL = getopt.getopt(sys.argv[1:],'i:j:k:o:',[])

optH = mybasic.parseParam(optL)

inputFile=optH['-i']
inputDirN=re.match('(.*)/refFlat_hg1.\.txt',inputFile).group(1)
genelist=optH['-j']
filteredname=optH['-k']
if '-o' in optH:
	outputDirN=optH['-o']
else:
	outputDirN=inputDirN

def loadRefFlatByGene(refFlatFileName):

	h = {}

	for line in open(refFlatFileName):
	
		r = processRefFlatLine(line)

		mybasic.addHash(h, r['geneName'], r)
	
	return h


def processRefFlatLine(line):

	tokL = line.rstrip().split('\t')

	h = {}

	h['geneName'] = tokL[0]
	h['exnList'] = map(lambda x,y: (int(x),int(y)), tokL[9].split(',')[:-1], tokL[10].split(',')[:-1])
	h['exnCount']=len(h['exnList'])
	h['line'] = line

	return h

refFlat=loadRefFlatByGene(inputFile)

filtered={}

for line in open(genelist):
	for gene in refFlat:
		if line[:-1]==gene or re.match('%s[^A-Z]{1}'%line[:-1],gene[0:len(line)])!=None:
			for seq in refFlat[gene]:
				lastexon=seq['exnList'][seq['exnCount']-1]
				if not filtered.has_key((gene,lastexon)):
					filtered[(gene,lastexon)]=seq['line']

fo=open('%s/refFlat_%s.txt'%(outputDirN,filteredname),'w')
for key in filtered:
	fo.write(filtered[key])
fo.close()


