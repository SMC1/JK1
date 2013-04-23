#Parser
#!/usr/bin/python

class Parser:

    item_list = []
    tag_item_list = []
    mutation_item_list = []

    condition_skip_list = []
    condition_del_list = []
    condition_cn_list = []
    condition_expr_list = []

    tag_index = ['inv_%', 'pair_%', 'panel_screening', 'RNA-Seq', 'tum_%', 'Xseq_%']

    operator_list = [">", "<", ">=", "<=", "="]

    #parsing the input query
    #1. parse the query
    #2. get each index list using Indexer
    #3. distinguish each item
    #   separate items - conditions
    def parsing_input(self, items, geneN, dbN):

        item_list = items.split(',')

        for item in item_list:

            if item in self.tag_index:
                self.tag_item_list.append(item)

            elif "MUT" in item:
                item_substr = item[item.find("MUT ")+4:]
                self.mutation_item_list.append(item_substr)

            elif "DEL" in item:
                item_substr = item[item.find("DEL ")+4:]

                if any(operator in item_substr for operator in self.operator_list) :
                    self.condition_del_list.append(item_substr)
                else :
                    print "error : no operator"

            elif "SKIP" in item:
                item_substr = item[item.find("SKIP ")+5:]
                self.condition_skip_list.append(item_substr)

            elif "CN" in item :
                item_substr = item[item.find("CN ")+3:]

                if "all" in item_substr:
                    pass
                else :
                    self.condition_cn_list.append(item_substr)

            elif "expr" in item :
                item_substr = item[item.find("expr ")+4:]

                if "all" in item_substr:
                    pass
                else :
                    self.condition_expr_list.append(item_substr)

        return item_list

    #getter - tag_item_list of the input query
    def get_tag_item_list(self):
        return self.tag_item_list

    #getter - mutation_item_list of the input query
    def get_mutation_item_list(self):
        return self.mutation_item_list

    #getter - condition_del_list of the input query
    def get_condition_del_list(self):
        return self.condition_del_list

    #getter - condition_skip_list of the input query
    def get_condition_skip_list(self):
        return self.condition_skip_list

    #getter - condition_cn_list of the input query
    def get_condition_cn_list(self):
        return self.condition_cn_list

    #getter - condition_expr_list of the input query
    def get_condition_expr_list(self):
        return self.condition_expr_list

    #getter - whole item_list of the input query
    def get_item_list(self):
        return self.item_list