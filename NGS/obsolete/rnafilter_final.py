#!/usr/bin/python
# list input, output data count sort

import sys, re, os, operator

if len(sys.argv) >= 3:
	inFileName = sys.argv[1]
	outFileName = sys.argv[2]
else:
	inFileName = '/home/gye_hyeon/RNASeq/S02.txt'
	outFileName = '/home/gye_hyeon/RNASeq/list_result_sort.txt'

outFile = open(outFileName, 'w')
inFile = open(inFileName)

#readlines() => list1 add
inlist1 = []
resultlist = []
inlist2 = []
inlist2 = inFile.readlines()
chrlist = []
cntlist = []
sumlist = []
roop = 1
cnt = 1
while roop:
#	print 'Count %s' % cnt
	cnt += 1
	scount = 0
	chrcnt = 0
	inlist1	= inlist2
	inlist2 = []
#list1
	locL = []
	for y in inlist1[0].strip().split('\t\t'):
		for loc in y.rstrip().split(','):
			locL.append(re.match('([^;]+):([0-9]+)-([0-9]+)([-+])',loc).groups())
	resultlist.append('\n'+'Chr '+inlist1[0].rstrip())		

#list2
	for line2 in inlist1:
		locR = []
		for x in line2.strip().split('\t\t'):
			for loc2 in x.rstrip().split(','):
				locR.append(re.match('([^;]+):([0-9]+)-([0-9]+)([-+])',loc2).groups())

		#chr1,chr2 == chr3,chr4 #start locL+-200  =>  locR
		if ( (locL[0][0] == locR[0][0]) and (locL[1][0] == locR[1][0]) ) and ( (( int(locL[0][1])+200 >= int(locR[0][1]) >= int(locL[0][1])-200 ) and ( int(locL[0][2])+200 >= int(locR[0][2]) >= int(locL[0][2])-200 )) and (( int(locL[1][1])+200 >= int(locR[1][1]) >= int(locL[1][1])-200 ) and ( int(locL[-1][2])+200 >= int(locR[-1][2]) >= int(locL[-1][2])-200 ) )):
		#same locL == locR
			if  (locL[0][1] == locR[0][1] and locL[0][2] == locR[0][2]) and (locL[1][1] == locR[1][1] and locL[-1][2] == locR[-1][2]):
				scount += 1
				continue
			resultlist.append(line2.strip())
			chrcnt += 1

		#reverse chr #start locL+-200  =>  locR
		elif ( (locL[0][0] == locR[1][0] ) and ( locL[1][0] == locR[0][0]) ) and ( (( int(locL[0][1])+200 >= int(locR[1][1]) >= int(locL[0][1])-200 ) and ( int(locL[0][2])+200 >= int(locR[-1][2]) >= int(locL[0][2])-200 )) and (( int(locL[1][1])+200 >= int(locR[0][1]) >= int(locL[1][1])-200 ) and ( int(locL[-1][2])+200 >= int(locR[0][2]) >= int(locL[-1][2])-200 )) ):
		#same locL == locR
			if  (locL[0][1] == locR[1][1] and locL[0][2] == locR[-1][2]) and (locL[1][1] == locR[0][1] and locL[-1][2] == locR[0][2]):
				scount += 1
				continue
			resultlist.append(line2.strip())
			chrcnt += 1
		else:
			inlist2.append(line2)

	# chr#:###-### \t\t #:###-###- \t chrcnt
	chrlist.append('chr'+inlist1[0].rstrip())
	cntlist.append(chrcnt)

#	chrlist.append('chr'+inlist1[0].rstrip()+'\t,'+str(chrcnt))
#	print 'Same %s'% scount
	if inlist2 == []:
		roop = 0

#for a in chrlist:
#	print a

sumlist = zip(chrlist, cntlist)
sumlist.sort(key=operator.itemgetter(1), reverse=True )
for f in sumlist:
	print f[0], f[1]

for rline in resultlist:
	outFile.write(rline+'\n')
inFile.close()
