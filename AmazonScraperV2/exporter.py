import csv
import json
# exporting a tuple variable into the csv file
def export_dic_to_csv(dic):  
	with open('output_data.csv', 'w', newline = '',encoding="utf-8") as csvfile:
		my_writer = csv.writer(csvfile)
		for val in dic.keys():
		
			my_writer.writerow([val]+dic[val])
def export_dic_to_json(dic):
	out_file = open("output_data_json.json", "w")    
	json.dump(dic, out_file) 
	out_file.close() 


"""list argument is list of lists """	
def export_list_to_csv(list_):
	with open('output_data.csv', 'w', newline = '',encoding="utf-8") as csvfile:
		my_writer = csv.writer(csvfile)
		for val in list_:
			my_writer.writerow(val)
def export_list_to_txt(list_,name='output_data.txt'):
	with open(name, 'w', newline = '',encoding="utf-8") as txtfile:
		for L in list_ :
			txtfile.writelines(L+"\n")
