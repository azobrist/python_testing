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

	with open(filename,'r') as csvf:
		data = csv.reader(csvf,delimiter=',')
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
	for ch in range(7):
                vst = '=AVERAGE(sensor{0}!{1}2:{1}201)'.format(ch+1,chr(ord('A')+x))
                cst = chr(ord('A')+ch)+str(1+x)
                sh.write_formula(cst,vst)
                vst = '={2}{0}-{2}{1}'.format(ch+1,ch+2,chr(ord('A')+x))
                cst = '{1}{0}'.format(ch+9,chr(ord('A')+x))
                sh.write_formula(cst,vst)
                vst = '={0}{1}/($I{2}-$I{3})'.format(chr(ord('A')+ch),9+x,2+x,1+x)
                cst = '{0}{1}'.format(chr(ord('A')+ch),17+x)
                sh.write_formula(cst,vst)
                vst = '=_xlfn.STDEV.S(sensor{0}!{1}2:{1}201)'.format(ch+1,chr(ord('A')+x))
                cst = '{0}{1}'.format(chr(ord('A')+ch),25+x)
                sh.write_formula(cst,vst)
    
d = [11.99,15.38,20.7,26.64,34.69,40.63,51.99]
for i in range(len(d)):
	vst = str(d[i])
	cst = 'I'+str(1+i)
	sh.write(cst,vst)
	vst = '=(I{0}/2)^2*PI()'.format(i+1)
	cst = 'J'+str(1+i)
	sh.write_formula(cst,vst)

vst = '=1/(A1*275)'.format(i+1)
cst = 'K1'
sh.write_formula(cst,vst)

bk_compile.close()
