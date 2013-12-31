#!/usr/bin/python

import sys, getopt, re, gzip, datetime
import mybasic, mygenome


def loadExonH():

	exnH = {}

	refFlatH = mygenome.loadRefFlatByChr()

	for chrom in refFlatH.keys():
		
		if chrom not in exnH:
			exnH[chrom] = []

		for tH in refFlatH[chrom]:

			for i in range(len(tH['exnList'])):
				exnH[chrom].append(tH['exnList'][i])

		exnH[chrom] = list(set(exnH[chrom]))

		exnH[chrom].sort(lambda x,y: cmp(x[1],y[1]))
		exnH[chrom].sort(lambda x,y: cmp(x[0],y[0]))

#	for chrom in exnH:
#		if len(chrom) > 6:
#			continue
#		for i in range(len(exnH[chrom])):
#			sys.stdout.write('%s\t%s\t%s\n' % (chrom, int(exnH[chrom][i][0])-1, int(exnH[chrom][i][1])))
	return exnH

def get_cnt_by_qual(line, th):
	tL = line.rstrip().split('\t')
	patt = re.compile('(\$)|(\^.)')
	patt_indel = re.compile('([\+\-]{1})([0-9]+)')

	baseStr = tL[-2]
	qualStr = tL[-1]
	indelL = patt_indel.findall(baseStr)
	for (sign,num) in indelL:
		baseStr = re.sub('\%s%s[ACGTNacgtn]{%s}' % (sign,num,num),'',baseStr)
	baseStr = patt.sub('',baseStr)

	if len(baseStr) != len(qualStr):
		print 'Error:', baseStr,qualStr
		print line
		raise Exception
	
	if th < 1:
		return len(baseStr)
	else:
		baseL = []
		for i in range(len(baseStr)):
			if ord(qualStr[i]) - 33 >= th:
				baseL.append(baseStr[i])
		return len(''.join(baseL))

def main(inFilePath,outFilePath):

	exnH = loadExonH()

	depthH = {'0':{}, '15':{}, '20':{}, '30':{}}

	exnChr = 'chr1'
	exnIdx = 0

	if inFilePath[-3:] == '.gz':
		inFile = gzip.open(inFilePath, 'rb')
	else:
		inFile = open(inFilePath)

	for line in inFile:

		tokL = line.split('\t')
		chrom, pos, cnt = tokL[0], int(tokL[1]), int(tokL[3])

		if chrom==exnChr and exnIdx==len(exnH[exnChr]):
			continue

		if chrom != exnChr:
			exnChr = chrom
			exnIdx = 0

		while exnIdx < len(exnH[exnChr]) and exnH[exnChr][exnIdx][1] < pos:
			exnIdx += 1

		if exnIdx < len(exnH[exnChr]) and exnH[exnChr][exnIdx][0] < pos <= exnH[exnChr][exnIdx][1]:
			for dt in ['0', '15', '20', '30']:
				cnt = get_cnt_by_qual(line, int(dt))
				if cnt > 1000:
					mybasic.incHash(depthH[dt], 1001, 1)
				else:
					mybasic.incHash(depthH[dt], cnt, 1)

	totalLen = 0

	for chrom in exnH:

		curPos = 0

		for exn in exnH[chrom]:

			curPos = max(curPos,exn[0])
			totalLen += exn[1]-curPos
			curPos = exn[1]
			
	for dt in ['0','15','20','30']:
		depthH[dt][0] = totalLen - sum(depthH[dt].values())


	for dt in ['0','15','20','30']:
		outFile = open(outFilePath + '_mq' + dt, 'w')
#		for i in range(max(depthH[dt].keys())+1):
		for i in range(1001):
			if i in depthH[dt]:
				d = depthH[dt][i]
			else:
				d = 0
			outFile.write('%d\t%d\n' % (i,d))
		if 1001 in depthH[dt]:
			outFile.write('1001\t%d\n' % depthH[dt][1001])
		else:
			outFile.write('1001\t0\n')
		outFile.flush()
		outFile.close()



if __name__ == '__main__':
	optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])
	optH = mybasic.parseParam(optL)

	main(optH['-i'],optH['-o'])
	#main('/EQL1/NSL/Exome/mutation/671T_Br1_WXS_trueSeq.pileup','/EQL1/NSL/Exome/mutation/671T_Br1_WXS_trueSeq.depth')
#	main('/EQL3/pipeline/SGI20131212_xsq2mut/S4C_B_SS/S4C_B_SS.pileup','/EQL3/pipeline/SGI20131212_xsq2mut/S4C_B_SS/S4C_B_SS.depth')
#	main('/EQL4/pipeline/dcov/S6C_B_SS.pileup', '/EQL4/pipeline/dcov/S6C_B_SS.depth')
#	main('/EQL4/pipeline/dcov/S4C_B_SS.pileup', '/EQL4/pipeline/dcov/S4C_B_SS.depth')
