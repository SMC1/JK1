import os,re,sys,getopt
import mybasic


optL, argL = getopt.getopt(sys.argv[1:],'i:',[])

optH = mybasic.parseParam(optL)

inputDirN=optH['-i']

inFileNL = os.listdir(inputDirN)
inFileNL = filter(lambda x: re.match('.*lastExon.txt',x),inFileNL)

print len(inFileNL)

for inFileN in inFileNL:
	sampN=re.match('(.*)lastExon.txt',inFileN).group(1)
	#print sampN
	os.rename('%s/%s'%(inputDirN, inFileN),'%s/%sEGFR.txt'%(inputDirN,sampN))
