library(ggplot2)
library(tibble)

data <- read.csv2("/home/pieter/consecutive-failures.csv", header = TRUE, sep = ",")

data$failed <- data$failed == "true"
data$gh_build_started_at <- strptime(data$gh_build_started_at, format = "%Y-%m-%d %H:%M:%S")

fills <- c("Total runs" = "bisque", "Failed runs" = "#feab9d")

ggplot(data, aes(x=gh_build_started_at)) +
  geom_histogram(data=data, aes(fill = "Total runs"), size = 0) +
  geom_histogram(data=subset(data, failed == TRUE), aes(fill = "Failed runs"), size = 0) +
  guides(color=FALSE) +
  ggtitle("Consecutive failures on Travis CI over time") +
  labs(x = "Time", y = "Consecutive test suite executions") +
  scale_fill_manual("Status", values = fills, guide = guide_legend(
    direction = "horizontal",
    label.position = "left"
  )) +
  theme_bw(base_size = 12, base_family = "") %+replace% 
  theme(axis.ticks = element_blank(), legend.background = element_blank(), 
        legend.position = "bottom", legend.title = element_blank(),
        legend.key = element_blank(), panel.background = element_blank(), 
        panel.border = element_blank(), strip.background = element_blank(), 
        axis.title.x = element_text(margin = margin(t = 0.5, b = 0, unit = "cm")),
        axis.title.y = element_text(margin = margin(r = 0.8, unit = "cm"), angle = 90),
        plot.background = element_blank(), complete = TRUE)
