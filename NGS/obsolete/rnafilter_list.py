#!/usr/bin/python
# list input

import sys, re, os

if len(sys.argv) >= 3:
	inFileName = sys.argv[1]
	resultFileName = sys.argv[2]
else:
	inFileName = '/home/gye_hyeon/RNASeq/S02.txt'
	resultFileName = '/home/gye_hyeon/RNASeq/list_result.txt'

resultFile = open(resultFileName, 'w')
inFile = open(inFileName)

#readlines() => list1 add
inlist1 = []
resultlist = []

inlist3 = inFile.readlines()

roop = 1
cnt = 1
while roop:
	print 'Count %s' % cnt
	cnt += 1
	scount = 0
	inlist1	= inlist3
#	inlist2 = inlist3
	inlist3 = []
#list1
	locL = []
	for y in inlist1[0].strip().split('\t\t'):
		for loc in y.rstrip().split(','):
			locL.append(re.match('([^;]+):([0-9]+)-([0-9]+)([-+])',loc).groups())
	resultlist.append('\n'+'Chr '+inlist1[0].rstrip())		
#	outFile.write('Line%s %s:%s-%s%s\t\t' % (ccount,locL[0][0],locL[0][1],locL[0][2],locL[0][3]))
#	outFile.write('%s:%s-%s%s\n' % (locL[1][0],locL[1][1],locL[-1][2],locL[1][3]))

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

		#reverse chr #start locL+-200  =>  locR
		elif ( (locL[0][0] == locR[1][0] ) and ( locL[1][0] == locR[0][0]) ) and ( (( int(locL[0][1])+200 >= int(locR[1][1]) >= int(locL[0][1])-200 ) and ( int(locL[0][2])+200 >= int(locR[-1][2]) >= int(locL[0][2])-200 )) and (( int(locL[1][1])+200 >= int(locR[0][1]) >= int(locL[1][1])-200 ) and ( int(locL[-1][2])+200 >= int(locR[0][2]) >= int(locL[-1][2])-200 )) ):
		#same locL == locR
			if  (locL[0][1] == locR[1][1] and locL[0][2] == locR[-1][2]) and (locL[1][1] == locR[0][1] and locL[-1][2] == locR[0][2]):
				scount += 1
				continue
			resultlist.append(line2.strip())
		else:
			inlist3.append(line2)

	print 'Same %s'% scount
	if inlist3 == []:
		roop = 0

for rline in resultlist:
	resultFile.write(rline+'\n')

inFile.close()
