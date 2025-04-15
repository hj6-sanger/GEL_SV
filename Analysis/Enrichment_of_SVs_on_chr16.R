# =============================================================================
# Library      : Genomic Properties
# Name         : handbook-of/GenomicProperty.R
# Author       : Tsun-Po Yang (ty2@sanger.ac.uk)
# Last Modified: 26/03/25; 02/11/23
# =============================================================================

# -----------------------------------------------------------------------------
# Methods: To annotate genomic loci based on their chromosomal position. Specifically, it assigns chromosome arms ("p" or "q") and computes distances to the centromere and telomere for a given genomic coordinate.
# Last Modified: 02/11/23
# -----------------------------------------------------------------------------
getArm <- function(chr, START) {
	  centromeres <- subset(cytoBand, gieStain == "acen")
	  colnames(centromeres)[1:3] <- c("CHR", "START", "END")
	  centromeres.chr <- subset(centromeres, CHR == chr)
	  centro <- centromeres.chr[1,]$END
	
	  if (START > centro) {
		    return("q")
	  } else {
		    return("p")
	  }
}

getTelo <- function(CHR, START, Arm) {
	  chromInfo.chr <- subset(chromInfo, chrom == CHR)
	
	  if (Arm == "q") {
		    return(chromInfo.chr$size - START)
	  } else {
		    return(START)
	  }
}

getCentro <- function(chr, START, Arm) {
	  centromeres.chr <- subset(centromeres, CHR == chr)
	  centro <- centromeres.chr[1,]$END
	
	  if (Arm == "q") {
		    return(START - centro)
	  } else {
		    return(centro - START )
	  }
}

# -----------------------------------------------------------------------------
# Comparing the frequency and distribution of structural variant (SV) deletions between chromosome 16 and other chromosomes across different histological subtypes
# Last Modified: 04/10/23
# -----------------------------------------------------------------------------
getCounts <- function(sv.del.nona.chr16, sv.del.nona.others, histology) {
	  colnames <- names(table(c(sv.del.nona.chr16[, histology], sv.del.nona.others[, histology])))
	
	  size.1 <- toTable(0, length(colnames), 2, colnames)
	  rownames(size.1) <- c("Others", "Chr16")
	
	  gel.del.m <- sv.del.nona.others
	  size.1[1, ] <- table(gel.del.m[, histology])[colnames]
	  gel.del.m <- sv.del.nona.chr16
	  size.1[2, ] <- table(gel.del.m[, histology])[colnames]
	  size.1 <- as.data.frame(t(size.1))
	  
	  idx <- as.numeric(as.vector(which(is.na(size.1[,1]))))
	  size.1$Others[idx] <- 0
	  idx <- as.numeric(as.vector(which(is.na(size.1[,2]))))
	  size.1$Chr16[idx] <- 0
	  
	  size.1 <- size.1[order(size.1[,2]),]
	  return(as.matrix(size.1))
}

getProportions <- function(size.1) {
	  size.2 <- size.1
	  size.2[,1] <- size.2[,1] / sum(size.2[,1]) * 100
	  size.2[,2] <- size.2[,2] / sum(size.2[,2]) * 100
	  
	  return(size.2)
}

