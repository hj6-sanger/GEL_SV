# =============================================================================
# Methods: Density plot
# Last Modified: 15/01/24
# =============================================================================
#plotting distributions of de novo SVs with respect to genomic properties and computing p vlaue using Monte-Carlo simulation.

getMonteCarloSimulations <- function(nrds.RT.2, column, size) {
	random.idx <- sort(sample(1:nrow(nrds.RT.2), size, replace=T))
	
	return(median(nrds.RT.2[random.idx, column]))
}

plotDensityWilcox <- function(reals, randoms, file.name, col, main.text, xlab.text, showMedian=F, max=2) {
	  ylab.text <- "Density"
	  pval <- testU(reals, randoms)
	
	  d <- density(reals)
	  xlim <- c(min(reals), max(reals))
	  if (!is.na(max))
		    xlim <- c(min(-max), max(max))
	  
	  pdf(file.name, height=6, width=6)
	  par(mar=c(5.1, 4.7, 4.1, 1.4))
	  plot(d, xlab=xlab.text, ylab=ylab.text, main=main.text, xlim=xlim, col=col, cex.axis=1.7, cex.lab=1.8, cex.main=1.9)
	
	  if (showMedian) {
		    abline(v=median(randoms), col="black", lty=5, lwd=3)
		    abline(v=median(reals), col=col, lty=5, lwd=3)
	  }
	
	  text(0, (max(d$y) + min(d$y))/2, getPvalueSignificanceLevel(pval), col="black", cex=5)
	  dev.off()
}

getMonteCarloSimulations <- function(nrds.RT.2, column, size) {
	  random.idx <- sort(sample(1:nrow(nrds.RT.2), size, replace=T))
	
	  return(median(nrds.RT.2[random.idx, column]))
}

plotDensityMonteCarlo2 <- function(reals, nrds.RT.2, column, file.name, col, main.text, xlab.text, ylab.text, showMedian=F, max=NA, rev=F) {
	  reals <- reals[!is.na(reals)]
	  nrds.RT.2.nona <- nrds.RT.2[!is.na(nrds.RT.2$VALUE),]
	  randoms <- replicate(1000, getMonteCarloSimulations(nrds.RT.2.nona, column, length(reals)))
	
	  ranks <- c(randoms, median(reals))
	  pval <- sum(ranks >= median(reals)) / length(ranks)
	  if (median(reals) < median(randoms))
		    pval <- sum(ranks <= median(reals)) / length(ranks)
	
	  d <- density(reals)
	  xlim <- c(0, 1)
	  if (rev)
		     xlim <- rev(xlim)
	  #xlim <- c(0.2, 0.7)   ## GC contents
	  pdf(file.name, height=4, width=4)
	  par(mar=c(5.1, 4.7, 4.1, 1.4))
	  plot(d, xlab=xlab.text, ylab=ylab.text, main=main.text, xlim=xlim, col=col, cex.axis=1.7, cex.lab=1.8, cex.main=1.9)
	
	  text((xlim[1] + xlim[2])/2, (max(d$y) + min(d$y))/2, getPvalueSignificanceLevel(pval), col="black", cex=5)
	  dev.off()
}

scale_values <- function(x){(x-min(x))/(max(x)-min(x))}

plotDensityMonteCarlo <- function(reals, vs, column, file.name, col, main.text, xlab.text, ylab.text, showMedian=F, max=NA, rev=F) {
	  reals <- reals[!is.na(reals)]
	  vs.nona <- vs[!is.na(vs$VALUE),]
	  randoms <- replicate(1000, getMonteCarloSimulations(vs.nona, column, length(reals)))
	
	  ranks <- c(randoms, median(reals))
	  pval <- sum(ranks >= median(reals)) / length(ranks)
	  if (median(reals) < median(randoms))
	  	  pval <- sum(ranks <= median(reals)) / length(ranks)
	  
	  d <- density(reals)
	  xlim <- c(min(reals), max(reals))
	  if (!is.na(max))
	  	  xlim <- c(min(-max), max(max))
	  if (rev)
	  	  xlim <- rev(xlim)
	  #xlim <- c(0.2, 0.7)   ## GC contents
	  
	  #reals.2 <- scale(rank(reals), center=F)
	  reals.2 <- scale(reals, center=F)
	  reals.2 <- scale_values(reals.2)
	  median_normalized <- median(reals.2)
	  median_shift_normalized <- median_normalized - 0.5  # Assuming a uniform distribution has a median of 0.5
	  col.idx <- ceiling(median_shift_normalized/0.05)
	  if (median_shift_normalized < 0)
	  	  col.idx <- floor(median_shift_normalized/0.05)
	  #if (median(reals) < median(randoms))
	  #	  col.idx <- col.idx * -1
	  if (rev)
	  	  col.idx <- col.idx * -1
	  
	  pdf(file.name, height=4, width=4)
	  par(mar=c(5.1, 4.7, 4.1, 1.4))
	  plot(d, xlab=xlab.text, ylab=ylab.text, main=main.text, xlim=xlim, col=col, cex.axis=1.7, cex.lab=1.8, cex.main=1.9)
	
	  if (col.idx > 0)
	  	  polygon(d,	col=reds[col.idx])
	  else 
	     polygon(d,	col=blues[col.idx])
	  
	  text((xlim[1] + xlim[2])/2, (max(d$y) + min(d$y))/2, getPvalueSignificanceLevel(pval), col="black", cex=5)
	  #text((xlim[1] + xlim[2])/2, (max(d$y) + min(d$y))/2, median_shift_normalized, col="black", cex=1)
	  dev.off()
}
