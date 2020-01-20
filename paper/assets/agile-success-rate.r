fn <- function(values, title) {
  labels <- c("Successful", "Challenged", "Failed")
  labels <- paste(labels, values)
  labels <- paste(labels, "%", sep="")
  pie(values, labels=labels, main=title, col=c("#baffc9", "#ffdfba", "#ffb3ba"))
} 

# Display both pie charts side by side.
par(mfcol=c(1, 2))
waterfall <- fn(c(11, 60, 29), "Waterfall method")
agile <- fn(c(39, 52, 9), "Agile methodologies")