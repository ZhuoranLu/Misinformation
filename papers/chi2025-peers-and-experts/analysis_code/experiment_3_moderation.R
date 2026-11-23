moderation_model = glm(selfCorrect ~  ai_correct + ai_incorrect + expert_correct + crowd_vote_correct+
                         crowd_vote_correct:crowd_ai_agreement + crowd_vote_correct:crowd_ai_disagreement
                       + expert_correct:expert_ai_agreement + expert_correct:expert_ai_disagreement, data = valid_predictions_all, family = binomial(link = "logit"))
summary(moderation_model)
