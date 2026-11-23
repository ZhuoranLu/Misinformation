valid_predictions_all <-read.table('valid_predictions_task_240907.csv',header=TRUE,sep=',')
## model x - y
direct_model = glm(selfCorrect ~  ai_correct + ai_incorrect + expert_correct, data = valid_predictions_all, family = binomial(link = "logit"))
summary(direct_model)

mediation = glm(crowd_vote_correct ~  ai_correct + ai_incorrect, data = valid_predictions_all)
summary(mediation)

full_model = glm(selfCorrect ~  ai_correct + ai_incorrect + expert_correct + crowd_vote_correct, data = valid_predictions_all, family = binomial(link = "logit"))
summary(full_model)
