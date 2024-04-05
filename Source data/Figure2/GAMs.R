library(mgcv)
library(segmented)
library(ggplot2)

# ??ȡ????
#data <- read.table("/Users/xnh/Desktop/PR_MF.txt", header = TRUE)
data<-read.csv("Demo.csv",
               header = T)
gam_model <- gam(y ~ s(x, k = 2), data = data)

summary(gam_model)
seg_model <- segmented(glm(y ~ x + x^2, data = data), seg.Z = ~x, psi = c(0.5,2))
breakpoints <- seg_model$psi
print(breakpoints)
plot(gam_model, xlab = "Pesticide risk", ylab = "Multifunctionality")
abline(v = 3.969056, col = "red", lty = 2)


