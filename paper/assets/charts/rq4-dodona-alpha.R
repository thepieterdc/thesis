install.packages("ggplot2")
library(ggplot2)

data <- read.csv2("/home/pieter/Documenten/thesis/evaluation/dodona/performance.csv", header = TRUE, sep = ",")
data <- subset(data, Alpha > -1 & Alpha < 80)
data$idx = seq(1:length(data$commit))

ggplot(data, aes(idx)) +
  geom_line(aes(y = Original, color = "Original")) +
  geom_line(aes(y = Alpha, color = "Alpha")) +
  ggtitle("Performance of the Alpha algorithm on Dodona") +
  labs(x = "Test run", y = "# test cases before first failure") +
  scale_color_manual(name = "Algorithm", values = c("Original" = "gray", "Alpha" = "red")) +
  theme_bw(base_size = 12, base_family = "") %+replace% 
  theme(axis.ticks = element_blank(), legend.background = element_blank(), 
        legend.position = "right", legend.title = element_text("Algorithm"),
        legend.key = element_blank(), panel.background = element_blank(), 
        panel.border = element_blank(), strip.background = element_blank(), 
        axis.title.x = element_text(margin = margin(t = 0.5, b = 0, unit = "cm")),
        axis.title.y = element_text(margin = margin(r = 0.8, unit = "cm"), angle = 90),
        plot.background = element_blank(), complete = TRUE)
