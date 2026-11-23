valid_predictions_all <-read.table('exp2_240902.csv',header=TRUE,sep=',')

moderation_model = glm(selfCorrect ~  treatment + expert_correct + crowd_vote_correct+
                         crowd_vote_correct:crowd_ai_agreement
                       + expert_correct:expert_ai_agreement, data = valid_predictions_all, family = binomial(link = "logit"))
summary(moderation_model)
