
# Forest plot drawing
# Load R packages
library(ggthemes)
library(ggplot2)

# Load data
dataset <- read.csv(file.choose(), header = TRUE)
dataset <- read.csv("/Volumes/demo.csv", header = TRUE)

# Forest plot drawing
a <- ggplot(dataset, aes(Coefficient, Index)) +
  geom_point(size = 2, color = "black") +
  geom_errorbarh(aes(xmax = Coefficient + `SD`, xmin = Coefficient - `SD`), size = 0.2, height = 0.2, colour = "black") +
  scale_x_continuous(limits = c(-0.2, 0.2)) +
  geom_vline(aes(xintercept = 0), color = "gray", linetype = "dashed", size = 0.6) +
  xlab('Coefficient') + 
  ylab(' ') +
  theme_few() +
  theme(axis.text.x = element_text(size = 20, color = "black")) +
  theme(axis.text.y = element_text(size = 20, color = "black")) +
  theme(title = element_text(size = 20)) +
  theme_bw() +
  theme(axis.ticks.length = unit(-0.25, "cm"), 
        axis.text.x = element_text(margin = unit(c(0.5, 0.5, 0.5, 0.5), "cm")), 
        axis.text.y = element_text(margin = unit(c(0.5, 0.5, 0.5, 0.5), "cm")))

# View plot 'a'
a
