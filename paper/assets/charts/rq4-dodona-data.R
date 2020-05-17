library(ggplot2)

data <- read.csv2("/home/pieter/Documenten/thesis/evaluation/dodona/performance.csv", header = TRUE, sep = ",")
data <- subset(data, Alpha > -1 & Alpha < 80)
data$idx = seq(1:length(data$commit))

summary(data)
