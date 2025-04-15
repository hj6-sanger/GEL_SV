'''
SV calling and filtering
This script extracted SVs in bedpe format from vcf files using vcfToBedpe.
"check.py" script was used to extract manta calls (not canvas calls in vcf). 

'''

import sys
import os
f=open(sys.argv[1])

fline = f.readline()
while fline :
        fline = fline.strip()
        fso = fline.split('\t')
        proband = fso[4].split('/')
        name = proband[len(proband)-1]
        path = fso[4] + '/Variations/' + name + '.SV.vcf.gz'
        os.system('zcat ' + path + ' | python check.py ' + fso[0] + '_proband')

        os.system('/re_gecip/population_genomics/hjung/manta-tmp/svtools/vcfToBedpe -i ' + fso[0] + '_proband_manta.txt -o ' + fso[0] + '_proband.bed')


        proband = fso[5].split('/')
        name = proband[len(proband)-1]
        path = fso[5] +  '/Variations/' + name + '.SV.vcf.gz'

        os.system('zcat ' + path + ' | python check.py ' + fso[0] + '_father')
        os.system('/re_gecip/population_genomics/hjung/manta-tmp/svtools/vcfToBedpe -i ' + fso[0] + '_father_manta.txt -o ' + fso[0] + '_father.bed')


        proband = fso[6].split('/')
        name = proband[len(proband)-1]
        path = fso[6] +  '/Variations/' + name + '.SV.vcf.gz'
        os.system('zcat ' + path + ' | python check.py ' + fso[0] + '_mother')
        os.system('/re_gecip/population_genomics/hjung/manta-tmp/svtools/vcfToBedpe -i ' + fso[0] + '_mother_manta.txt -o ' + fso[0] + '_mother.bed')


        os.system('python bed.py ' + fso[0] + '_mother.bed')
        os.system('python bed.py ' + fso[0] + '_father.bed')
        os.system('python bed.py ' + fso[0] + '_proband.bed')

        os.system('bsub -q short -P re_gecip_population_genomics -n 1 -o log.txt -e err.txt -R"select[mem>200000] rusage[mem=200000] span[hosts=1]" -M200000 "bedtools pairtopair -is -slop 10 -a 2_' + fso[0] + '_proband.bed -b 2_' + fso[0] + '_father.bed > ' + fso[0] + '.father.intersect"')

        os.system('bsub -q short -P re_gecip_population_genomics -n 1 -o log.txt -e err.txt -R"select[mem>200000] rusage[mem=200000] span[hosts=1]" -M200000 "bedtools pairtopair -is -slop 10 -a 2_' + fso[0] + '_proband.bed -b 2_' + fso[0] + '_mother.bed > ' + fso[0] + '.mother.intersect"')

        fline = f.readline()
f.close()

import sys
import os
f=open(sys.argv[1])
fline = f.readline()
while fline :
        fso = fline.split('\t')
        os.system('cat ' + fso[0] + '_xaa '  +  fso[0] + '_xab ' + fso[0]  + '_xac ' + fso[0]  + '_xad ' + fso[0]  + '_xae ' + fso[0]  + '_xaf > ' + fso[0] + '_intersect')
        os.system('python stat.py ' +  fso[0] + '_intersect unique_' + fso[0] + '_proband.bed')

        os.system('bedtools pairtopair -a 2_unique_'+fso[0] + '_proband.bed -b 2_' + fso[0] +'_mother.bed -slop 100 > ' + fso[0] +'_mom_slop100')

        os.system('bedtools pairtopair -a 2_unique_'+fso[0] + '_proband.bed -b 2_' + fso[0] +'_father.bed -slop 100 > ' + fso[0] +'_dad_slop100')
        o=set()

        k=open(fso[0] + '_mom_slop100')
        kline = k.readline()
        while kline :
                kso = kline.split('\t')
                if kso[10] == kso[27] :
                        o.add(kso[0] + '@' + kso[1] + '@' + kso[2])
                kline = k.readline()
        k.close()

        k=open(fso[0] + '_dad_slop100')
        kline = k.readline()
        while kline :
                kso = kline.split('\t')
                if kso[10] == kso[27] :
                        o.add(kso[0] + '@' + kso[1] + '@' + kso[2])
                kline = k.readline()
        k.close()

        k=open('2_unique_'+fso[0] + '_proband.bed')
        g=open('3_unique_'+fso[0] + '_proband.bed','w')

        kline = k.readline()
        while kline :
                kso = kline.split('\t')
                tmp = kso[0] + '@' + kso[1] + '@' + kso[2]
                if tmp not in o :
                        g.write(kline)
                kline = k.readline()
        k.close()
        g.close()
        fline = f.readline()
f.close()
