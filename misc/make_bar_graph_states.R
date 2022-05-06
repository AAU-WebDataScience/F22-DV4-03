library(tidyverse)
library(ggplot2)
my_data <- read.csv("D:/Documents - HDD/GitHub/F22-DV4-03/misc/amount_of_states.csv")


ggplot(my_data %>% filter(Amount > 0), aes(x = reorder(State, -Amount), y=Amount))+geom_bar(stat = "identity", color="#211A52", fill="#211A52")+xlab("State code")+theme_minimal()