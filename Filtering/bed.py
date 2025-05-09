import sys

'''
This script was called by "filtering.py".
This script filters out SVs with a length < 50.
This script filters out SVs with imprecise breakpoints and rescues such SVs flagged as 'ColocalizedCanva'.
'''

f=open(sys.argv[1])
g=open('2_' + sys.argv[1],'w')

fline = f.readline()
while fline :
	fline = fline.strip()
	if not fline.startswith('#') :
		fso = fline.split('\t')
		lens1= float(fso[4]) - float(fso[2])

		if lens1 >= 50 :
			if 'IMPRECISE' not in fline :
					g.write(fline + '\n')
			else :
				if 'ColocalizedCanvas' in fline :
					g.write(fline + '\n')
	fline = f.readline()
f.close()
g.close()