plotProportions <- function(file.name, main.text, xlab.text, ylab.text, labels, counts, counts.prop, outs=c(36), outs.col=c(red), height=6.1, cutoff=20) {
	  grays <- c("lightgray", "darkgray", "dimgray")
	  #grays <- c("dimgray", "darkgray", "lightgray")
	  cols <- grays[rep_len(1:3, nrow(counts))]
	
	  blues <- c(blue, blue.light)
	  idx <- as.numeric(which(counts.prop[,2] == 0))
	  cols[idx] <- blues[rep_len(1:2, length(idx))]
	  
	  if (length(outs) != 0) {
	  	  for (o in 1:length(outs))
	  	  	  cols[outs[o]] <- outs.col[o]
	  }
	  
	  par(xpd=T)
	  pdf(paste0(file.name, ".pdf"), height=height, width=6.8)
	  par(mar=c(5.1, 4.6, 4.2, 18), xpd=TRUE)
	  barplot(counts.prop, col=cols, ylim=c(0, 100), ylab=ylab.text, xaxt="n", main=main.text, cex.names=1.8, cex.axis=1.8, cex.lab=1.9, cex.main=2)
	  #text(labels=c("Others ", "Chr16 "), x=c(0.8, 2), y=par("usr")[3] - 4, srt=45, adj=0.965, xpd=NA, cex=1.8)
	  axis(side=1, at=1-0.3,     labels=labels[1], font=1, cex.axis=1.9)
	  axis(side=1, at=2-0.3/2/2, labels=labels[2], font=1, cex.axis=1.9)
	  axis(side=1, at=1-0.3,     labels=paste0("n=", sum(counts[,1])), line=1.8, cex.axis=1.9, col.ticks="white")
	  axis(side=1, at=2-0.3/2/2, labels=paste0("n=", sum(counts[,2])), line=1.8, cex.axis=1.9, col.ticks="white")
	
	  idx <- as.numeric(which(counts[,2] >= cutoff))
	  for (c in 1:ncol(counts))
	  	  #text(c - 0.3/c/c, counts.prop[1, c]/2, counts[1, c], cex=1.8)
		    for (r in 1:nrow(counts))
		    	  if (r %in% idx)
		    	  	  if (counts[r, c] > 0)
			   	        text(c - 0.3/c/c, sum(counts.prop[r-1:r, c]) + (counts.prop[r, c]/2), counts[r, c], cex=1.8)
	
	  #text(4.3, 86, expression(italic('P')~"                   "), cex=2)
	  #text(4.3, 86, paste0("   = ", scientific(fisher.test(counts)[[1]])), cex=2)
	  legend("right", c(rev(rownames(counts.prop)[idx]), paste0("Not in ", labels[2])), text.col="black", pch=15, col=c(rev(cols[idx]), blue), pt.cex=3, cex=1.9, horiz=F, bty="n", inset=c(-1.6, 0))
	  dev.off()
}


# =============================================================================
# Manuscript   : Enrichment of maternal dnSVs at subtelometric, early-replicating regions of chromosome 16
# Author       : Tsun-Po Yang (ty2@sanger.ac.uk)
# =============================================================================
#wd.src <- "/nfs/users/nfs_t/ty2/dev/R"           ## @nfs
wd.src <- "/Users/ty2/Work/dev/R"                 ## @localhost

wd.src.lib <- file.path(wd.src, "handbook-of")    ## Required handbooks/libraries for this manuscript
handbooks  <- c("GenomicProperty.R")
invisible(sapply(handbooks, function(x) source(file.path(wd.src.lib, x))))

wd.src.ref <- file.path(wd.src, "guide-to-the")   ## The Bioinformatician's Guide to the Genome
load(file.path(wd.src.ref, "hg38.RData"))

# -----------------------------------------------------------------------------
# Set up working directory
# Last Modified: 02/11/23
# -----------------------------------------------------------------------------
#wd <- "/lustre/scratch127/casm/team294rr/ty2"   ## @lustre
wd <- "/Users/ty2/Work/sanger/ty2"               ## @localhost
BASE <- "GEL"
base <- tolower(BASE)

wd.anlys  <- file.path(wd, BASE, "analysis")
wd.rt <- file.path(wd.anlys, "properties", paste0(base, "-sv-del"))
wd.rt.data  <- file.path(wd.rt, "data")
wd.rt.plots <- file.path(wd.rt, "plots", "Pratto")

wd.nr3  <- file.path(wd, "../../dev/nr3/data/genome_properties")
wd.icgc.data  <- file.path(wd, "ICGC", "metadata")

