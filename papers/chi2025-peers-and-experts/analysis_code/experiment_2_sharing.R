valid_predictions_all <-read.table('valid_predictions_task_exp2_240918.csv',header=TRUE,sep=',')
## model x - y
direct_model = glm(finalWill ~  ai_positive + ai_negative + expert, data = valid_predictions_all)
summary(direct_model)

mediation = glm(crowd_positive_mean ~  ai_positive + ai_negative, data = valid_predictions_all, family = binomial(link = "logit"))
summary(mediation)

full_model = glm(finalWill ~  ai_positive + ai_negative + expert + crowd_vote, data = valid_predictions_all)
summary(full_model)

