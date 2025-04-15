import sys
import os

'''
This script only extracts manta calls for downstream analysis (not canvas calls in VCF). 
This script was called by "filtering.py".
'''

f=open(sys.argv[1] + '_manta.txt','w')
g1=open(sys.argv[1]+ '_canvas.txt','w')
o=set()
for line in sys.stdin :
	if not line.startswith('#') :
		fso = line.split('\t')
		kso = fso[2].split(':')
		if kso[0].startswith('Manta') :
			g.write(line)
		else :
			g1.write(line)
	else :
		g.write(line)


g.close()
g1.close()
