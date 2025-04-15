import sys

f=open('./3intersect.txt')
g=open('./4intersect.txt','w')
fline = f.readline()
while fline :
        fline = fline.strip()
        fso = fline.split('\t')
        on=1
        if fso[4] == '0/1' and float(fso[5]) < 0.35 :
                on =0
        if fso[6] == '0/1' and float(fso[7]) < 0.35 :
                on=0

        if on == 1 :
                if fso[4] == '0/0' and fso[6] == '1/1' and fso[2] == '0/1' :

                        if float(fso[3]) >=0.66 and float(fso[3]) <=0.8:
                                g.write('mother_both' + '\t' + fline + '\n')
                        elif float(fso[3]) <=0.33 and float(fso[3]) >=0.2:
                                g.write('father' + '\t' + fline + '\n')

                elif fso[4] == '1/1' and fso[6] == '0/0' and fso[2] == '0/1' :

                        if float(fso[3]) <=0.33 and float(fso[3]) >=0.2:
                                g.write('mother_both' + '\t' + fline + '\n')
                        if float(fso[3]) >=0.66 and float(fso[3]) <=0.8:
                                g.write('father' + '\t' + fline + '\n')

                elif fso[4] == '0/0' and (fso[6] == '0/1' and float(fso[7]) >=0.4 and float(fso[7]) <= 0.6)  and fso[2] == '0/1' :
                        if float(fso[3]) <=0.33 and float(fso[3]) >=0.2:
                                g.write('father,mother_meiosis_I' + '\t' + fline + '\n')

                        if float(fso[3]) >=0.66 and float(fso[3]) <=0.8:
                                g.write('mother_meiosis_II' + '\t' + fline + '\n')

                elif (fso[4] == '0/1' and float(fso[5]) >=0.4 and float(fso[5]) <= 0.6) and fso[6] == '0/0' and fso[2] == '0/1' :
                        if float(fso[3]) <=0.33 and float(fso[3]) >=0.2:
                                g.write('mother_both' + '\t' + fline + '\n')
                        if float(fso[3]) >=0.66 and float(fso[3]) <=0.8:
                                g.write('father' + '\t' + fline + '\n')
                elif (fso[4] == '0/1' and float(fso[5]) >=0.4 and float(fso[5]) <= 0.6) and fso[6] == '1/1' and fso[2] == '0/1' :
                        if float(fso[3]) <=0.33 and float(fso[3]) >=0.2:
                                g.write('father' + '\t' + fline + '\n')
                        if float(fso[3]) >=0.66 and float(fso[3]) <=0.8:
                                g.write('mother_both' + '\t' + fline + '\n')
                elif fso[4] == '1/1' and (fso[6] == '0/1' and float(fso[7]) >=0.4 and float(fso[7]) <= 0.6) and fso[2] == '0/1' :
                        if float(fso[3]) <=0.33 and float(fso[3]) >=0.2:
                                g.write('mother_meiosis_II' + '\t' + fline + '\n')
                        if float(fso[3]) >=0.66 and float(fso[3]) <=0.8:
                                g.write('father,mother_meiosis_I' + '\t' + fline + '\n')
        fline = f.readline()
f.close()
