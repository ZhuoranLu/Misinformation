valid_predictions_all <-read.table('valid_predictions_task_240907.csv',header=TRUE,sep=',')
## model x - y
direct_model = glm(finalWill ~  ai_positive + ai_negative + expert, data = valid_predictions_all)
summary(direct_model)

mediation = glm(crowd_positive_mean ~  ai_positive + ai_negative, data = valid_predictions_all)
summary(mediation)

full_model = glm(finalWill ~  ai_positive + ai_negative + expert + crowd_positive_mean, data = valid_predictions_all)
summary(full_model)
