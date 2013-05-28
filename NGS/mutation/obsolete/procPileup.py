#!/usr/bin/python

import sys, os, re, getopt
import mybasic


pattL = map(re.compile, ('\$','\^.','\+[0-9]+[ACGTNacgtn]+','\-[0-9]+[ACGTNacgtn]+'))

def main():

	inFile = sys.stdin
	outFile = sys.stdout

	for line in inFile:

		tL = line.split('\t')

		baseStr = tL[-2]
		
		for patt in pattL:
			baseStr  = patt.sub('',baseStr)

		ref = baseStr.count('.') + baseStr.count(',')

		baseStr = baseStr.replace('.','').replace(',','').upper()

		outFile.write('%s:%s,%s,%s,%s,%s\n' % (tL[0],tL[1],tL[3],tL[2].upper(),ref,baseStr))
	
	outFile.close()

#optL, argL = getopt.getopt(sys.argv[1:],'i:o:l:',[])
#
#optH = mybasic.parseParam(optL)
#
#if '-i' in optH and '-o' in optH and '-l' in optH:
#
#	main(optH['-i'], optH['-o'], int(optH['-l']))

main()
