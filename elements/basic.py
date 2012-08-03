#!/usr/bin/python

import sys, getopt
import mybasic


def function(inFileName,outFileName):

	inFile = open(inFile)
	outFile = open(outFileName, 'w')


optL, argL = getopt.getopt(sys.argv[1:],'i:o:t',[])

optH = mybasic.parseParam(optL)

if '-i' in optH and '-o' in optH:

	function(optH['-i'], optH['-o'])

# function('','')
