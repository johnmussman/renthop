library(randomForest)
library(readr)

setwd('~/kaggle/renthop/')
df <- read.csv('models/analysisR/framed_data_1.csv', sep='\t')

df$interest_level <- as.factor(df$interest_level)
df$price <- as.integer(df$price)
df$bedrooms <- as.double(df$bedrooms)
df$bathrooms <- as.double(df$bathrooms)
df$latitude <- as.double(df$latitude)
df$longitude <- as.double(df$longitude)
df$building_id <- as.factor(df$building_id)
df$manager_id <- as.factor(df$manager_id)
for(i in 13:length(colnames(df))) {
  df[,colnames(df)[i]] <- as.logical(df[,colnames(df)[i]])
}

df$prewar <- df$pre.war + df$prewar

train_rows <- sample(c(TRUE, TRUE, FALSE), nrow(df), replace = TRUE)
train <- df[train_rows,]
test <- df[!train_rows,]

# took 10 min to run with 500 trees, gave logloss .666 using 2/3 training set and 33 features
rf <- randomForest(interest_level ~ price + bedrooms + bathrooms + 
                     latitude + longitude + manager_id + #building_id +
                     common.outdoor.space + laundry.in.building +
                     exclusive + hardwood + dining.room + terrace +
                     doorman + fitness.center + balcony + prewar +
                     wheelchair.access + swimming.pool + laundry.in.unit +
                     elevator + high.speed.internet + hardwood.floors +
                     outdoor.space + loft + roof.deck + new.construction +
                     garden.patio + dishwasher + no.fee +
                     dogs.allowed + cats.allowed, train, ntree=500, importance=TRUE)

predicted <- as.data.frame(predict(rf, test, type = "prob"))

logloss <- function(predicted_probs, actuals) {
  correct_cols <- match(actuals, colnames(predicted_probs))
  predicted_probs_of_actual <- as.list(c())
  for(i in 1:dim(predicted)[1]) {
    predicted_probs_of_actual <- append(predicted_probs_of_actual, predicted_probs[i, correct_cols[i]])
  }
  
  cumulative_score = 0
  for(i in 1:length(predicted_probs_of_actual)) {
    cumulative_score <- cumulative_score + log(max(min(as.double(predicted_probs_of_actual[i]), 1 - 1e-15), 1e-15))
  }
  return(-1 * cumulative_score/length(predicted_probs_of_actual))
}

logloss(predicted, test$interest_level)

#mean(predicted == test$interest_level)
 
#plot(test$interest_level, predicted)

varImpPlot(rf)
