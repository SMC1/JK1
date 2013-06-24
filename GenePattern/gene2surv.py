#!/usr/bin/python_epd

import sys, getopt, numpy, scipy.stats
import mygp, mymath


optL, argL = getopt.getopt(sys.argv[1:],'',['inGctFile=', 'inClinicalFile=', 'geneName=', 'dataName=', 'endPointName=', 'centerMetric=', 'cutoffType=', 'cutoffTop=', 'cutoffBottom='])
optH = mygp.parseParam(optL)

if '--inGctFile' in optH:
    inGctFileName = optH['--inGctFile']
else:
    inGctFileName = '/Users/jinkuk/Data/Rembrandt/Rembrandt_GBM_new.gct'

if '--inClinicalFile' in optH:
    inClinicalFileName = optH['--inClinicalFile']
else:
    inClinicalFileName = '/Users/jinkuk/Data/Rembrandt/clinical.txt'

if '--geneName' in optH:
    geneName = optH['--geneName']
else:
    geneName = 'MET'

if '--dataName' in optH:
    dataName = optH['--dataName']
else:
    dataName = 'Rembrandt'

if '--endPointName' in optH:
    endPointName = optH['--endPointName']
else:
    endPointName = 'death'

if '--centerMetric' in optH:
    centerMetric = optH['--centerMetric']
else:
    centerMetric = 'median'

if '--cutoffType' in optH: # mad, fold, top_percentile 
    cutoffType = optH['--cutoffType']
else:
    cutoffType = 'fold'

if '--cutoffTop' in optH: # cutoff values: multiple of mad/fold in log2 scale OR top_percentile
    cutoffTop= float(optH['--cutoffTop'])
else:
    cutoffTop = 1

if '--cutoffBottom' in optH:
    cutoffBottom = float(optH['--cutoffBottom'])
else:
    cutoffBottom = -1


plat = 'x'

indH = CanGen.loadClinical({},inClinicalFileName)
indH = CanGen.loadGct(indH, [geneName], inGctFileName, plat)

print '\n', len(indH), [(ind.sId,ind.pId) for ind in indH.values()]
indL = filter(lambda x: plat in x.expr and geneName in x.expr[plat], indH.values())
print len(indL), [(ind.sId,ind.pId) for ind in indL]
indL = filter(lambda x: x.censor > -1, indL)
print len(indL)

valueL = [x.expr[plat][geneName] for x in indL]
l = len(valueL)

if centerMetric == 'median':
	center = numpy.median(valueL)
elif centerMetric == 'mean':
	center = numpy.mean(valueL)
else:
	raise Exception

if cutoffType in ('mad','fold'):

	if cutoffType == 'mad':
		multiplier = mymath.mad(valueL)
	else:
		multiplier = 1

	threshold = (center + multiplier*cutoffBottom, center + multiplier*cutoffTop)

else:

	threshold = (scipy.stats.scoreatpercentile(valueL,100-cutoffBottom), scipy.stats.scoreatpercentile(valueL,100-cutoffTop))

print center, threshold

outFile = open('%s_%s__by__%s.mvc' % (dataName,endPointName,geneName),'w')

outFile.write('pId\ttime\tevent\tvalue\tlabel\tpriority\n')

for ind in indL:

	endPoint = getattr(ind,'get'+endPointName[0].upper()+endPointName[1:])()
	followup = ind.censor

	if endPoint > 0:
		event = 1
		time = endPoint
	elif followup > 0:
		event = 0
		time = followup

	if ind.expr[plat][geneName] < threshold[0]:

		if cutoffType != 'top_percentile':
			label = '"%s < 2^%s %s"' % (geneName,cutoffBottom,cutoffType)
		else:
			label = '"%s < %s %s"' % (geneName,cutoffBottom,cutoffType)

		priority = '1'

	elif ind.expr[plat][geneName] >= threshold[1]:

		if cutoffType != 'top_percentile':
			label = '"%s > 2^%s %s"' % (geneName,cutoffTop,cutoffType)
		else:
			label = '"%s > %s %s"' % (geneName,cutoffTop,cutoffType)
			
		priority = '2'

	else:

		label = '"%s mid"' % (geneName,)
		priority = '9'

	outFile.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (ind.pId, time, event, ind.expr[plat][geneName], label, priority))

outFile.close()
