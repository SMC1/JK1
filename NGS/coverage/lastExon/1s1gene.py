import sys, getopt
import mybasic, mygenome

optL, argL = getopt.getopt(sys.argv[1:],'i:j:',[])

optH = mybasic.parseParam(optL)

if not ('-i' in optH and '-j' in optH):

	print 'Usage: ./1s1gene.py -i [bedgraph file path] -j [refFlat file path]'
	sys.exit(0)

bedgraphFileN = optH['-i']
refFlatFileN=optH['-j']

data={}

filePathPrefix = bedgraphFileN.split('.bedgraph')[0]

bedgraph=open(bedgraphFileN,'r')
refFlat=mygenome.loadRefFlatByChr(refFlatFileN)

temp=0 
for line in bedgraph:
	l=line.split('\t')
	chr_sample=l[0]
	if (chr_sample!='chr7' and temp==1):
		break
	if chr_sample=='chr7' and refFlat.has_key(chr_sample):
		s=int(l[1])
		e=int(l[2])
		d=int(l[3])
		temp=1  
		for gene in refFlat[chr_sample]:
			SeqId=gene['refSeqId']
			if not data.has_key(SeqId):
				data.update({SeqId:{'denominator':0,'nominator':0,'rate':0}})
			if not (e<gene['exnList'][0][0] or s>gene['exnList'][len(gene['exnList'])-1][1]):
				for exon in gene['exnList']:
					length=mygenome.overlap((s,e),(exon[0],exon[1]))
					if length!=0:
						dens=length*d
						data[SeqId]['denominator']+=dens
						if exon==gene['exnList'][len(gene['exnList'])-1]:
							data[SeqId]['nominator']+=dens

fo=open('%s_lastExon.txt'%(filePathPrefix),'w')
for SId in data:
	if data[SId]['denominator']!=0:
		data[SId]['rate']=float(data[SId]['nominator'])/data[SId]['denominator']
		fo.write('%s\t%s\n'%(SId,data[SId]['rate']))
fo.close()



