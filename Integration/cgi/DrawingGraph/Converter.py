#converter
#!/usr/bin/python
import json, os

class Converter:

	#constructor
	#1. set the sample_list
	#2. set the query item_list
	def __init__(self, sample_list, item_list):
		self.sample_list = sample_list
		self.item_list = item_list

	#writing data to txt file - delimiter is " "
	#1. write sample ids from sample_list
	#2. write result of the queries
	def writing_txt(self):

		text_file = open("output.txt", "w")

		text_file.write("Sample:" + " ")

		#1
		for sId in self.sample_list.keys():
			text_file.write(sId + " ")

		#2
		for item in self.item_list:
			text_file.writelines("\n")
			text_file.write("%s:" %item + " ")

			for sId, value in self.sample_list.iteritems():
				if item in value.keys() or str(value.keys()) in item:
					text_file.write(str(value[item]) + " ")
				else:
					text_file.write('' + " ")

		text_file.close()

		return

	#writing txt file data to json file
	#1. read lines from .txt
	#2. prep samples_dic = {} and read sample_ids from txt file
	#3. add ids to samples_dic
	#4. prep index_dic = {}
	#   null_list = [] for null dics like "rppa", "cna"...,
	#   each_item_data_list = [] to complete the final dic
	#5. loop
	#   parsing item_index from the line
	#   parsing data_list from the line
	#   calculate percentage
	#   prep each_item_data_dic = {} -> actual json format of "gene_data.json"
	#   compose each_item_data_dic -> need to add values to "hugo", "mutations" / others = null_list
	#6. merge all
	#   prep total_data_dic ={}
	#   append index_dic, each_item_data_list, sample_dic
	#   each_item_data_lists -> the num of each_item_data_list should be the same as the num of items
	#7. write to .json
	def writing_json(self):

		text_file = open("output.txt", "r")

		#1
		lines = []
		for line in text_file.readlines():
			lines.append(line)

		#2
		samples_dic = {}
		samples_tmp = str(lines[0])
		samples_prep = samples_tmp[samples_tmp.find('Sample: ')+8:samples_tmp.find("\n")-1]
		id_list = samples_prep.split(" ")

		#3
		i = 0
		for sId in id_list :
			samples_dic[sId] = i
			i += 1

		#4
		index_dic = {}

		null_list = []
		for i in range(len(id_list)):
			null_list.append('')

		each_item_data_list = []

		#5
		for i in range(len(lines)-1):
			#skip the first line - samples' id
			i += 1
			item_tmp = str(lines[i])
			item_name = item_tmp[:item_tmp.find(":")]
			index_dic[item_name] = i-1
			item_prep = item_tmp[item_tmp.find(":")+2:item_tmp.find("\n")-1]
			data_list = item_prep.split(" ")
			data_list.append("")
			total_cnt = 0
			data_cnt = 0

			for data in data_list:
				if len(data) is not 0 :
					data_cnt += 1
				total_cnt += 1

			percentage = 100 * int(data_cnt)/int(total_cnt)

			each_item_data_dic = {"percent_altered":'00', "rppa":[], "mutations":[], "mrna":[], "cna":[], "hugo":'indexName'}
			each_item_data_dic["hugo"] = item_name
			each_item_data_dic["mutations"] = data_list
			each_item_data_dic["percent_altered"] = str(data_cnt) + "(" + str(percentage) + "%)"

			each_item_data_dic["rppa"] = null_list
			each_item_data_dic["mrna"] = null_list
			each_item_data_dic["cna"] = null_list

			each_item_data_list.append(each_item_data_dic)


		#6
		total_data_dic = {"hugo_to_gene_index":'', "gene_data":'', "samples":''}
		total_data_dic["hugo_to_gene_index"] = index_dic
		total_data_dic["gene_data"] = each_item_data_list
		total_data_dic["samples"] = samples_dic

		#7
		gene_json = open("gene_data.json", "w")
		json.dump(total_data_dic, gene_json)

		text_file.close()
		gene_json.close()

		return

	#find and replace .json file
	#1. correct "" to null
	def find_and_replace(self):

		open('/var/www/html/js/gene_data.json','w').write(open('gene_data.json').readline().replace('""','null'))

		return


