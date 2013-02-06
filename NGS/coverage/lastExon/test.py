import os,getopt,sys,re
import mybasic
	
	

optL, argL = getopt.getopt(sys.argv[1:],'i:',[])

optH = mybasic.parseParam(optL)

inputDirN=optH['-i']

inputFileNL = os.listdir(inputDirN)
	
inputFileNL = filter(lambda x: re.match('.*\.bedgraph', x),inputFileNL)

print len(inputFileNL)

for inputFileN in inputFileNL:
	
	sampN=re.match('(.*)\.bedgraph', inputFileN).group(1)

	print sampN

	
		



