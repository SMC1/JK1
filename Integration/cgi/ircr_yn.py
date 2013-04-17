#!/usr/bin/python

import sys, MySQLdb, cgi

conditionL_preH = {
'ircr1': [
    ('"S"', 'sample_tag', 'tag="panel_screening"', '%s','scrn'),
    ('"R"', 't_avail_RNASeq', 'True', '%s','RSq'),
    ('substring(tag,6)', 'sample_tag', 'tag like "XSeq_%"', '%s','XSq'),
    ('substring(tag,6)', 'sample_tag', 'tag like "pair_%"', '%s','pair'),
    ('substring(tag,5)', 'sample_tag', 'tag like "tum_%"', '%s','tum'),
    ('substring(tag,5)', 'sample_tag', 'tag like "inv_%"', '%s','inv'),
    ('z_score', 'array_gene_expr', 'z_score is not NULL', '%4.1f','expr'),
    ('value_log2', 'array_cn', 'True', '%4.1f','CN'),
    ('rpkm', 'rpkm_gene_expr', 'rpkm is not NULL', '%4.1f','RPKM')
],

'tcga1': [
    ('"R"', 't_avail_RNASeq', 'True', '%s','RSq'),
    ('substring(tag,6)', 'sample_tag', 'tag like "XSeq_%"', '%s','XSq'),
    ('z_score', 'array_gene_expr', 'z_score is not NULL', '%4.1f','expr'),
    ('value_log2', 'array_cn', 'True', '%4.1f','CN'),
    ('rpkm', 'rpkm_gene_expr', 'rpkm is not NULL', '%4.1f','RPKM')
],

'ccle1': [
    ('z_score', 'array_gene_expr', 'z_score is not NULL', '%4.1f','expr'),
    ('value_log2', 'array_cn', 'True', '%4.1f','CN')
]

}

conditionL_fusion = [ ('nEvents', 't_fusion', 'frame=True', '%3d', 'in'),
                      ('nEvents', 't_fusion', 'frame=False', '%3d', 'off')]


cutoff = .1

