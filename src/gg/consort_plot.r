# GOAL: Creating a consort diagram to describe how search engine choices have been narrowed

# Load Library ----------------------------------------
library(janitor)
library(dplyr)
library(ggplot2)

# Write a function to create our consort diagram ------------

consort_plot_function <- function(r_consort_input_df, r_query_summary_df, out_consort_png, logical_operator){

# Read in all important datasets from python--------------

consort_input_df <- r_consort_input_df

names(consort_input_df) <- gsub(" ", "_", names(consort_input_df))

query_requests <- r_query_summary_df%>%
  mutate(Search_Options = gsub(" ", "_", Search_Options))

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
    consort_col <- paste0("Filtered_Column_", query_requests$`Search_Options`[i])
  
  #Need to account for when no variation in a column
  value_count_included <- table(consort_input_df[`consort_col`] == TRUE)
  if (!"TRUE" %in% names(value_count_included)) {
    value_count_included[["TRUE"]] <- 0
  }
  num_included <- value_count_included[["TRUE"]]
  
  value_count_excluded <- table(consort_input_df[`consort_col`] == FALSE)

    if (!"TRUE" %in% names(value_count_excluded)) {
    value_count_excluded[["TRUE"]] <- 0
  }
  num_excluded <- value_count_excluded[["TRUE"]]
  
p <- p+  
  #Exclusion rectangle
geom_rect(xmin = 70, xmax=97, ymin=88-(10*(i-1)), ymax=94-(10*(i-1)), color='black',
            fill='white', size=0.25) +
  annotate('text', x= 83.5, y=91-(10*(i-1)), label= paste0(num_excluded, " excluded for \n", colnames(consort_input_df)[i]), size=2.5)+
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
# Due to trickiness of colnames, we subset by matching by index
if(logical_operator == "&&"){

consort_input_df$index <- 1:nrow(consort_input_df)

consort_subset_info <- tibble(consort_input_df[`consort_col`] == TRUE)
consort_subset_info$index <- 1:nrow(consort_subset_info)
subset_dataset <- consort_subset_info[consort_subset_info[ ,1] == TRUE, ]

consort_input_df <- merge(consort_input_df, subset_dataset, by="index", all=FALSE)
    }

}
  

ggsave(out_consort_png, p)

}