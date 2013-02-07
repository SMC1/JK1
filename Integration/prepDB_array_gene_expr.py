#!/usr/bin/python

import sys, getopt
import mybasic


def function(inGctFileName):

	inFile = open(inGctFile)


optL, argL = getopt.getopt(sys.argv[1:],'i:o:t',[])

optH = mybasic.parseParam(optL)

if '-i' in optH and '-o' in optH:

	function(optH['-i'], optH['-o'])

function('/EQL1/NSL/array_gene/NSL_GBM_93_zNorm.gct')
