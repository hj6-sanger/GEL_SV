'''
Visualization of SVs using samplot
'''

import sys
import os

k=open(sys.argv[1])
g=open('hg38_4new-clustered-SV.txt','w')
g1=open('hg19_4new-clustered-SV.txt','w')
kline = k.readline()
j=1
while kline :
        kline = kline.strip()
        kso = kline.split('\t')
        f=open('/re_gecip/population_genomics/hjung/metadata/3-FINAL-META-GRCH38.txt')
        f=open('v4-3All-FINAL-META.txt')
        fline = f.readline()
        ids = kso[len(kso)-1]
       
        while fline :
                fline = fline.strip()
                fso = fline.split('\t')
                if fso[1] == ids and fso[0] == 'hg38' :
                        g.write(kline + '\t' + str(j) +  '\n')
                        print (fline)
                        rso = fso[8].split('/')
                        path = fso[8] + '/Assembly/' + rso[5] + '.bam'
                        rso = kso[2].split('_')
                        chro = 'chr' + kso[0]

                      
                        start=int(kso[1])

                        end=int(kso[4])
                        gap = int(round((end-start) * 1))
                  
                        start = start -gap
                        end = end + gap



                        os.system('time samplot plot --coverage_only -o ' + str(j) + '_proband_' + ids + '.pdf -b ' + path + ' -c' + chro  + ' -s ' + str(start) + ' -e ' + str(end))

                   


                        rso = fso[9].split('/')
                        path = fso[9] + '/Assembly/' + rso[5] + '.bam'
                        os.system('time samplot plot --coverage_only -o ' + str(j)+ '_father_' + ids + '.pdf -b ' + path + ' -c' + chro  + ' -s ' + str(start) + ' -e ' + str(end))

                        rso = fso[10].split('/')
                        path = fso[10] + '/Assembly/' + rso[5] + '.bam'
                        os.system('time samplot plot --coverage_only -o ' +str(j) + '_mother_' + ids + '.pdf -b ' + path + ' -c' + chro  + ' -s ' + str(start) + ' -e ' + str(end))

                        j=j+1
                        break
                elif fso[1] == ids and fso[0] == 'hg19' :
                        g1.write(kline + '\n')
                        break
                fline = f.readline()
        f.close()

        kline = k.readline()
f.close()
g.close()
g1.close()




'''
Visualization of SVs using IGV
'''


f=open(sys.argv[1])
fline = f.readline()
a=[]
b=[]
while fline :
        fline = fline.strip()
        fso = fline.split('\t')

        a.append(fso[0] +'@P')
        kso = fso[4].split('/')
        name = kso[len(kso)-1]
        b.append(fso[4] + '/Assembly/' + name + '.bam')
        a.append(fso[0] +'@F')
        kso = fso[5].split('/')
        name = kso[len(kso)-1]
        b.append(fso[5] + '/Assembly/' + name + '.bam')
        a.append(fso[0] +'@M')
        kso = fso[6].split('/')
        name = kso[len(kso)-1]
        b.append(fso[6] + '/Assembly/' + name + '.bam')
        fline = f.readline()
f.close()

dt=dict(zip(a,b))

g=open('IGV.bat','w')
f=open('head.txt')
fline = f.readline()
while fline :
        fline = fline.strip()
        fso = fline.split('\t')
        g.write('new\n')
        g.write('genome hg38\n')
        g.write('snapshotDirectory ./\n')

        ge = dt.get(fso[len(fso)-3] +'@P')
        g.write('load ' + ge + '\n')
        ge = dt.get(fso[len(fso)-3] +'@F')
        g.write('load ' + ge + '\n')
        ge = dt.get(fso[len(fso)-3] +'@M')
        g.write('load ' + ge + '\n')

        start = int(fso[1])-50
        end = int(fso[2]) + 50
        tmp = 'PROBAND_' + fso[0] + '@' + fso[1] + '@' + fso[2]
        g.write('goto ' + fso[0] + ':' + str(start) + '-' + str(end) + '\n')
        g.write('collapse\n')
        g.write('snapshot ' + tmp + '.png\n')
	fline = f.readline()
f.close()
g.close)_
