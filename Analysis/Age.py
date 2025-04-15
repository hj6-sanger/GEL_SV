solve=set()

f=open('../solved_ids.tsv')
fline = f.readline()
while fline :
        fso = fline.split('\t')
        solve.add(fso[0])
        fline = f.readline()
f.close()


from scipy import stats
sv=set()

f=open('../Affected-v4-phased_denovo_SV.txt')

fline = f.readline()

while fline :
        fline = fline.strip()
        fso = fline.split('\t')
        sv.add(fso[11])
        fline = f.readline()
f.close()

f=open('../v4-3All-FINAL-META.txt')

fline = f.readline()
a=[]
b=[]
c=[]
d=[]
disease = set()
el= 0
disease.add('Neuro_disorder')
disease.add('Other_disorder')
while fline :
        fline = fline.strip()
        fso = fline.split('\t')

        disease.add(fso[17])

        father = int(fso[11]) - int(fso[13])
        mother = int(fso[11]) - int(fso[15])
       
        if  fso[5].startswith('A') :
              
                a.append(fso[1])
                b.append(father)
                c.append(mother)
                d.append(fso[17])
 
        fline = f.readline()

f.close()

print (el)

dt_f = dict(zip(a,b))
dt_m = dict(zip(a,c))
g=open('propotion.txt','w')
g1=open('all-father-age.txt','w')
g2=open('all-mother-age.txt','w')
g3=open('driver-all-age-boxplot.txt','w')

g3.write('disorder' + '\t'  + 'dnSV' + '\t'+'father_age' + '\t' + 'mother_age' + '\n')
from scipy.stats import mannwhitneyu
import numpy as np

tot_f_a=[]
tot_f_b=[]

tot_m_a=[]
tot_m_b=[]

for gene in disease :
        i=0
        f_aa=[]
        f_bb=[]

        m_aa=[]
        m_bb=[]
        while i <  len(d) :
                if d[i] == gene :
                        name = gene.replace(' ','_')
                        if a[i] in sv :
                                f_aa.append(b[i])
                                tot_f_a.append(b[i])

                                g1.write(name + '\t' + '1' + '\t' + str(b[i]) + '\n')
                                g2.write(name + '\t' + '1' + '\t' + str(c[i]) + '\n')
                                g3.write('All_disorders' + '\t' + 'with_dnSV' + '\t' +  str(b[i]) + '\t' + str(c[i]) + '\n')
                                g3.write(gene + '\t' + 'with_dnSV' + '\t' +  str(b[i]) + '\t' + str(c[i]) + '\n')
                            
                                m_aa.append(c[i])
				tot_m_a.append(c[i])
                        else :
                                f_bb.append(b[i])
                                tot_f_b.append(b[i])

                                g1.write(name + '\t' + '2' + '\t' + str(b[i]) + '\n')
                                g2.write(name + '\t' + '2' + '\t' + str(c[i]) + '\n')
                                g3.write('All_disorders' + '\t' + 'without_dnSV' + '\t' +  str(b[i]) + '\t' + str(c[i]) + '\n')
                                g3.write(gene + '\t' + 'without_dnSV' + '\t' +  str(b[i]) + '\t' + str(c[i]) + '\n')
                               
                                m_bb.append(c[i])
                                tot_m_b.append(c[i])
                i=i+1
        if len(f_aa) > 0  and len(f_bb) > 0 :
                print (gene,len(f_aa),len(f_bb))

                res1=mannwhitneyu(f_aa,f_bb)
                res3=stats.ttest_ind(f_aa,f_bb)
                print (np.mean(f_aa),np.mean(f_bb),np.median(f_aa),np.median(f_bb))
                res2=mannwhitneyu(m_aa,m_bb)
                res4=stats.ttest_ind(m_aa,m_bb)
                print (np.mean(m_aa),np.mean(m_bb),np.median(m_aa),np.median(m_bb))
                print ("\n")

                g.write(gene + '\t' + str(len(f_aa)) + '\t' + str(len(f_bb)) + '\t' + str(res1[1]) + '\t' + str(res2[1]) + '\t' + str(res3[1]) + '\t' + str(res4[1]) +'\n')
g.close()
g1.close()
g2.close()
g3.close()
