library(polycor)
setwd("C:\\Users\\Samar\\PycharmProjects\\Skin_disease")
path <- "input/dataset.csv"
dataset <- read.csv(path)

columns= c("Correlation") 
dataframe = setNames(data.frame(matrix(ncol = 1, nrow = 0)), columns)

dependent <- dataset$disease

cols <- head(colnames(dataset), -2)
for(i in cols) { 
  independent <- dataset[, i]
  vec <- c(polychor(independent, dependent))
  dataframe[i, ] <- vec
}

print(head(dataframe))

write.csv(dataframe, "input/output.csv")