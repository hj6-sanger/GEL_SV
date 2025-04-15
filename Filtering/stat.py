
import sys
f=open(sys.argv[1])
a=[]


fline = f.readline()
while fline :
	fline = fline.strip()
	fso = fline.split('\t')
	name = fso[len(fso)-1]
	if name != fso[15] :
		tmp = fso[0] + '@' + fso[1] + '@' + fso[2] + '@' + fso[3] + '@' + fso[4] + '@' + fso[5]
		a.append(tmp)
	fline = f.readline()
f.close()


import collections

c=collections.Counter(a)

import sys

f=open(sys.argv[2])
g=open('2_' + sys.argv[2],'w')


fline = f.readline()
while fline :
	fline = fline.strip()
	fso = fline.split('\t')
	tmp = fso[0] + '@' + fso[1] + '@' + fso[2] + '@' + fso[3] + '@' + fso[4] + '@' + fso[5]
	g.write(fline + '\t' + str(c[tmp]) + '\n')
	fline = f.readline()
f.close()
g.close()

