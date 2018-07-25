#!/usr/bin/python3
import sys
import csv
import xlsxwriter

filename = sys.argv[1]
session_name=filename.split('_')[0]
bk_compile = xlsxwriter.Workbook(session_name+'_weighted_vs_csa_+snr.xlsx')
sh_compile = [0]*len(sys.argv)
for i in range(len(sys.argv)):
	sh_compile[i]=bk_compile.add_worksheet('sensor'+str(i+1))

for i in range(len(sys.argv)-1):
	filename=sys.argv[i+1]
	hdr_str=filename.split('_')[1]
	if hdr_str == "12mm":
		num=1
	elif hdr_str == "15mm":
		num=2
	elif hdr_str == "20mm":
		num=3
	elif hdr_str == "26mm":
		num=4
	elif hdr_str == "35mm":
		num=5
	elif hdr_str == "40mm":
		num=6
	elif hdr_str == "50mm":
		num=7

	for i in range(len(sh_compile)):
		sh_compile[i].write(0,num-1,hdr_str)

	with open(filename,'r') as tsvf:
		data = csv.reader(tsvf,delimiter='\t')
		cnt=0
		for row in data:
			col=0
			for i in row:
				if col >= 8 and col < 15:
					#if cnt == 0:
						#sh_compile[col-8].write(cnt,sensor-1,hdr_str)
					sh_compile[col-8].write(cnt+1,num-1,float(i))
				col+=1
			cnt+=1

sh = bk_compile.add_worksheet('Vpp vs Dia')

for x in range(7):
	for i in range(7):
		vst = '=_xlfn.AVERAGE(sensor{0}!X2:X1001)'.format(x+1).replace('X',chr(ord('A')+i))
		cst = chr(ord('A')+i)+str(1+x)
		sh.write_formula(cst,vst)

bk_compile.close()