# -----------------------------------------------------------------------------
# Distance to telomere
# Last Modified: 30/11/23; 04/07/23
# -----------------------------------------------------------------------------
#cytoBand <- readTable(file.path(wd.rt.data, "cytoBand.txt"), header=F, rownames=F, sep="\t")
centromeres <- subset(cytoBand, gieStain == "acen")
colnames(centromeres)[1:3] <- c("CHR", "START", "END")

gel.del.nona <- gel.del.1.2
gel.del.nona$Arm    <- NA
gel.del.nona$Telo   <- NA
gel.del.nona$Centro <- NA
gel.del.nona$Arm    <- mapply(x = 1:nrow(gel.del.nona), function(x) getArm(gel.del.nona$CHR[x], gel.del.nona$START[x]))
gel.del.nona$Telo   <- mapply(x = 1:nrow(gel.del.nona), function(x) getTelo(gel.del.nona$CHR[x], gel.del.nona$START[x], gel.del.nona$Arm[x]))
gel.del.nona$Centro <- mapply(x = 1:nrow(gel.del.nona), function(x) getCentro(gel.del.nona$CHR[x], gel.del.nona$START[x], gel.del.nona$Arm[x]))

# -----------------------------------------------------------------------------
# Stripchart (black)
# Last Modified: 26/09/23
# -----------------------------------------------------------------------------
#gel.del.nona$GROUP0 <- NA
gel.del.nona$GROUP <- NA
gel.del.nona$GROUP2 <- NA
for (g in 1:30) {
	  #gel.del.nona.group <- subset(subset(gel.del.nona, Dist >= (g-1) * 5000000), Dist < g * 5000000)
	  #if (nrow(gel.del.nona.group) != 0)
	  #   gel.del.nona[rownames(gel.del.nona.group),]$GROUP0 <- g
	
	  gel.del.nona.group <- subset(subset(gel.del.nona, Telo >= (g-1) * 5000000), Telo < g * 5000000)
	  if (nrow(gel.del.nona.group) != 0)
		    gel.del.nona[rownames(gel.del.nona.group),]$GROUP <- g
	
	  gel.del.nona.group <- subset(subset(gel.del.nona, Centro >= (g-1) * 5000000), Centro < g * 5000000)
	  if (nrow(gel.del.nona.group) != 0)
		    gel.del.nona[rownames(gel.del.nona.group),]$GROUP2 <- g
}
#gel.del.nona$GROUP0  <- gel.del.nona$GROUP0*5
gel.del.nona$GROUP  <- gel.del.nona$GROUP*5
gel.del.nona$GROUP2 <- gel.del.nona$GROUP2*5

save(gel, gel.del, gel.del.1, gel.del.2, gel.del.1.2, gel.del.nona, file=file.path(wd.rt.data, paste0("exported_SVs_hg38_gel.del.1.2_mechanism_Telo.RData")))

# -----------------------------------------------------------------------------
# Enrichment plot (Telo; Two-side)
# Last Modified: 12/01/24
# -----------------------------------------------------------------------------
gel.del.nona.chr16.mother <- subset(gel.del.nona, V21 == "mother")
gel.mother.p <- as.data.frame(table(subset(gel.del.nona.chr16.mother, Arm == "p")$GROUP))
gel.mother.p$Freq <- gel.mother.p$Freq/2
gel.mother.p$Var1 <- as.numeric(as.vector(gel.mother.p$Var1))
#gel.mother.p$Var1 <- gel.mother.p$Var1 * -1

gel.mother.q <- as.data.frame(table(subset(gel.del.nona.chr16.mother, Arm == "q")$GROUP))
gel.mother.q$Freq <- gel.mother.q$Freq/2
gel.mother.q$Var1 <- as.numeric(as.vector(gel.mother.q$Var1))

