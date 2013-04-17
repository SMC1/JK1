#Json converter
#!/usr/bin/python
import json, MySQLdb, cgi, os

sample_list = {}

item_list = []
tag_item_list = []
mutation_item_list =[]
skip_item_list = []
deletion_item_list = []
others_item_list = []

condition_expr_list = []
condition_cn_list = []

tag_index = ['inv_%', 'pair_%', 'panel_screening', 'RNA-Seq', 'tum_%', 'Xseq_%']
## seperate CN & expr for filtering function?
mutation_index = []
skip_index = []
deletion_index =[]

##list[sid] = { 'cn', 'mu', ..... }

def crawlingData_tag():

    #module2 - crawling data
    for item in tag_item_list:
        for sId in sample_list:
            cursor.execute('SELECT samp_id, tag FROM sample_tag where samp_id = "%s" and tag like "%s"' % (sId, item))
            data = []
            data = cursor.fetchall()

            for(samp_id, tag) in data:
                sample_list[samp_id][item] = tag

    return

def crawlingData_Rsq():

    # prep RNA-Seq data availability table
    # run when the input item is 'Rsq'
    cursor.execute('create temporary table t_avail_RNASeq as select distinct samp_id from splice_normal')

    for sId in sample_list:
        cursor.execute('select samp_id from t_avail_RNASeq where samp_id = "%s"' % sId)
        data = []
        data = cursor.fetchall()

        for samp_id in data:
            sample_list[sId]["Rsq"] = "R"

    return

def crawlingData_CN(geneN, cn_cnt):
        # get cn from array_cn table

    for sId in sample_list:
        data = []
        if len(condition_cn_list) is not 0:
            cursor.execute('select samp_id, value_log2 from array_cn where gene_sym = "%s" and samp_id = "%s"%s' % (geneN, sId, condition_cn_list[cn_cnt]))
            data = cursor.fetchall()
        else :
            cursor.execute('select samp_id, value_log2 from array_cn where gene_sym = "%s" and samp_id = "%s"' % (geneN, sId))

        for (samp_id, value_log2) in data:
            sample_list[samp_id]["CN"] = "%4.1f" %value_log2

    print sample_list
    return

def crawlingData_mutation():

    return

def crawlingData_id():

    #module1 - sample id crawling
    cursor.execute('create temporary table samples as \
        select distinct samp_id from array_gene_expr union select distinct samp_id from array_cn union select distinct samp_id from splice_normal union select distinct samp_id from mutation')

    cursor.execute('select samp_id from samples order by samp_id')

    samples = {}
    samples = cursor.fetchall()


    i = 0
    for i in range(len(samples)):
        sample_str= str(samples[i])
        sample_id = sample_str[sample_str.find("('")+2:sample_str.find("')")-2]

        sample_list[sample_id] = {}

    return sample_list


def calculate_percentage():

    return

########################################################################################################################
def writing_txt():

    text_file = open("output.txt", "w")

    text_file.write("Sample:" + " ")

    for sId in sample_list.keys():
        text_file.write(sId + " ")

    for item in item_list:
        text_file.writelines("\n")
        text_file.write("%s:" %item + " ")

        for sId, value in sample_list.iteritems():
            if item in value.keys():
                text_file.write(value[item] + " ")
            else:
                text_file.write('' + " ")

    text_file.close()

    return

def writing_json():

    ##open txt file
    text_file = open("output.txt", "r")

    ##read each lines
    lines = []
    for line in text_file.readlines():
        lines.append(line)

    ##prepare samples_id to gene_data_dic
    samples_dic = {}
    samples_tmp = str(lines[0])
    samples_prep = samples_tmp[samples_tmp.find('Sample: ')+8:samples_tmp.find("\n")-1]
    id_list = samples_prep.split(" ")
    i = 0
    for sId in id_list :
        samples_dic[sId] = i
        i += 1

    ##add index values into index_dic
    index_dic = {}

    ##prepare each_item_data into
    null_list = []
    for i in range(len(id_list)):
        null_list.append("")

    each_item_data_list = []

    for i in range(len(lines)-1):
        #skip the first line - samples' id
        i += 1
        item_tmp = str(lines[i])
        item_name = item_tmp[:item_tmp.find(":")-1]
        index_dic[item_name] = i-1
        item_prep = item_tmp[item_tmp.find(":")+2:item_tmp.find("\n")-1]
        data_list = item_prep.split(" ")

        each_item_data_dic = {"percent_altered":'00', "rppa":[], "mutations":[], "mrna":[], "cna":[], "hugo":'indexName'}
        each_item_data_dic["hugo"] = item_name
        each_item_data_dic["mutations"] = data_list

        each_item_data_dic["rppa"] = null_list
        each_item_data_dic["mrna"] = null_list
        each_item_data_dic["cna"] = null_list

        each_item_data_list.append(each_item_data_dic)


    #merge
    total_data_dic = {"hugo_to_gene_index":'', "gene_data":'', "samples":''}
    total_data_dic["hugo_to_gene_index"] = index_dic
    total_data_dic["gene_data"] = each_item_data_list
    total_data_dic["samples"] = samples_dic

    gene_json = open("gene_data.json", "w")
    json.dump(total_data_dic, gene_json)

    text_file.close()
    gene_json.close()

    return

def parsing_input(items):

    item_list = items.split(',')

    for item in item_list:
        if item in tag_index:
            tag_item_list.append(item)
        elif item in mutation_index:
            mutation_item_list.append(item)
        elif item in deletion_index:
            deletion_item_list.append(item)
        elif item in skip_index:
            skip_item_list.append(item)
        elif "CN" in item :
            item_substr = item[item.find("CN ")+3:]
            cond = "and value_log2 " + item_substr
            condition_cn_list.append(cond)
        elif "expr" in item :
            item_substr = item[item.find("expr ")+4:]
            cond = "where" + item_substr
            condition_expr_list.append(item_substr)

    return item_list

########################################################################################################################

link = cgi.FieldStorage()
if link.has_key("geneN") :
    geneN = link.getvalue("geneN")
else :
    geneN = "EGFR"

if link.has_key("dbN") :
    dbN = link.getvalue("dbN")
else :
    dbN = "ircr1"

if link.has_key("items") :
    sId = link.getvalue("items")
else :
    items = "Xseq_%,inv_%,Rsq,CN >1.5"

#connectfffffef
db = MySQLdb.connect(host="localhost", user="cancer", passwd="cancer", db=dbN)
db.autocommit = True

#cursor
cursor = db.cursor()

print "Content-type: text/html\r\n\r\n";

print '''
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
    <html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
    <title>converting Json</title>
    </head>

    <body>

    <form method='get'>
    <select name='dbN'>
    <option value ='ircr1' name='dbN' %s>IRCR GBM</option>
    <option value ='tcga1' name='dbN' %s>TCGA GBM</option>
    </select>
    <input type='text' name='geneN' value='%s'>
    <input type='text' name='items' value='%s'>
    <input type='submit' value='Submit'>
    </form>

    ''' % (('selected' if dbN=='ircr1' else ''), ('selected' if dbN=='tcga1' else ''), geneN, items)

print'''
</body>
</html>'''

########################################################################################################################
##  Run
item_list = parsing_input(items)
crawlingData_id()
crawlingData_tag()
crawlingData_Rsq()
crawlingData_CN(geneN, 0)
#writing_txt()
#calculate_percentage()
#writing_json()

#command = "sed -e 's/\"\"/null/g' -i gene_data.json"
#os.system(command)

