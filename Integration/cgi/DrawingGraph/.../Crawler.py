#crawler
#!/usr/bin/python
import MySQLdb

class Crawler:

    sample_list = {}

    #constructor
    #1.set dbN, geneN, item_list
    #2. crawl samples from db
    def __init__(self, dbN, geneN, item_list=[]):
        self.dbN = dbN
        self.geneN = geneN
        self.item_list = item_list
        self.crawlingData_id()

    #db connector
    def connect_db(self):
        #connect
        db = MySQLdb.connect(host="localhost", user="cancer", passwd="cancer", db="%s" % self.dbN)
        db.autocommit = True

        #cursor
        cursor = db.cursor()

        return cursor

    #crawling samples' id
    #1. crawl data
    #2. add to sample_list dic
    def crawlingData_id(self):
        cursor = self.connect_db()

        cursor.execute('create temporary table samples as \
            select distinct samp_id from array_gene_expr union select distinct samp_id from array_cn union select distinct samp_id from splice_normal union select distinct samp_id from mutation')

        cursor.execute('select samp_id from samples order by samp_id')

        samples = {}
        samples = cursor.fetchall()

        i = 0
        for i in range(len(samples)):
            sample_str= str(samples[i])
            sample_id = sample_str[sample_str.find("('")+2:sample_str.find("')")-2]

            self.sample_list[sample_id] = {}

        return

    #crawling tag data
    #input_param : tag_item_list (to query)
    #1. loop
    #   query execute and fetch data
    #2. add fetched data to sample_list dic
    def crawlingData_tag(self, tag_item_list):
        cursor = self.connect_db()

        for item in tag_item_list:
            for sId in self.sample_list:
                cursor.execute('SELECT samp_id, tag FROM sample_tag where samp_id = "%s" and tag like "%s"' % (sId, item))
                data = []
                data = cursor.fetchall()

                for(samp_id, tag) in data:
                    self.sample_list[samp_id][item] = tag

        return

    #crawling Rsq data
    #1. prep RNA-Seq temp table
    #2. loop
    #   query execute to get t_avail from tmp table
    #3. add data to sample_list dic
    def crawlingData_Rsq(self):
        cursor = self.connect_db()

        cursor.execute('create temporary table t_avail_RNASeq as select distinct samp_id from splice_normal')

        for sId in self.sample_list:
            cursor.execute('select samp_id from t_avail_RNASeq where samp_id = "%s"' % sId)
            data = []
            data = cursor.fetchall()

            for samp_id in data:
                self.sample_list[sId]["Rsq"] = "R"

        return

    #crawling CN data
    #1. fetch data from array_cn table
    #   switch if the query has a condition
    #2. add data to sample_list dic
    def crawlingData_CN(self, geneN, condition_cn_list, cnd_cnt):
        cursor = self.connect_db()
        data = []

        #1
        if len(condition_cn_list) > 0:
            cursor.execute('select samp_id, value_log2 from array_cn where gene_sym = "%s" and value_log2 %s' % (geneN, condition_cn_list[cnd_cnt]))
            data = cursor.fetchall()

            for (samp_id, value_log2) in data:
                #cond_str -> condition substring to add the dic
                #cond_str = str(condition_cn_list[cnd_cnt])
                #cond_str = cond_str[cond_str.find("value_log")+10:]
                #2
                self.sample_list[samp_id]["CN "+condition_cn_list[cnd_cnt]] = "%4.1f" %value_log2

            #1
        else :
            cursor.execute('select samp_id, value_log2 from array_cn where gene_sym = "%s"' % (geneN))
            data = cursor.fetchall()
            for (samp_id, value_log2) in data:
                #2
                self.sample_list[samp_id]["CN all"] = "%4.1f" %value_log2

        return

    #crawling mutation data
    #1. fetch data from mutation table
    #2. add data to the sample_list dic
    def crawlingData_mutation(self, geneN, mutation_item_list):
        cursor = self.connect_db()
        data = []

        for item in mutation_item_list:
            cursor.execute('select samp_id, ch_aa, nReads_alt from mutation where gene_sym="%s" and ch_aa = "%s"' %(geneN, item))
            data = cursor.fetchall()

            for (samp_id, ch_aa, nReads_alt) in data:
                self.sample_list[samp_id]["MUT " + ch_aa] = nReads_alt

        return

    #crawling splice_skip data
    #1. fetch data from splice_skip table
    #2. add data to the sample_list dic
    def crawlingData_skip(self, geneN, condition_skip_list, cnd_cnt):
        cursor = self.connect_db()
        data = []

        cursor.execute('select samp_id, delExons, nReads from splice_skip where gene_sym = "%s" and delExons like %s ' % (geneN, condition_skip_list[cnd_cnt]))
        data = cursor.fetchall()
        for (samp_id, delExons, nReads) in data:
            self.sample_list[samp_id]["SKIP " + condition_skip_list[cnd_cnt]] = nReads

        print self.sample_list
        return

    #crawling splice_eiJunc (del) data
    #1. fetch data from splice_eiJunc table
    #2. add data to the sample_list dic
    def crawlingData_del(self, geneN, condition_del_list, cnd_cnt):
        cursor = self.connect_db()
        data = []

        cursor.execute('select samp_id, juncAlias, nReads from splice_eiJunc where gene_sym="%s" and nReads>10 and juncAlias %s group by samp_id' % (geneN, condition_del_list[cnd_cnt]))
        data = cursor.fetchall()

        for (samp_id, juncAlias, nReads) in data:
            self.sample_list[samp_id]["DEL " + condition_del_list[cnd_cnt]] = nReads

        return

    #crawling expr data
    #1. fetch data from array_gene_expr table
    #2. add data to the sample_list dic
    def crawlingData_expr(self, geneN, condition_expr_list, cnd_cnt):
        cursor = self.connect_db()
        data = []

        if len(condition_expr_list) > 0:
            cursor.execute('select samp_id, z_score from array_gene_expr where gene_sym ="%s" and z_score %s' %(geneN, condition_expr_list[cnd_cnt]))

            data = cursor.fetchall()
            for (samp_id, z_score) in data:
                self.sample_list[samp_id]["expr" + condition_expr_list[cnd_cnt]] = "%4.1f" %z_score
        else :
            cursor.execute('select samp_id, z_score from array_gene_expr where gene_sym = "%s" and z_score is not null' % (geneN))

            data = cursor.fetchall()
            for (samp_id, z_score) in data:
                self.sample_list[samp_id]["expr all"] = "%4.1f" %z_score

        return


    def get_sample_list(self):

        return self.sample_list
