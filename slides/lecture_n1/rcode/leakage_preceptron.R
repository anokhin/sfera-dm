rm(list = ls())
library(scales)

df_sd <- 0.1
n <- 25

df_and <- data.frame(
  x = c(rnorm(n, 0, df_sd), rnorm(n, 0, df_sd), rnorm(n, 1, df_sd), rnorm(n, 1, df_sd)),
  y = c(rnorm(n, 0, df_sd), rnorm(n, 1, df_sd), rnorm(n, 0, df_sd), rnorm(n, 1, df_sd)),
  label = c(rep(-1, 3*n), rep(1, n)))
png('./../images/leakage_perceptron_and.png', width = 640, height = 480)
plot(df_and$x, df_and$y, 
     col = c(alpha('red', 0.7), alpha('blue', 0.7))[as.factor(df_and$label)], pch = 19,
     main = 'Noised AND operation')
fit_and <- lm(label ~ ., data = df_and)
k_and <- -fit_and$coefficients[2]/fit_and$coefficients[3]
b_and <- -fit_and$coefficients[1]/fit_and$coefficients[3]
abline(a = b_and, b = k_and, 
       col = 'darkgreen', lwd = 3, lty = 2)
dev.off()


df_xor <- data.frame(
  x = c(rnorm(n, 0, df_sd), rnorm(n, 0, df_sd), rnorm(n, 1, df_sd), rnorm(n, 1, df_sd)),
  y = c(rnorm(n, 0, df_sd), rnorm(n, 1, df_sd), rnorm(n, 0, df_sd), rnorm(n, 1, df_sd)),
  label = c(rep(-1, n), rep(1, n), rep(1, n), rep(-1, n)))
png('./../images/leakage_perceptron_xor.png', width = 640, height = 480)
plot(df_xor$x, df_xor$y, 
     col = c(alpha('red', 0.7), alpha('blue', 0.7))[as.factor(df_xor$label)], pch = 19,
     main = 'Noised XOR operation')
fit_xor <- lm(label ~ ., data = df_xor)
k_xor <- -fit_xor$coefficients[2]/fit_xor$coefficients[3]
b_xor <- -fit_xor$coefficients[1]/fit_xor$coefficients[3]
abline(a = b_xor, b = k_xor, 
       col = 'darkgreen', lwd = 3, lty = 2)
dev.off()
