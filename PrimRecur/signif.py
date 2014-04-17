#!/usr/bin/python

import sys
import mymysql

colH = {
	'skip': {'tbl':'splice_skip_AF', 'locus':('concat(loc1,"~",loc2)'), 'anchor':'loc1', 'info':('gene_sym','frame','delExons','exon1','exon2'), 'data':('nReads','nReads_w1'), 'data_n':('NULL','NULL')}, \
	'fusion': {'tbl':'splice_fusion_AF', 'locus':('concat(loc1,"~",loc2)'), 'anchor':'loc1','info':('gene_sym1','gene_sym2','frame','ftype','exon1','exon2'), 'data':('nReads','nReads_w1'), 'data_n':('NULL','NULL')}, \
	'eiJunc': {'tbl':'splice_eiJunc_AF', 'locus':('loc'), 'anchor':'loc', 'info':('gene_sym','juncInfo','juncAlias','isLastExon'), 'data':('nReads','nReads_w'), 'data_n':('NULL','NULL')}, \
	'mutation_xsq': {'tbl':'mutation', 'locus':('concat(chrom,":",chrSta,"~",chrEnd,ref,">",alt)'), 'anchor':'concat(chrom,":",chrSta,"~",chrEnd,ref)', 'info':('ref','alt','strand','gene_symL','ch_dna','ch_aa','ch_type','cosmic','mutsig'), 'data':('nReads_alt','nReads_ref'), 'data_n':('NULL','NULL')}, \
	'mutation_rsq': {'tbl':'mutation_rsq', 'locus':('concat(chrom,":",chrSta,"~",chrEnd,ref,">",alt)'), 'anchor':'concat(chrom,":",chrSta,"~",chrEnd,ref)', 'info':('ref','alt','strand','gene_symL','ch_dna','ch_aa','ch_type','cosmic','mutsig'), 'data':('r_nReads_alt','r_nReads_ref'), 'data_n':('NULL','NULL')}, \
	'mutation_normal': {'tbl':'mutation_normal', 'locus':('concat(chrom,":",chrSta,"~",chrEnd,ref,">",alt)'), 'anchor':'concat(chrom,":",chrSta,"~",chrEnd,ref)', 'info':('ref','alt','strand','gene_symL','ch_dna','ch_aa','ch_type','cosmic','mutsig'), 'data':('nReads_alt','nReads_ref'), 'data_n':('n_nReads_alt','n_nReads_ref')}, \
	}

