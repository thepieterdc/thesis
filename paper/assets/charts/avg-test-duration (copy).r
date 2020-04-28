library(dplyr)
library(ggplot2)
library(tibble)

categories <- c("[10-60)", "[60-120)", "[120-300)", "[300-600)", "[600-1800)", "[1800-3600)", "[3600-7200)", "[7200-86400)")

data <- read.csv2("/home/pieter/durations.csv", header = TRUE)

data <- data$duration[data$duration >= 10 & data$duration < 86400]

bins <- mutate(
  category = case_when(
    data >= 10 & data < 60 ~ categories[1],
    data >= 60 & data < 120 ~ categories[2],
    data >= 120 & data < 300 ~ categories[3],
    data >= 300 & data < 600 ~ categories[4],
    data >= 600 & data < 1800 ~ categories[5],
    data >= 1800 & data < 3600 ~ categories[6],
    data >= 3600 & data < 7200 ~ categories[7],
    data >= 7200 & data < 86400 ~ categories[8]
  ),
  xmin = case_when(
    data >= 10 & data < 60 ~ 10,
    data >= 60 & data < 120 ~ 60,
    data >= 120 & data < 300 ~ 120,
    data >= 300 & data < 600 ~ 300,
    data >= 600 & data < 1800 ~ 600,
    data >= 1800 & data < 3600 ~ 1800,
    data >= 3600 & data < 7200 ~ 3600,
    data >= 7200 & data < 86400 ~ 7200,
  ),
  xmax = case_when(
    data >= 10 & data < 60 ~ 60,
    data >= 60 & data < 120 ~ 120,
    data >= 120 & data < 300 ~ 300,
    data >= 300 & data < 600 ~ 600,
    data >= 600 & data < 1800 ~ 1800,
    data >= 1800 & data < 3600 ~ 3600,
    data >= 3600 & data < 7200 ~ 7200,
    data >= 7200 & data < 86400 ~ 86400,
  ),
  as_tibble(data)
)

bins$category <- factor(bins$category, levels=categories, ordered=FALSE)

summary(bins$category)

normalize <- function(min, max, val) {
  (val - min) / (max - min)
}

boxplot(data, horizontal = TRUE)

png("save.png")
ggplot(data = bins, mapping = aes(x=category, y=normalize(xmin, xmax, value))) +
  geom_boxplot(fill="bisque", color="black", alpha=0.3) +
  ggtitle("Execution time of test suites using Travis CI") +
  labs(x='categorised duration', y='normalised duration') +
  guides(color=FALSE) +
  theme_minimal()
