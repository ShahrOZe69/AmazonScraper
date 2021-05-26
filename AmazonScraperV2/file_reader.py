import xlrd
import pandas as pd
def read_from_xls(filename):	 
	wb = xlrd.open_workbook(filename)
	sheet = wb.sheet_by_index(0)
	data=[]
	for i in range(sheet.nrows):
		row_dat=[]
		for j in range(sheet.cols):
			row_dat.append(sheet.cell_value(i,j))
		data.append(row_dat)	
	return data
def read_from_xlsx(filename):
	dfs = pd.read_excel(filename)
	return dfs