def main(outDirName,dType):

	(con,cursor) = mymysql.connectDB(db='ircr1')
	cH = colH[dType]

	if dType == 'mutation' or dType == 'mutation_normal':
		postFix = '_pre'
	else:
		postFix = ''

	outFile = open('%s/signif_%s%s.txt' % (outDirName,dType,postFix),'w')
	outFile.write('dType\tsId_pair\tlocus\t%s\tp_mt\tp_wt\tr_mt\tr_wt\tn_mt\tn_wt\n' % ('\t'.join(cH['info'])))

	cursor.execute('select distinct samp_id from sample_tag where substring(tag,1,6)="pair_R"')
	sIdL_p = [x for (x,) in cursor.fetchall()]

	for sId_p in sIdL_p:

		cursor.execute('select samp_id from sample_tag where tag="pair_P:%s"' % sId_p)
		sIdL_r = [x for (x,) in cursor.fetchall()]
		if sId_p == 'S633_2':
			sIdL_r = ['S750']
		for sId_r in sIdL_r:

			cursor.execute('select 1 from %s where samp_id="%s" limit 1' % (cH['tbl'],sId_p))
			if len(cursor.fetchall())==0:
				continue

			cursor.execute('select 1 from %s where samp_id="%s" limit 1' % (cH['tbl'],sId_r))
			if len(cursor.fetchall())==0:
				continue

			print '\t%s-%s' % (sId_p,sId_r)

			cursor.execute('create temporary table tK \
				select %s locus,%s loc1,%s from %s where samp_id="%s" union \
				select %s locus,%s loc1,%s from %s where samp_id="%s"' % (cH['locus'],cH['anchor'],','.join(cH['info']),cH['tbl'],sId_p, cH['locus'],cH['anchor'],','.join(cH['info']),cH['tbl'],sId_r))
			cursor.execute('alter table tK add index (locus)')

			cursor.execute('create temporary table tP select %s locus, %s p_mt, %s p_wt from %s where samp_id="%s"' % (cH['locus'],cH['data'][0],cH['data'][1],cH['tbl'],sId_p))
			cursor.execute('alter table tP add index (locus)')

			cursor.execute('create temporary table tR select %s locus, %s r_mt, %s r_wt from %s where samp_id="%s"' % (cH['locus'],cH['data'][0],cH['data'][1],cH['tbl'],sId_r))
			cursor.execute('alter table tR add index (locus)')

			cursor.execute('create temporary table tN select distinct %s locus, %s n_mt, %s n_wt from %s where samp_id="%s" or samp_id="%s"' % (cH['locus'], cH['data_n'][0], cH['data_n'][1], cH['tbl'], sId_p,sId_r))
			cursor.execute('alter table tN add index (locus)')

			cursor.execute('create temporary table tC select tK.locus, loc1, %s, p_mt, p_wt, r_mt, r_wt, n_mt, n_wt \
				from tK left join tP using (locus) left join tR using (locus) left join tN using (locus)' % (','.join(cH['info'])))
			cursor.execute('alter table tC add index (loc1,p_mt)')

			if dType in ['fusion','skip','eiJunc']:

				cursor.execute('create temporary table tA_p select * from splice_normal_loc1 where samp_id="%s"' % sId_p)
				cursor.execute('alter table tA_p add primary key (loc1)')
				cursor.execute('update tC, tA_p set tC.p_wt=tA_p.nReads_w1 where tC.p_mt is null and tC.loc1=tA_p.loc1')

				cursor.execute('create temporary table tA_r select * from splice_normal_loc1 where samp_id="%s"' % sId_r)
				cursor.execute('alter table tA_r add primary key (loc1)')
				cursor.execute('update tC, tA_r set tC.r_wt=tA_r.nReads_w1 where tC.r_mt is null and tC.loc1=tA_r.loc1')

			cursor.execute('select locus, %s, \
				if(p_mt is null,0,p_mt) p_mt, if(p_wt is null,0,p_wt) p_wt,\
				if(r_mt is null,0,r_mt) r_mt, if(r_wt is null,0,r_wt) r_wt, \
				if(n_mt is null,0,n_mt) n_mt, if(n_wt is null,0,n_wt) n_wt \
				from tC order by p_mt desc' % (','.join(cH['info'])))
			results = cursor.fetchall()

			for tokL in results:
				outFile.write('%s\t%s-%s\t%s\n' % (dType, sId_p, sId_r, '\t'.join(map(str,tokL))))

			cursor.execute('drop table tK')
			cursor.execute('drop table tP')
			cursor.execute('drop table tR')
			cursor.execute('drop table tN')
			cursor.execute('drop table if exists tA_p')
			cursor.execute('drop table if exists tA_r')
			cursor.execute('drop table tC')
		#for sId_r

	outFile.close()
	con.close()

#dTypeL = ['fusion']
#dTypeL = ['mutation_rsq']
#dTypeL = ['skip','fusion','eiJunc','mutation_xsq','mutation_rsq', 'mutation_normal']
dTypeL = ['mutation_rsq','mutation_normal']

for dType in dTypeL:
	print dType
#	main('/EQL3/pipeline/somatic_mutect',dType)
#	main('/EQL1/PrimRecur/signif_20140107',dType)
#	main('/EQL1/PrimRecur/signif_20140121',dType)
#	main('/EQL1/PrimRecur/signif_20140204',dType)
#	main('/EQL1/PrimRecur/signif_20140214',dType)
#	main('/EQL1/PrimRecur/signif_20140224',dType)
	main('/EQL1/PrimRecur/signif_20140304',dType)
