fn <- function(values, title) {
  labels <- c("Failed", "Passed")
  labels <- paste(labels, " (", values, ")", sep="")
  pie(values, labels=labels, main=title, col=c("#ffb3ba", "#baffc9"), init.angle = 0)
} 

# Display both pie charts side by side.
par(mfcol=c(1, 2))
waterfall <- fn(c(4558279, 24323724), "Durieux et al")
agile <- fn(c(225766, 2114920-225766), "TravisTorrent")