#!/usr/bin/python3
import sys
import csv
import xlsxwriter

filename = sys.argv[1]
bk = xlsxwriter.Workbook(filename+'_stats.xlsx')
sh = bk.add_worksheet('raw_data')
sh1 = bk.add_worksheet('stats')

graph_iteration = 0
graph_size = 15

with open(filename,'r') as tsvf:
	data = csv.reader(tsvf,delimiter='\t')
	cnt=0
	for row in data:
		col=0
		for i in row:
			sh.write(cnt,col,float(i))
			col+=1
		cnt+=1

def add_chart_vert(name,data_col_str,graph_col_str):
	cnt = graph_iteration
	vst = '=raw_data!$X$1:$X$1000'.replace('X',data_col_str)
	#sh = bk.add_worksheet('stats')
	ch = bk.add_chart({'type': 'line'})
	ch.add_series({
	#  'categories': '=Sheet1!$I$1:$I$1000',
	  'values': vst, 
	  })
	ch.set_title({'name': name})
	ch.set_legend({'position': 'none'})
	ch.set_y_axis({
	'name': 'stp',})
	ch.set_x_axis({'name': 'time'})
	ch.set_size({'width': 512, 'height': 256})
	cst = graph_col_str + str(1+graph_size*cnt)
	sh.insert_chart(cst, ch)
	cnt += 1
	return cnt

def add_labels(sensor):
	row = 15*sensor
	sh.write(13+row,16,"AVE")
	sh.write(13+row,17,"STDEV")
	sh.write(13+row,18,"P-P")
	sh.write(13+row,19,"CFACTOR")

def add_formulas(sensor,col):
	row = 15*sensor
	vst = '=_xlfn.AVERAGE(X1:X1000)'.replace('X',col)
	tmp = str(15+row)
	cst = 'Q'+tmp
	sh.write_formula(cst,vst)
	vst = "=raw_data!"+cst
	cst = 'A'+str(sensor+1)
	sh1.write(cst,vst)

	vst = '=_xlfn.STDEV.S(X1:X1000)'.replace('X',col)
	tmp = 'Q'+str(15+row)
	cst = tmp.replace('Q',chr(ord('Q') + 1))
	sh.write_formula(cst, vst)
	vst = "=raw_data!"+cst
	cst = 'B'+str(sensor+1)
	sh1.write(cst,vst)

	vst = '=MAX(?1:?1000)-MIN(?1:?1000)'.replace('?',col)
	tmp = 'Q'+str(15+row)
	cst = tmp.replace('Q',chr(ord('Q') + 2))
	sh.write_formula(cst, vst)
	vst = "=raw_data!"+cst
	cst = 'C'+str(sensor+1)
	sh1.write(cst,vst)

	vst = '=S'+str(15+row)+'/R'+str(15+row)
	tmp = 'Q'+str(15+row)
	cst = tmp.replace('Q',chr(ord('Q') + 3))
	sh.write_formula(cst, vst)
	vst = "=raw_data!"+cst
	cst = 'D'+str(sensor+1)
	sh1.write(cst,vst)

graph_iteration = add_chart_vert('sensor1','I','Q')
graph_iteration = add_chart_vert('sensor2','J','Q')
graph_iteration = add_chart_vert('sensor3','K','Q')
graph_iteration = add_chart_vert('sensor4','L','Q')
graph_iteration = add_chart_vert('sensor5','M','Q')
graph_iteration = add_chart_vert('sensor6','N','Q')
graph_iteration = add_chart_vert('sensor7','O','Q')

for i in range(7):
	add_labels(i)
	add_formulas(i,chr(ord('I')+i))

bk.close()