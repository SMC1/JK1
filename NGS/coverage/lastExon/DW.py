import sys,os,re,getopt
import mybasic


optL, argL = getopt.getopt(sys.argv[1:],'i:j:',[])

optH = mybasic.parseParam(optL)

inputDirN=optH['-i']
geneN=optH['-j']


inputFileNL = os.listdir(inputDirN)
	
inputFileNL = filter(lambda x : re.match('.*\_%s.txt'%(geneN), x),inputFileNL)

pattern=re.compile('.*?-.*?-.*?-.*?-[0-9]{2}([DW]{1})\S*')

for inputFile in inputFileNL:
	
	if re.match(pattern,inputFile)!=None and re.match(pattern,inputFile).group(1)=='D':
		os.renames('%s/%s'%(inputDirN,inputFile),'%s/%s_D/%s'%(inputDirN,geneN,inputFile))
	elif re.match(pattern,inputFile)!=None and re.match(pattern,inputFile).group(1)=='W':
		os.renames('%s/%s'%(inputDirN,inputFile),'%s/%s_W/%s'%(inputDirN,geneN,inputFile))

