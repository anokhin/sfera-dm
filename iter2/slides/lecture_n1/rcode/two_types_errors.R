rm(list = ls())
library(scales)

df_sd <- 0.3
df <- data.frame(
  x = c(rnorm(25, -1, df_sd), rnorm(25, 1, df_sd)),
  y = c(rnorm(25, -1, df_sd), rnorm(25, 1, df_sd)),
  label = c(rep(-1, 25), rep(1, 25))
  )
plot(df$x, df$y, 
     col = c(alpha('red', 0.7), alpha('blue', 0.7))[as.factor(df$label)], pch = 19,
     main = 'Two types of error')
fit <- lm(label ~ ., data = df)
k <- -fit$coefficients[2]/fit$coefficients[3]
b <- -fit$coefficients[1]/fit$coefficients[3]
abline(a = b, b = k, 
       col = 'darkgreen', lwd = 3, lty = 2)

points(-abs(min(df$x[which(df$label == -1)]))/4, b, col = 'blue', pch = 17)
points(abs(max(df$x[which(df$label == 1)]))/4, b, col = 'red', pch = 17)

legend('topleft', c('class 0', 'class 1', 'decision boundary', 'error 1', 'error 2'), 
       lwd = c(NA, NA, 3, NA, NA), lty = c(NA, NA, 3, NA, NA), pch = c(19, 19, NA, 17, 17), 
       col=c('red', 'blue', 'darkgreen', 'red', 'blue'))
