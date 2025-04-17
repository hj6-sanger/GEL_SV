import sys
import operator
f=open(sys.argv[1])

sv1=[]
sv2=[]

fline = f.readline()
fline = fline.strip()
fso = fline.split('\t')

#sv1 array stores the information of SV1
sv1.append(fso[0])
sv1.append(int(fso[1]))
sv1.append(int(fso[4]))
sv1.append(fso[8])
sv1.append(fso[9])

fline = f.readline()
fline = fline.strip()
fso = fline.split('\t')


#sv2 array  stores the information of SV1
sv2.append(fso[0])
sv2.append(int(fso[1]))
sv2.append(int(fso[4]))
sv2.append(fso[8])
sv2.append(fso[9])


sv=[]
sv.append(sv1)
sv.append(sv2)

sorted_sv = sorted(sv, key=operator.itemgetter(1))


#dispersed_dup 
if (sorted_sv[0][3] == '-' and sorted_sv[0][4] == '+') and (sorted_sv[1][3] == '+' and sorted_sv[1][4] == '-') :
	if (sorted_sv[0][1] < sorted_sv[1][1]  < sorted_sv[0][2]) and sorted_sv[0][2] < sorted_sv[1][2] :
		print ("Dispersed_Dup")

#Loss-Loss

if (sorted_sv[0][3] == '+' and sorted_sv[0][4] == '-') and (sorted_sv[1][3] == '+' and sorted_sv[1][4] == '-') :
	if (sorted_sv[0][1] < sorted_sv[1][1]) and (sorted_sv[0][2] < sorted_sv[1][1]) :
		print ("Loss-Loss")

#Dup-Trp/INV-DUP OR DUP-NML-DUP OR Loss-invDUP 
if (sorted_sv[0][3] == '-' and sorted_sv[0][4] == '-') and (sorted_sv[1][3] == '+' and sorted_sv[1][4] == '+') :
	if (sorted_sv[0][1] < sorted_sv[1][1]) and (sorted_sv[0][2] < sorted_sv[1][1]) :
		print ("Dup-Trp/INV-DUP")
	if (sorted_sv[0][1] < sorted_sv[1][1]  < sorted_sv[0][2]) and sorted_sv[0][2] < sorted_sv[1][2] :
		print ("DUP-NML-DUP")
	if (sorted_sv[0][1] < sorted_sv[1][1]  < sorted_sv[0][2]) and (sorted_sv[0][1] < sorted_sv[1][2]  < sorted_sv[0][2]) :
		print ("Loss-invDUP")


#INV-Loss OR Loss-invLoss
if (sorted_sv[0][3] == '+' and sorted_sv[0][4] == '+') and (sorted_sv[1][3] == '-' and sorted_sv[1][4] == '-') :
	if (sorted_sv[0][1] < sorted_sv[1][1]  < sorted_sv[0][2]) and sorted_sv[0][2] < sorted_sv[1][2] :
		diff = abs(sorted_sv[1][1]-sorted_sv[0][1])
		diff2 = abs(sorted_sv[1][2]-sorted_sv[0][2])
		if diff < 50 and diff2 < 50 :
			print ("Reciprocal Inversion")
		elif diff < 50 or diff2 < 50 :
			print ("INV-Loss")
		else :
			print ("Loss-invLoss")

 
		



