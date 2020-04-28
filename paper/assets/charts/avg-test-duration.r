library(dplyr)
library(ggplot2)
library(tibble)

categories <- c("[10-60)", "[60-120)", "[120-300)", "[300-600)", "[600-1800)", "[1800-3600)", "[3600-7200)", "[7200-86400)")

data <- read.csv2("/home/pieter/durations.csv", header = TRUE)

data <- data$duration[data$duration >= 10 & data$duration < 86400]

boxplot(
  data,
  horizontal = TRUE,
  outline = FALSE
)
