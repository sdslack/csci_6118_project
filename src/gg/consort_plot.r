# GOAL: Creating a consort diagram to describe how search engine choices have been narrowed

# Load Library ----------------------------------------
library(janitor)
library(dplyr)
library(ggplot2)

# Read in all important datasets from python--------------

    consort_input_df <- read.csv("data/consort_input_df.csv")
    query_requests <- read.csv("data/query_requests.csv")


#GGPLOT Consort Diagram--------------------------------------------
ggplot_setup <- tibble(x= 1:100, y= 1:100)

p <- ggplot_setup %>% 
  ggplot(aes(x, y)) +
  scale_x_continuous(minor_breaks = seq(10, 100, 10)) +
  scale_y_continuous(minor_breaks = seq(10, 100, 10)) +
  theme_linedraw()+
  #Overall box
  geom_rect(xmin = 10, xmax=50, ymin=94, ymax=100, color='black',
            fill='white', size=0.25) +
  annotate('text', x= 30, y=97,label= paste0(nrow(consort_input_df), " sequences available"), size=2.5)+
  theme_void()

# Create loop to continually add more boxes based on the number of search criteria that we have
for (i in 1:nrow(query_requests)) {
# Include only the relevant columns
consort_col <- i - 1
  
  #Need to account for when no variation in a column
  value_count_included <- table(consort_input_df[[paste0("Include_Column", consort_col)]] == "Included")
  if (!"TRUE" %in% names(value_count_included)) {
    value_count_included[["TRUE"]] <- 0
  }
  num_included <- value_count_included[["TRUE"]]
  
  value_count_excluded <- table(consort_input_df[[paste0("Include_Column", consort_col)]] == "Excluded")
  if (!"TRUE" %in% names(value_count_excluded)) {
    value_count_excluded[["TRUE"]] <- 0
  }
  num_excluded <- value_count_excluded[["TRUE"]]
  
p <- p+  
  #Exclusion rectangle
geom_rect(xmin = 70, xmax=97, ymin=88-(10*(i-1)), ymax=94-(10*(i-1)), color='black',
            fill='white', size=0.25) +
  annotate('text', x= 83.5, y=91-(10*(i-1)), label= paste0(num_excluded, " excluded for \n", colnames(consort_input_df)[i+1]), size=2.5)+
  #Inclusion Rectangle
  geom_rect(xmin = 15, xmax=45, ymin=84-(10*(i-1)), ymax=90-(10*(i-1)), color='black',
            fill='white', size=0.25) +
  annotate('text', x= 30, y=87-(10*(i-1)),label= paste0(num_included, " available"), size=2.5)+
  #Inclusion arrow
  geom_segment(
    x=30, xend=30, y=94-(10*(i-1)), yend=90-(10*(i-1)), 
    size=0.15, linejoin = "mitre", lineend = "butt",
    arrow = arrow(length = unit(1, "mm"), type= "closed")) +
  #Exclusion arrow
  geom_segment(
    x=30, xend=69.7, y=92-(10*(i-1)), yend=92-(10*(i-1)), 
    size=0.15, linejoin = "mitre", lineend = "butt",
    arrow = arrow(length = unit(1, "mm"), type= "closed"))
    
# Subset the consort_input_df to only include entries which passed the most recent query filter
# before moving on to the next query filter
  subset_column <- paste0("Include_Column", consort_col)
  consort_input_df <- consort_input_df[consort_input_df[[subset_column]] == "Included", ]
}
  


ggsave("data/Consort_Plot.png", p)
