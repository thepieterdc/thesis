library(dplyr)
library(ggplot2)
library(tibble)

categories <- c("[10-60)", "[60-120)", "[120-300)", "[300-600)", "[600-1 800)", "[1 800-3 600)", "[3 600-94 286]")

data <- read.csv2("/home/pieter/durations.csv", header = TRUE)
data <- data$duration[data$duration >= 10]

summary(data)

bins <- mutate(
  category = case_when(
    data >= 10 & data < 60 ~ categories[1],
    data >= 60 & data < 120 ~ categories[2],
    data >= 120 & data < 300 ~ categories[3],
    data >= 300 & data < 600 ~ categories[4],
    data >= 600 & data < 1800 ~ categories[5],
    data >= 1800 & data < 3600 ~ categories[6],
    data >= 3600 ~ categories[7]
  ),
  as_tibble(data)
)

bins$category <- factor(bins$category, levels=categories, ordered=FALSE)

summary(bins)

ggplot(data=bins, aes(x=category, y=value)) +
  stat_summary(fun.y = length, fill = "bisque", geom = "bar") +
  stat_summary(aes(label=format(..y.., big.mark = " ")), fun.y = length, geom = "text", size = 3, vjust = -0.5) +
  guides(color=FALSE) +
  ggtitle("Test run durations on Travis-CI") +
  labs(x = "Duration interval (s)", y = "Amount of test runs") +
  scale_y_continuous(labels = function(x) format(x, big.mark = " ", scientific = FALSE)) +
  theme_bw(base_size = 12, base_family = "") %+replace% 
  theme(axis.ticks = element_blank(), legend.background = element_blank(), 
        legend.position = "bottom", legend.title = element_blank(),
        legend.key = element_blank(), panel.background = element_blank(), 
        panel.border = element_blank(), strip.background = element_blank(), 
        axis.title.x = element_text(margin = margin(t = 0.5, b = 0, unit = "cm")),
        axis.title.y = element_text(margin = margin(r = 0.8, unit = "cm"), angle = 90),
        plot.background = element_blank(), complete = TRUE)
