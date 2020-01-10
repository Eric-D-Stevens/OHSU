#qnorm(.5, 15, 4)




# 3 die ostatistics Oct 30:
library(tidyverse)
set.seed(12345)
unif_means_ten <- numeric(10) # space for big results (vector of Os)
for (i in 1:10000){
  x <- runif(10, min = 1, max = 6) # draw random sample with 10 observations each
  unif_means_ten[i] <- mean(x) # compute mean for each ith sample
}
my_sim <- unif_means_ten %>% tibble(sample_mean = .)
my_sim

mm <- mean(unif_means_ten) # mean of the sampling distribution of means
mm

sem <- sd(unif_means_ten) # sem
sem


graph <- ggplot(my_sim, aes(x = sample_mean)) +
  geom_density(color = "dodgerblue") +
  stat_function(fun = dnorm, args = list(mean = mm, sd = sem), color = "red")

graph
