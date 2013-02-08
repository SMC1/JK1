errorlist=['C484.TCGA-06-0151-01A-01D-1491-08.5','C484.TCGA-06-0648-01A-01D-1492-08.5','C484.TCGA-28-5211-01C-11D-1845-08.2','C484.TCGA-06-0686-01A-01D-1492-08.5','C484.TCGA-06-0747-01A-01D-1492-08.4']
fo=open('errorlist.txt','w')
for i in range(5):
	fo.write('%s\n'%errorlist[i])
fo.close()