def main(dbN,geneN):

    if dbN == 'ccle1':

        mutation_map = {'DEL:3\'UTR':'UTR', 'SNP:3\'UTR':'UTR', 'SNP:Missense_Mutation':'MS', 'SNP:Intron':'INT', 'DEL:Frame_Shift_Del':'FS', \
                        'SNP:5\'UTR':'UTR', 'DEL:In_Frame_Del':'FP', 'INS:3\'UTR':'UTR', 'SNP:Splice_Site_SNP':'SS', 'SNP:Nonsense_Mutation':'NS', \
                        'INS:Frame_Shift_Ins':'FS', 'DEL:Intron':'INT', 'INS:Intron':'INT', 'DNP:Missense_Mutation':'MS', 'INS:Splice_Site_Ins':'SS', \
                        'TNP:Intron':'INT', 'DNP:Nonsense_Mutation':'NS', 'DNP:Intron':'INT', 'SNP:De_novo_Start_OutOfFrame':'SOF', 'DNP:5\'UTR':'UTR', \
                        'INS:5\'UTR':'UTR', 'SNP:Nonstop_Mutation':'NM', 'DNP:3\'UTR':'UTR', 'SNP:5\'Flank':'FLK', 'DEL:5\'UTR':'UTR', 'DNP:Splice_Site_DNP':'SS', \
                        'INS:In_Frame_Ins':'FP', 'DEL:Splice_Site_Del':'SS', 'SNP:De_novo_Start_InFrame':'SIF', 'DEL:5\'Flank':'FLK', 'INS:5\'Flank':'FLK', \
                        'DNP:De_novo_Start_InFrame':'SIF', 'DNP:Stop_Codon_DNP':'STC', 'INS:Stop_Codon_Ins':'STC', 'TNP:Nonsense_Mutation':'NS', \
                        'TNP:Missense_Mutation':'MS', 'DEL:Start_Codon_Del':'SC'}

    else:

        mutation_map = {'DEL:Frame_Shift_Del':'FS', 'DEL:In_Frame_Del':'FP', 'DEL:Splice_Site':'SS', 'DEL:Translation_Start_Site':'TSS', \
                        'DNP:Missense_Mutation':'MS', 'DNP:Nonsense_Mutation':'NS', 'DNP:Splice_Site':'SS', \
                        'INS:Frame_Shift_Ins':'FS', 'INS:In_Frame_Ins':'FP', 'INS:Splice_Site':'SS', \
                        'SNP:Missense_Mutation':'MS', 'SNP:Nonsense_Mutation':'NS', 'SNP:Nonstop_Mutation':'NM', 'SNP:Splice_Site':'SS', 'SNP:Translation_Start_Site':'TSS', \
                        'Substitution - Missense':'MS', 'Substitution - Nonsense':'NS', 'Substitution - Missense,Substitution - coding silent':'MS', 'Nonstop extension':'rNS'}

    # prep RNA-Seq data availability table
    cursor.execute('create temporary table t_avail_RNASeq as select distinct samp_id from splice_normal')

    # prep exonSkip info
    cursor.execute('select delExons,frame,loc1,loc2, count(*) cnt from splice_skip where gene_sym = "%s" group by delExons order by count(*) desc' % geneN)
    results = cursor.fetchall()

    conditionL_exonSkip = []

    for (delExons,frame,loc1,loc2, cnt) in results:

        if ':Y' in frame:
            frame_code = 'in'
        elif ':N' in frame:
            frame_code = 'off'
        else:
            frame_code = 'utr'

        conditionL_exonSkip.append( [
            ('nReads', 'splice_skip', 'delExons="%s"' % delExons, '%3d', '%s<br><sub>(n=%s, %s)</sub>' % (delExons.split(',')[0], cnt,frame_code),), \
            #			('avg(nReads)', 'splice_normal', 'loc1="%s" or loc2="%s"' % (loc1,loc2), '%d') ])
            ('sum(nReads)', 'splice_normal', 'loc1="%s"' % (loc1,), '%d') ])

    # prep mutation info
    cursor.execute('select ch_dna,ch_aa,ch_type,cosmic,count(*) cnt from mutation where gene_sym="%s" and nReads_alt>2 group by ch_dna order by count(*) desc, cosmic desc limit 20' % geneN)
    results = cursor.fetchall()

    conditionL_mutation = []

    for (ch_dna,ch_aa,ch_type,cosmic,cnt) in results:

        ch_aa = ch_aa.replace(',','<br>')

        if cosmic:
            cosmic_fmt = '<font color="red">%s</font><br><sub>(n=%d, %s)</sub>'

        else:
            cosmic_fmt = '%s<br><sub>(n=%d, %s)</sub>'

        conditionL_mutation.append( [
            ('nReads_alt', 'mutation', 'nReads_alt>2 and ch_dna="%s"' % ch_dna, '%d', cosmic_fmt % (ch_aa if(ch_aa) else ch_dna, cnt, mutation_map[ch_type])), \
            ('nReads_ref', 'mutation', 'nReads_alt>2 and ch_dna="%s"' % ch_dna, '%d') ])

    # prep fusion table
    cursor.execute('create temporary table t_fusion as \
        select samp_id,locate(":Y",frame)>1 frame,count(nPos) nEvents \
        from splice_fusion where (find_in_set("%s",gene_sym1) or find_in_set("%s",gene_sym2)) group by samp_id, locate(":Y",frame)>1' % (geneN,geneN))

    # prep eiJunc info
    cursor.execute('select loc,juncAlias, count(*) cnt from splice_eiJunc where gene_sym="%s" and nReads>10 group by loc' % geneN)
    results = cursor.fetchall()

    conditionL_eiJunc = []

    for (loc,juncAlias,cnt) in results:
        conditionL_eiJunc.append( [
            ('nReads', 'splice_eiJunc', 'loc="%s" and nReads>10' % loc, '%3d', '%s<br><sub>(n=%s)</sub>' % (juncAlias, cnt)),
            ('sum(nReads)', 'splice_normal', 'loc1="%s"' % (loc,), '%d') ])


    conditionL = conditionL_preH[dbN] + conditionL_mutation + conditionL_fusion + conditionL_exonSkip + conditionL_eiJunc

    print '<p>%s status of %s panel</p>' % (geneN,dbT_h[dbN])

    #cursor.execute('create temporary table t_id as \
    #    select distinct samp_id from array_gene_expr union select distinct samp_id from array_cn union select distinct samp_id from splice_normal union select distinct samp_id from mutation')

    #cursor.execute('alter table t_id add index (samp_id)')

    #cursor.execute('select samp_id from t_id left join array_gene_expr using (samp_id) \
    #    where gene_sym="%s" or gene_sym is NULL order by z_score desc' % geneN)

    cursor.execute('create temporary table t_id as \
		select distinct samp_id from array_gene_expr union select distinct samp_id from array_cn union select distinct samp_id from splice_normal union select distinct samp_id from mutation')

    cursor.execute('alter table t_id add index (samp_id)')

    cursor.execute('create temporary table t_expr as select * from array_gene_expr where gene_sym="%s"' % geneN)

    cursor.execute('alter table t_expr add index (samp_id,gene_sym)')

    cursor.execute('select samp_id from t_id left join t_expr using (samp_id) order by z_score desc')

    results = cursor.fetchall()

    numTotSamp = len(results)

    print('\n<table border="1" cellpadding="0" cellspacing="0">')

    # header: row1
    print '<tr>\n<td rowspan=2><div class="verticaltext" align="middle">samples<br><sub>n=%s<sub></div></td>' % numTotSamp,

    for i in range(len(conditionL)):

        row = conditionL[i]

        if type(row) == list:
            row = row[0]

        if i < len(conditionL_preH[dbN]):
            print('<td rowspan=2 align="middle"><div class="verticaltext">%s</div></td>' % row[-1])
        else:
            if i == len(conditionL_preH[dbN]) and len(conditionL_mutation)>0:
                print('<td align="middle" colspan=%s>mutation (mt/wt)</td>' % len(conditionL_mutation))
            elif i == len(conditionL_preH[dbN])+len(conditionL_mutation):
                print('<td align="middle" colspan=%s>fusion</td>' % len(conditionL_fusion))
            elif i == len(conditionL_preH[dbN])+len(conditionL_mutation)+len(conditionL_fusion) and len(conditionL_exonSkip)>0:
                print('<td align="middle" colspan=%s>exonSkip (mt/wt)</td>' % len(conditionL_exonSkip))
            elif i == len(conditionL_preH[dbN])+len(conditionL_mutation)+len(conditionL_fusion)+len(conditionL_exonSkip) and len(conditionL_eiJunc)>0:
                print('<td align="middle" colspan=%s>3p deletion (mt/wt)</td>' % len(conditionL_eiJunc))

    print('\n</tr>\n')

    # header: row2
    print '<tr>\n',

    for i in range(len(conditionL)):

        row = conditionL[i]

        if type(row) == list:
            row = row[0]

        if i < len(conditionL_preH[dbN]):
            pass
        else:
            print('<td height="100"><div class="verticaltext" align="middle">%s</div></td>' % row[-1])

    print('\n</tr>\n')

    for (sId,) in results:

        print '<tr>',
        print '<td nowrap><a href="ircr_samp.py?%s">%s</td>' % (sId, sId),

        d_flag = None
        r_flag = None

        for row in conditionL:

            if type(row) == list:
                row_wt = row[1]
                row = row[0]
            else:
                row_wt = None

            (col,tbl,cnd,fmt) = row[:4]

            cursor.execute('show columns from %s like "gene_sym"' % tbl)

            if cursor.fetchone():
                cnd += ' and gene_sym="%s"' % geneN

            cursor.execute('select %s from %s where samp_id="%s" and %s' % (col,tbl,sId,cnd))

            results2 = cursor.fetchall()

            if len(results2) > 1:
                print sId
                raise Exception

            if type(row)==tuple and row[-1]=='RSq':

                if len(results2) > 0:
                    r_flag = True
                else:
                    r_flag = False

            if type(row)==tuple and row[-1]=='XSq':

                if len(results2) > 0:
                    d_flag = True
                else:
                    d_flag = False

            if len(results2) == 1 and results2[0][0] not in (0,'0'):

                value = ('%s' % fmt) % results2[0][0]

                if row_wt:

                    (col,tbl,cnd,fmt) = row_wt[:4]
                    cursor.execute('select %s from %s where samp_id="%s" and %s' % (col,tbl,sId,cnd))

                    results_wt = cursor.fetchone()

                    if results_wt[0]:
                        count_wt = ('%s' % fmt) % results_wt[0]
                    else:
                        count_wt = 0

                    #here -highlight
                    if int(value) > int(count_wt) * cutoff:
                        if not '28/28' in row[4] :
                            print '<td><font color=red><b>%s</b></font><sub>/%s</sub></td>' % (value, count_wt),
                        else:
                            print '<td>%s<sub>/%s</sub></td>' % (value, count_wt),
                    else:
                        print '<td>%s<sub>/%s</sub></td>' % (value, count_wt),

                else:
                    if row[1] == 't_fusion':
                        if row[4] == 'in':
                            print '<td><a href=ircr_fusion.py?dbN=%s&geneN=%s&sId=%s&flag=in> %s </td>' % (dbN, geneN, sId, value),
                        else :
                            print '<td><a href=ircr_fusion.py?dbN=%s&geneN=%s&sId=%s&flag=off> %s </td>' % (dbN, geneN, sId, value)
                    else :
                        print '<td>%s</td>' % value

            else:
                #grey out
                if (r_flag==False and row[1] in ('splice_skip','t_fusion','splice_eiJunc')) or (d_flag==False and row[1] in ('mutation')):
                    print '<td bgcolor=silver></td>'
                else:
                    print '<td></td>'

        print '</tr>'

    print('\n</table>\n')