total.mother <- sum(gel.mother.p$Freq) + sum(gel.mother.q$Freq)
gel.mother.p$Freq <- gel.mother.p$Freq / total.mother * 100
gel.mother.q$Freq <- gel.mother.q$Freq / total.mother * 100

##
gel.del.nona.chr16.father <- subset(gel.del.nona, V21 == "father")
gel.father.p <- as.data.frame(table(subset(gel.del.nona.chr16.father, Arm == "p")$GROUP))
gel.father.p$Freq <- gel.father.p$Freq/2
gel.father.p$Var1 <- as.numeric(as.vector(gel.father.p$Var1))
#gel.father.p$Var1 <- gel.father.p$Var1 * -1

gel.father.q <- as.data.frame(table(subset(gel.del.nona.chr16.father, Arm == "q")$GROUP))
gel.father.q$Freq <- gel.father.q$Freq/2
gel.father.q$Var1 <- as.numeric(as.vector(gel.father.q$Var1))

total.father <- sum(gel.father.p$Freq) + sum(gel.father.q$Freq)
gel.father.p$Freq <- gel.father.p$Freq / total.father * 100
gel.father.q$Freq <- gel.father.q$Freq / total.father * 100

## Plot p-arm
file.name <- file.path(wd.rt.plots, paste0("DNS_Telomere_Telo_5_P_parm.pdf"))
main.text <- c("", "")
#xlab.text <- "Distance to telomeres [Mb]"
xlab.text <- "p arm"
ylab.text <- "Frequency [%]"
cols <- c("black", "gray", "black")
legends <- c("Mother", "Father", "Total")
max(c(gel.mother.p$Freq, gel.mother.q$Freq, gel.father.p$Freq, gel.father.q$Freq))
ylim <- c(0, 9)

pdf(file.name, height=5, width=4)
par(mar=c(5.1, 4.6, 4.1, 1.5))
plot(NULL, xlim=c(5, 105), ylim=ylim, bty="n", xaxt="n", yaxt="n", xlab=xlab.text, ylab=ylab.text, main=main.text, col="white", pch=19, cex.axis=1.9, cex.lab=2, cex.main=2.1)

points(gel.father.p$Freq ~ gel.father.p$Var1, col=cols[2], pch=19, cex=2.5)
lines(y=gel.father.p$Freq, x=gel.father.p$Var1, col=cols[2], lty=1, lwd=2.5)	
points(gel.mother.p$Freq ~ gel.mother.p$Var1, col=cols[1], pch=19, cex=2.5)
lines(y=gel.mother.p$Freq, x=gel.mother.p$Var1, col=cols[1], lty=1, lwd=2.5)	

axis(side=1, at=5, labels=5, cex.axis=1.9)
axis(side=1, at=seq(5, 105, by=25), labels=c(5,"",50,"",100), cex.axis=1.9)
axis(side=2, cex.axis=1.9)
#axis(side=1, at=120, labels=120, cex.axis=1.9)
#axis(side=1, at=seq(25,150, by=25), labels=c("",50,"",100,"",150), cex.axis=1.9)
#legend("topright", legend=legends[1:2], col=cols[1:2], lty=1, lwd=5, pt.cex=2, cex=1.9)
#legend("topright", legend=legends[1:2], col=cols[1:2], pch=19, lty=1, lwd=5, pt.cex=2, cex=1.9, bty="n")
dev.off()

## Plot q-arm
file.name <- file.path(wd.rt.plots, paste0("DNS_Telomere_Telo_5_Q_qarm.pdf"))
main.text <- c("", "")
#xlab.text <- "Distance to telomeres [Mb]"
xlab.text <- "q arm [Mb]"
ylab.text <- ""
cols <- c("black", "gray", "black")
legends <- c("Mother", "Father", "Total")
max(c(gel.mother.p$Freq, gel.mother.q$Freq, gel.father.p$Freq, gel.father.q$Freq))
ylim <- c(0, 9)

