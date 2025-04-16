'''
This script makes an input for Unfazed tool using Haplotype caller. 
The input for this script is a list of SVs (i.e., genomic coordinates of deletion) with the proband ID.
'''


import os
import sys
k=open(sys.argv[1])
kline = k.readline()
while kline :
        kline = kline.strip()
        f=open('v4-3All-FINAL-META.txt')
        fline = f.readline()
        while fline :
                fline = fline.strip()
                fso = fline.split('\t')
                if fso[1] == kline and fso[0] == 'hg38' :

                        os.system('mkdir ./' + kline)
                        os.system('gatk HaplotypeCaller -R /re_gecip/population_genomics/hjung/genome.fa -I ./'+ fso[1] + '.bam -L ' + fso[1] + '_sv.bed -O ./' +kline + '/' +  fso[1]+'.vcf.gz -ERC GVCF')
                        os.system('gatk HaplotypeCaller -R /re_gecip/population_genomics/hjung/genome.fa -I ./'+ fso[2] + '.bam -L ' + fso[1] + '_sv.bed -O ./'+ kline + '/'  + fso[2]+'.vcf.gz -ERC GVCF')
                        os.system('gatk HaplotypeCaller -R /re_gecip/population_genomics/hjung/genome.fa -I ./'+ fso[3] + '.bam -L ' + fso[1] + '_sv.bed -O ./' + kline + '/' +   fso[3]+'.vcf.gz -ERC GVCF')
                        os.system('gatk CombineGVCFs -R /re_gecip/population_genomics/hjung/genome.fa --variant ./' + kline + '/' +  fso[1]+'.vcf.gz --variant ./' + kline + '/' +  fso[2]+'.vcf.gz --variant ./' + kline + '/' + fso[3] +'.vcf.gz -O ./' + kline + '/' +  fso[1] + 'cohort.vcf.gz')

                        os.system('gatk GenotypeGVCFs -R /re_gecip/population_genomics/hjung/genome.fa -V ./'+ kline + '/'+  fso[1] +'cohort.vcf.gz -O ./' + kline + '/' +  fso[1] +'genotype.vcf.gz')


                        os.system('sambamba view -f bam -h -L '+fso[1]+'_sv.bed ' +  fso[1] +'.bam > target_' + fso[1] + '.bam')
                        os.system('samtools index target_' + fso[1] + '.bam')


                        kso = fso[8].split('/')
                        pro = kso[len(kso)-1]

                        os.system('gunzip ./' + fso[1] +'/' + fso[1] +'genotype.vcf.gz')

                        os.system('bedtools intersect -a ./' + fso[1] + '_sv.bed -b ./' + fso[1] + '/' + fso[1] +'genotype.vcf -wa -wb > ./' + fso[1] + '/intersect.txt')

                       

                       
                        os.system('unfazed -t 4 -s ./'+ kline + '/'  + fso[1] +'genotype.vcf.gz -p ' + fso[1] + '_trio.ped --bam-pairs ' + pro + ':./target_' + fso[1] + '.bam -g 38 -d ' + fso[1] +'_sv.bed --outfile ' + fso[1] + '_unfazed.txt')
                       
                     
                fline = f.readline()
        f.close()

        kline = k.readline()
k.close()
