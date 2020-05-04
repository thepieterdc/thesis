library(ggplot2)

data <- read.csv2("/home/pieter/Documenten/thesis/evaluation/sel2/performance.csv", header = TRUE, sep = ",")

data <- subset(data, Alpha > -1)
data$idx = seq(1:length(data$commit))

summary(data)
