# Analysis of de novo SVs in Genomics England

Welcome to this site for GEL-SV This site will serve as a source code repository for analyzing GEL-SV data. 

1. "/Analysis/" contains scripts for analyzing age with dnSVs, phasing analysis, timing of triplications from maternal origin, and genomic properties.

2. "/Filtering/" contains scripts for filtering out SVs.


# Running a script for SV classification

1. "/Classification" contains a command-line executable script for classifying complex SVs. The current naive script can classify Loss-Loss, Inv-Loss, Loss-Inv-Loss, Loss-invDup, DUP-TRP/INV-DUP, and Dispersed Dup. We aim to publish a method paper on a fully automated SV classification pipeline using a bam file as input.

2. The script takes a bedpe file with clustered SVs as input. 
 
 
 * Example input bedpe (/Classification/Loss-invLoss.bedpe)
 ```
21	22552774	22552776	21	22586470	22586472	MantaINV	1	+	+
21	22579426	22579430	21	22586794	22586798	MantaINV	1	-	-
 ```

3. "/Classification" also contains examples of the input files for this script (e.g., Loss-Loss, Inv-Loss, Loss-Inv-Loss, Loss-invDup, DUP-TRP/INV-DUP, and Dispersed Dup.)


