#!/usr/bin/python

import sys, os, re, getopt
import mybasic


patt = re.compile('(\$)|(\^.)')
patt_indel = re.compile('([\+\-]{1})([0-9]+)')

def main(inFilePath,outFileDir,ref,qualCutoff=15):

	inFileTitle = re.match('(.*).recal.bam', os.path.basename(inFilePath)).group(1)

	inFile = os.popen('samtools mpileup -f %s %s' % (ref, inFilePath))
	outFile = 0

	curChrom = ''

	for line in inFile:

		tL = line[:-1].split('\t')

		if tL[0] != curChrom:
			if outFile:
				outFile.close()
			outFile = open('%s/%s_%s.pileup_proc' % (outFileDir,inFileTitle,tL[0]),'w')
			curChrom = tL[0]

		baseStr = tL[-2]
		qualStr = tL[-1]
		
		indelL = patt_indel.findall(baseStr)
		
		for (sign,num) in indelL:
			baseStr = re.sub('\%s%s[ACGTNacgtn]{%s}' % (sign,num,num),'',baseStr)

		baseStr  = patt.sub('',baseStr)

		if len(baseStr) != len(qualStr):
			print 'Error:', baseStr, qualStr
			raise Exception

		baseL = []

		for i in range(len(baseStr)):
			if ord(qualStr[i])-33 >= qualCutoff:
				baseL.append(baseStr[i])

		baseStr = ''.join(baseL)
		total = len(baseStr)

		ref = baseStr.count('.') + baseStr.count(',')

		baseStr = baseStr.replace('.','').replace(',','').upper()

		outFile.write('%s:%s,%s,%s,%s,%s\n' % (tL[0],tL[1],total,tL[2].upper(),ref,baseStr))
	
	outFile.close()

	print 'Success: %s' % inFileTitle

if __name__ == '__main__':

	optL, argL = getopt.getopt(sys.argv[1:],'i:o:q:r:',[])

	optH = mybasic.parseParam(optL)

	if '-i' in optH and '-o' in optH and '-q' in optH and '-r' in optH:

		main(optH['-i'], optH['-o'], optH['-r'], int(optH['-q']) )
