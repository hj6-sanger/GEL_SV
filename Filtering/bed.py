import sys

'''
This script was called by "filtering.py".
The imprse

f=open(sys.argv[1])
g=open('2_' + sys.argv[1],'w')

fline = f.readline()
while fline :
	fline = fline.strip()
	if not fline.startswith('#') :
		fso = fline.split('\t')
		lens1= float(fso[2]) - float(fso[1])
		lens2= float(fso[5]) - float(fso[4])

		if lens1 <= 50 or lens2 <=50 :
			g.write(fline + '\n')
		else :
			if 'ColocalizedCanvas' in fline :
				g.write(fline + '\n')
	fline = f.readline()
f.close()
g.close()


