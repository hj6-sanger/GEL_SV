# Analysis of de novo SVs in Genomics England

Welcome to this site for GEL-SV This site will serve as a source code repository for analyzing GEL-SV data. 

1. "/Analysis/" contains scripts for analyzing age with dnSVs, phasing analysis, timing of triplications from maternal origin, and genomic properties.

2. "/Filtering/" contains scripts for filtering out SVs.


# Running a script for SV classification

1. "Classification" contains a command-line executable script for classifying complex SVs. The current naive script can classify Loss-Loss, Inv-Loss, Loss-Inv-Loss, Loss-invDup, DUP-TRP/INV-DUP, and Dispersed Dup.
 
 
 
 * Example
 ```
samtools_home = /cluster/data/scratch/share/samtools-0.1.19
bwa_home = /cluster/data/scratch/share/bwa-0.6.2
blast_home = /cluster/bio/bin