dbT_h = {'ircr1':'AVATAR GBM', 'tcga1':'TCGA GBM', 'ccle1':'CCLE'}

form = cgi.FieldStorage()

if form.has_key('geneN'):
    geneN = form.getvalue('geneN')
else:
    geneN = 'EGFR'

if form.has_key('dbN'):
    dbN = form.getvalue('dbN')
else:
    dbN = 'ircr1'

if len(sys.argv) >1:
    dbN = sys.argv[1]

con = MySQLdb.connect(host="localhost", user="cancer", passwd="cancer", db=dbN)

con.autocommit = True
cursor = con.cursor()

print "Content-type: text/html\r\n\r\n";

print '''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<title>%s status of %s panel</title>
<style type="text/css">
.verticaltext{
-webkit-transform:rotate(-90deg); writing-mode:tb-rl; -moz-transform:rotate(90deg); -o-transform: rotate(90deg); white-space:nowrap; display:blocking; padding-left:1px;padding-right:1px;padding-top:10px;padding-bottom:10px;
}
</style>
</head>
<body>

<form method='get'>
<select name='dbN'>
<option value ='ircr1' name='dbN' %s>AVATAR GBM</option>
<option value ='tcga1' name='dbN' %s>TCGA GBM</option>
<option value ='ccle1' name='dbN' %s>CCLE</option>
</select>
<input type='text' name='geneN' value='%s'>
<input type='submit' value='Submit'>
</form>

''' % (geneN,dbT_h[dbN],('selected' if dbN=='ircr1' else ''),('selected' if dbN=='tcga1' else ''),('selected' if dbN=='ccle1' else ''),geneN)

main(dbN,geneN)

print('''
<br>Legends<br>
* "expr": z-normalized <br>
* "CN": in log2 scale <br>
* "mutation": (alt allele count) > 2 <br>
* "mutation": no silent <br>
* red in "mutation": in COSMIC database <br>
* "fusion": nPos > 1 <br>
* "exonSkip": nReads >= 5 <br>
* "3p deletion": nReads > 10 <br>
* red numbers: (mut allele count) > (ref allele count) * 0.1 <br>
</body>
</html>''')

