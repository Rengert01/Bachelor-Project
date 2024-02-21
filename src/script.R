library(reshape2)
library(dplyr)
library(ggplot2)

setwd("/home/rengert/BP/src/csv")

reports <- read.csv("reports.csv")
ratings <- read.csv("ratings.csv")

# Assuming your data frames are named reports and ratings
# Convert the ratings columns to numeric if they are not already
ratings$Hidde <- as.numeric(ratings$Hidde)
ratings$Max <- as.numeric(ratings$Max)
ratings$Gabriel <- as.numeric(ratings$Gabriel)

# Reshape data to long format for ANOVA
ratings_long <- melt(ratings)

head(ratings_long)

# Perform repeated measures ANOVA
anova_result <- aov(value ~ variable, data = ratings_long)

# perform tukey hsd test
TukeyHSD(anova_result, conf.level=.95)

# Print the summary of the ANOVA
summary(anova_result)

# Create a violin plot
ggplot(ratings_long, aes(x = variable, y = value, fill = variable)) +
  geom_violin() +
  geom_boxplot(width = 0.2, fill = "white", color = "black") +
  labs(title = "Violin Plot of Ratings",
       x = "Individuals",
       y = "Ratings") +
  coord_cartesian(ylim = c(1, 10)) +
  theme_minimal()

# boxplot <- ggplot(ratings_long, aes(x = variable, y = value)) +
#   geom_boxplot() +
#   labs(title = "Boxplot of Ratings by Difficulty Level",
#        x = "Difficulty Level",
#        y = "Rating")
# 
# # Print the boxplot
# print(boxplot)

reports <- reports %>%
  mutate(Hidde = recode(Hidde, "Human" = -1, "Draw!" = 0, "AI" = 1),
         Max = recode(Max, "Human" = -1, "Draw!" = 0, "AI" = 1),
         Gabriel = recode(Gabriel, "Human" = -1, "Draw!" = 0, "AI" = 1))

# Reshape data to long format for ANOVA
reports_long <- melt(reports)

head(reports_long)

# Perform repeated measures ANOVA
anova_result <- aov(value ~ variable, data = reports_long)

summary(anova_result)

# perform tukey hsd test
TukeyHSD(anova_result, conf.level=.95)

# Define labels for the values
value_labels <- c("-1" = "Loss", "0" = "Draw", "1" = "Win")

# Create a bar plot
ggplot(reports_long, aes(x = factor(value), fill = factor(value))) +
  geom_bar() +
  facet_wrap(~variable, scales = "free_y") +
  labs(title = "Bar Plot of Performance",
       x = "Performance",
       y = "Count") +
  scale_x_discrete(labels = value_labels) +  # Customize x-axis labels
  coord_cartesian(ylim = c(0, 20)) +  # Set consistent y-axis range
  theme_minimal()

# boxplot2 <- ggplot(reports_long, aes(x = variable, y = value)) +
#   geom_boxplot() +
#   labs(title = "Boxplot of Performane by Difficulty Level",
#        x = "Difficulty Level",
#        y = "Performance")
# 
# # Print the boxplot
# print(boxplot2)