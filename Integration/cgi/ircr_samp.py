#!/usr/bin/python

import cgi, MySQLdb, sys

def db_conn():
    #connect
    db = MySQLdb.connect(host="localhost", user="cancer", passwd="cancer", db=dbN)
    db.autocommit = True

    #cursor
    cursor = db.cursor()
    return cursor

#get fusiton data from db
def get_fusion_data(sId) :

    cursor = db_conn()
    cursor.execute("select * from splice_fusion where samp_id = '%s' and nPos > 1 order by nPos desc" % sId)
    results = cursor.fetchall()

    return results

#get mutation data from db
def get_mutation_data(sId):

    cursor = db_conn()
    cursor.execute("select * from mutation where samp_id = '%s'" % sId)
    results = cursor.fetchall()

    return results

#get skip info from db
def get_skip_data(sId):

    cursor = db_conn()
    cursor.execute("select * from splice_skip where nPos > 1 and samp_id = '%s'" %sId)

    results = cursor.fetchall()

    return results

def get_del_data(sId):

    cursor = db_conn()
    cursor.execute("select * from splice_eiJunc where samp_id = '%s'" %sId)

    results = cursor.fetchall()

    return results


def print_table(fusion_content, mutation_content, skip_content, del_content):

    fusion_index = ["loc1", "loc2", "gene_sym1", "gene_sym2", "ftype", "exon1", "exon2", "frame", "nPos"]
    mutation_index = ["chrom", "chrSta", "chrEnd", "ref", "alt", "nReads_ref", "nReads_alt", "strand", "gene_sym", "ch_dna", "ch_aa", "ch_type", "cosmic", "mutsig"]
    skip_index = ["loc1", "loc2", "gene_sym", "frame", "delExons", "exon1", "exon2", "nReads", "nPos"]
    eiJunc_index = ["loc", "gene_sym", "juncInfo", "juncAlias", "nReads"]

    print '<b> Sample ID : %s ' % fusion_content[0][0]

    #print row0 - Fusion tableName
    print '''
        <br>Fusion Table : <a class="expand_f" href="#">Expand</a> | <a class="collapse_f" href="#">Collapse</a><br>
        <table border="1" cellpadding="0" cellspacing="0" id = "Fusion">
        <thead>
            <th colspan=9 align=left> Fusion </th>'''

    #print row1 - header
    print '<tr>'
    for index in fusion_index:
        print '<td nowrap> %s </td>' %index
    print '</tr></thead><tbody>'

    #print row2 - data
    for i in range(len(fusion_content)) :
        row = fusion_content[i]
        print '<tr>'
        for j in range(len(row)) :
            j += 1
            if not j == len(row) :
                print '<td> %s </td>' %row[j]
        print '</tr>'

    print '</tbody></table>'

    print '<hr />'

    #print row0 - Mutation tableName
    print '''
        <br>Mutation Table : <a class="expand_m" href="#">Expand</a> | <a class="collapse_m" href="#">Collapse</a><br>
        <table border="1" cellpadding="0" cellspacing="0" id = "Mutation">
        <thead>
            <th colspan=9 align=left> Mutation </th>'''

    #print row1 - header
    print '<tr>'
    for index in mutation_index:
        print '<td nowrap> %s </td>' %index
    print '</tr></thead><tbody>'

    #print row2 - data
    for i in range(len(mutation_content)):
        row = mutation_content[i]
        print '<tr>'
        for j in range(len(row)):
            j += 1
            if not j == len(row):
                print '<td> %s </td>' %row[j]
        print '</tr>'

    print '</tbody></table>'

    print '<hr />'

    #print row0 - Skip tableName
    print '''
        <br>Skip Table : <a class="expand_s" href="#">Expand</a> | <a class="collapse_s" href="#">Collapse</a><br>
        <table border="1" cellpadding="0" cellspacing="0" id = "Skip">
        <thead>
            <th colspan=9 align=left> Skip </th>'''

    #print row1 - header
    print '<tr>'
    for index in skip_index:
        print '<td nowrap> %s </td>' %index
    print '</tr></thead><tbody>'

    #print row2 - data
    for i in range(len(skip_content)):
        row = skip_content[i]
        print '<tr>'
        for j in range(len(row)):
            j += 1
            if not j == len(row):
                print '<td> %s </td>' %row[j]
        print '</tr>'

    print '</tbody></table>'

    #print row0 - eiJunc tableName
    print '''
        <br>3p deletion Table : <a class="expand_d" href="#">Expand</a> | <a class="collapse_d" href="#">Collapse</a><br>
        <table border="1" cellpadding="0" cellspacing="0" id = "Del">
        <thead>
            <th colspan=9 align=left> 3p Deletion </th>'''

    #print row1 - header
    print '<tr>'
    for index in eiJunc_index:
        print '<td nowrap> %s </td>' %index
    print '</tr></thead><tbody>'

    #print row2 - data
    for i in range(len(del_content)):
        row = del_content[i]
        print '<tr>'
        for j in range(len(row)):
            j += 1
            if not j == len(row):
                print '<td> %s </td>' %row[j]
        print '</tr>'

    print '</tbody></table>'

    return

link = cgi.FieldStorage()
if link.has_key("dbN") :
    dbN = link.getvalue("dbN")
else :
    dbN = "ircr1"

if link.has_key("sId") :
    sId = link.getvalue("sId")
else :
    sId = "S780"

print "Content-type: text/html\r\n\r\n";

print '''
<!DOCTYPE HTML>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<title>Sample Detail Page</title>
<script type="text/javascript" src="http://code.jquery.com/jquery-1.5.2.js"></script>
<script type="text/javascript">
$(document).ready(function () {
        $(".expand_m").click(function () {
            $("#Mutation tbody").show("slow");
        });
        $(".collapse_m").click(function () {
            $("#Mutation tbody").hide("fast");
        });
        $(".expand_f").click(function () {
            $("#Fusion tbody").show("slow");
        });
        $(".collapse_f").click(function () {
            $("#Fusion tbody").hide("fast");
        });
        $(".expand_s").click(function () {
            $("#Skip tbody").show("slow");
        });
        $(".collapse_s").click(function () {
            $("#Skip tbody").hide("fast");
        });
        $(".expand_d").click(function () {
            $("#Del tbody").show("slow");
        });
        $(".collapse_d").click(function () {
            $("#Del tbody").hide("fast");
        });
    });

</script>
</head>

<body>
'''

fusion_content = get_fusion_data(sId)
mutation_content = get_mutation_data(sId)
skip_content = get_skip_data(sId)
del_content = get_del_data(sId)
print_table(fusion_content, mutation_content, skip_content, del_content)

print('''
</body>
</html>''')