pdf(file.name, height=5, width=5)
par(mar=c(5.1, 1.5, 4.1, 4.6))
plot(NULL, xlim=c(150, 5), ylim=ylim, bty="n", xaxt="n", yaxt="n", xlab=xlab.text, ylab=ylab.text, main=main.text, col="white", pch=19, cex.axis=1.9, cex.lab=2, cex.main=2.1)

points( gel.father.q$Freq ~  gel.father.q$Var1, col=cols[2], pch=19, cex=2.5)
lines(y=gel.father.q$Freq, x=gel.father.q$Var1, col=cols[2], lty=1, lwd=2.5)	
points( gel.mother.q$Freq ~  gel.mother.q$Var1, col=cols[1], pch=19, cex=2.5)
lines(y=gel.mother.q$Freq, x=gel.mother.q$Var1, col=cols[1], lty=1, lwd=2.5)	

#axis(side=1, at=5, labels=5, cex.axis=1.9)
#axis(side=1, at=120, labels=120, cex.axis=1.9)
axis(side=1, at=seq(150, 0, by=-25), labels=c(150,"",100,"",50,"",5), cex.axis=1.9)
axis(side=4, cex.axis=1.9)
#legend("topright", legend=legends[1:2], col=cols[1:2], lty=1, lwd=5, pt.cex=2, cex=1.9, bty="n")
legend("topleft", legend=legends[1:2], col=cols[1:2], pch=19, lty=1, lwd=5, pt.cex=2, cex=2, bty="n")
dev.off()

# -----------------------------------------------------------------------------
# Enriched on chr16
# Last Modified: 09/02/24; 14/11/23; 02/10/23; 16/08/23
# -----------------------------------------------------------------------------
gel.del.nona.mother.bp <- subset(subset(gel.del.nona, Telo <= 15000000), V21 == "mother")
gel.del.nona.mother <- gel.del.nona.mother.bp[0,]
events <- unique(gel.del.nona.mother.bp$event_id)
for (e in 1:length(events)) {
	  del <- subset(gel.del.nona.mother.bp, event_id == events[e])
	  gel.del.nona.mother <- rbind(gel.del.nona.mother, del[1,])
}

gel.del.nona.mother.chr16  <- subset(gel.del.nona.mother, CHR == "chr16")
gel.del.nona.mother.others <- subset(gel.del.nona.mother, CHR != "chr16")

counts <- getCounts(gel.del.nona.mother.chr16, gel.del.nona.mother.others, "V13")
counts.prop <- getProportions(counts)
#writeTable(counts, file.path(wd.rt.plots, "PCAWG_CHR16_Non-FS_ALL.txt"), colnames=T, rownames=T, sep="\t")
counts <- counts[c(1:10,12,11,13),]
counts.prop <- counts.prop[c(1:10,12,11,13),]
rownames(counts) <- c("Dysmorphic", "Growth", "Haematological", "Hearing", "Metabolic", "Ophthalmological", "Skeletal", "Cardiovascular", "Endocrine", "Renal and urinary", "Ultra-rare disorders", "Tumour syndromes", "Neurodevelopmental")
rownames(counts.prop) <- c("Dysmorphic", "Growth", "Haematological", "Hearing", "Metabolic", "Ophthalmological", "Skeletal", "Cardiovascular", "Endocrine", "Renal and urinary", "Ultra-rare disorders", "Tumour syndromes", "Neurodevelopmental")

file.name <- file.path(wd.rt.plots, "GEL_MOTHER_CHR16_75+15")
main.text <- c("Disorders", "")
xlab.text <- ""
ylab.text <- "Proportion [%]"
labels <- c("Others", "Chr16")
plotProportions(file.name, main.text, xlab.text, ylab.text, labels, counts, counts.prop, outs=c(11, 12, 13), outs.col=c(orange, red, "darkgray"), cutoff=1, height=6.1)

