# %% analysis block 1
def cohen_d(df,measurement,helper):
    con = df.query("treatment==0")[measurement]
    exp = df.query("treatment==1")[measurement]
    return helper(con,exp)

def cohen_d_helper(con,exp):
    std_pooled = ((np.std(con)**2+np.std(exp)**2)/2)**(0.5)
    return np.abs(np.mean(con)-np.mean(exp))/std_pooled

def cohen_w_helper(con,exp):
    cohen_w = chisquare_effectsize([np.sum(con), np.sum(con == False)], 
                               [np.sum(exp), np.sum(exp == False)])
    return cohen_w

# %% analysis block 23
def t_test_helper(df,measure):
    print("dependent variable",measure)
    con = df.query("treatment==0")[measure]
    exp = df.query("treatment==1")[measure]
    print("con mean, std:",con.mean(),con.std())
    print("exp mean, std:",exp.mean(),exp.std())
    print(len(df)-1)
    print("t test:")
    print(ttest_ind(con,exp))
    print("kruskal:")
    print(kruskal(con,exp))
    print(" ")

# %% analysis block 78
def boot_strap(df_agree,df_disagree,measurement):
    agree_list = []
    disagree_list = []
    for i in range(1000):
        agree = cohen_d(df_agree.sample(len(df_agree),replace=True),measurement,cohen_d_helper)
        disagree = cohen_d(df_disagree.sample(len(df_disagree),replace=True),measurement,cohen_d_helper)
        agree_list.append(agree)
        disagree_list.append(disagree)
    agree_list = np.array(agree_list)
    disagree_list = np.array(disagree_list)
    print("agree",np.mean(agree_list),np.quantile(agree_list,0.05),np.quantile(agree_list,0.95))
    print("disagree",np.mean(disagree_list),np.quantile(disagree_list,0.05),np.quantile(disagree_list,0.95))
    print("delta d:", np.mean(agree_list)-np.mean(disagree_list))
    print("superiority: ",np.mean((agree_list-disagree_list)>0))
    return agree_list,disagree_list,ttest_rel(agree_list,disagree_list)

# %% analysis block 26
def generate_res(df):
    res = pd.DataFrame()
    
    for elem in set(df["workerId"]):
        temp_res = pd.DataFrame()
        temp_predictions = df.query("workerId==@elem")
        
        temp_survey = survey.query("workerId==@elem")
        temp_expertise_survey = expertise_survey.query("workerId==@elem")
        
        if len(temp_survey)>0:
            temp_res["programming"] = [temp_survey["programming"].values[0]]
            temp_res["age"] = [temp_survey["age"].values[0]]
            temp_res["social_media"] = [temp_survey["socialMedia"].values[0]]
            temp_res["gender"] = [temp_survey["gender"].values[0]]

        if len(temp_expertise_survey)>0:
            temp_res["occupation"] = [temp_expertise_survey["occupation"].values[0]]
            temp_res["education"] = [temp_expertise_survey["education"].values[0]]
            
        temp_res["workerId"] = [elem]
        temp_res["treatment"] = [temp_predictions["treatment"].values[0]]
        
        true_acc = temp_predictions.query("label==1")["selfCorrect"].mean()
        false_acc = temp_predictions.query("label==0")["selfCorrect"].mean()
        true_will = temp_predictions.query("label==1")["finalWill"].mean()
        false_will = temp_predictions.query("label==0")["finalWill"].mean()
        
        conf_correct = temp_predictions.query("selfCorrect==1")["finalConfidence"].mean()
        conf_incorrect = temp_predictions.query("selfCorrect==0")["finalConfidence"].mean()
        conf_discernment = conf_correct-conf_incorrect
        temp_res["conf_correct"] = [conf_correct]
        temp_res["conf_incorrect"] = [conf_incorrect]
        temp_res["conf_discernment"] = [conf_discernment]
        
        
        temp_res["truth_discernment"] = [true_acc-(1-false_acc)]
        temp_res["truth_discernment"] = [true_acc-(1-false_acc)]
        temp_res["willingness_discernment"] = [true_will-false_will]
        temp_res["true_will"] = [true_will]
        temp_res["false_will"] = [false_will]
        


#         temp_res["agree_"] = [false_will]
#         temp_res["false_will"] = [false_will]

        temp_res["accuracy"] = [temp_predictions["selfCorrect"].mean()]

        res = pd.concat([res,temp_res])
        

    return res
res = generate_res(valid_predictions_task)
res_agree = generate_res(valid_predictions_task_agree)
res_disagree = generate_res(valid_predictions_task_disagree)
res_4 = generate_res(valid_predictions_task.query("prev_length==4"))
res_6 = generate_res(valid_predictions_task.query("prev_length==6"))
res_8 = generate_res(valid_predictions_task.query("prev_length==8"))

# %% analysis block 35
t_test_helper(valid_predictions_task,"selfCorrect")
t_test_helper(res,"truth_discernment")

t_test_helper(valid_predictions_task.query("label==1"),"finalWill")
t_test_helper(valid_predictions_task.query("label==0"),"finalWill")
t_test_helper(res_disagree,"willingness_discernment")

# %% analysis block 38
t_test_helper(valid_predictions_task.query("expert_ai_agreement==1"),"selfCorrect")
t_test_helper(res_agree,"truth_discernment")
print("    ")
t_test_helper(valid_predictions_task.query("expert_ai_agreement==1 and label==1"),"finalWill")
t_test_helper(valid_predictions_task.query("expert_ai_agreement==1 and label==0"),"finalWill")
t_test_helper(res_agree,"willingness_discernment")

# %% analysis block 49
t_test_helper(valid_predictions_task.query("expert_ai_agreement==0"),"selfCorrect")
t_test_helper(res_disagree,"truth_discernment")
print(" ")
t_test_helper(valid_predictions_task.query("expert_ai_agreement==0 and label==1"),"finalWill")
t_test_helper(valid_predictions_task.query("expert_ai_agreement==0 and label==0"),"finalWill")
t_test_helper(res_disagree,"willingness_discernment")

# %% analysis block 51
t_test_helper(res,"willingness_discernment")

# %% analysis block 71
t_test_helper(valid_predictions_task.query("prev_length==4"),"selfCorrect")
t_test_helper(valid_predictions_task.query("prev_length==6"),"selfCorrect")
t_test_helper(valid_predictions_task.query("prev_length==8"),"selfCorrect")

# %% analysis block 85
t_test_helper(valid_predictions_task.query("prev_length==4"),"selfCorrect")
cohen_d(valid_predictions_task.query("prev_length==4"),"selfCorrect",cohen_d_helper)
t_test_helper(valid_predictions_task.query("prev_length==6"),"selfCorrect")
cohen_d(valid_predictions_task.query("prev_length==6"),"selfCorrect",cohen_d_helper)
t_test_helper(valid_predictions_task.query("prev_length==8"),"selfCorrect")
cohen_d(valid_predictions_task.query("prev_length==8"),"selfCorrect",cohen_d_helper)

# %% analysis block 97
t_test_helper(valid_predictions_task.query("label==1 and expert_ai_agreement==1"),"finalWill")
t_test_helper(valid_predictions_task.query("label==1 and expert_ai_agreement==0"),"finalWill")

t_test_helper(valid_predictions_task.query("label==0 and expert_ai_agreement==1"),"finalWill")
t_test_helper(valid_predictions_task.query("label==0 and expert_ai_agreement==0"),"finalWill")

# %% analysis block 159
valid_predictions_task["label_real"] = valid_predictions_task.apply(lambda x: 1 if x["label"]==1 and x["treatment"]==1 else 0,axis=1)
valid_predictions_task["label_fake"] = valid_predictions_task.apply(lambda x: 1 if x["label"]==0 and x["treatment"]==1 else 0,axis=1)

import statsmodels.api as sm
def mediation(df,dep,crowd,expert,ai):
    print("x - y")
    dep_df = df[dep]
    indep = df[ai+expert+["constant"]]
    distribution = sm.families.Binomial() if len(set(dep_df))==2 else sm.families.Gaussian()
    
    gamma_model = sm.GLM(dep_df, indep, family=distribution)
    gamma_results = gamma_model.fit()

    print(gamma_results.summary())

    print("x - m")

    dep_df = df[crowd[0]]
    indep = df[ai+["constant"]]
    distribution = sm.families.Binomial() if len(set(dep_df))==2 else sm.families.Gaussian()

    gamma_model = sm.GLM(dep_df, indep, family=distribution)
    gamma_results = gamma_model.fit()
    print(gamma_results.summary())

    print("x+m - y")

    dep_df = df[dep]
    indep = df[ai+crowd+expert+["constant"]]
    distribution = sm.families.Binomial() if len(set(dep_df))==2 else sm.families.Gaussian()

    gamma_model = sm.GLM(dep_df, indep, family=distribution)
    gamma_results = gamma_model.fit()
    print(gamma_results.summary())
mediation(valid_predictions_task,"selfCorrect",["crowd_vote_correct"],["expert_ai_agreement"],["treatment"])
# mediation(valid_predictions_task,"finalWill",["crowd_prediction"],["expert"],["label_real","label_fake"])
# mediation(valid_predictions_task.query("label==0"),"finalWill",crowd = "crowd_prediction",expert = "expert")

# %% analysis block 79
truth_discernment_agree_list,truth_discernment_disagree_list,t_res = boot_strap(res_agree,res_disagree,"truth_discernment")
np.quantile(truth_discernment_agree_list,0.05),np.quantile(truth_discernment_agree_list,0.95)
np.quantile(truth_discernment_disagree_list,0.05),np.quantile(truth_discernment_disagree_list,0.95)
t_res

# %% analysis block 98
acc_agree_list,acc_disagree_list,t_res = boot_strap(valid_predictions.query("expert_ai_agreement==1"),valid_predictions.query("expert_ai_agreement==0"),"selfCorrect")
np.quantile(acc_agree_list,0.05),np.quantile(acc_agree_list,0.95)
np.quantile(acc_disagree_list,0.05),np.quantile(acc_disagree_list,0.95)
t_res

# %% analysis block 99
acc_agree_list,acc_disagree_list,t_res = boot_strap(valid_predictions.query("expert_ai_agreement==1 and label==1"),valid_predictions.query("expert_ai_agreement==0 and label==1"),"finalWill")
np.quantile(acc_agree_list,0.05),np.quantile(acc_agree_list,0.95)
np.quantile(acc_disagree_list,0.05),np.quantile(acc_disagree_list,0.95)
t_res

# %% analysis block 100
willingness_discernment_agree_list,willingness_discernment_disagree_list,t_res = boot_strap(res_agree,res_disagree,"willingness_discernment")
np.quantile(willingness_discernment_agree_list,0.05),np.quantile(willingness_discernment_agree_list,0.95)
np.quantile(willingness_discernment_disagree_list,0.05),np.quantile(willingness_discernment_disagree_list,0.95)
t_res

# %% analysis block 101
will_true_discernment_agree_list,will_true_discernment_disagree_list,t_res = boot_strap(res_agree,res_disagree,"truth_discernment")
np.quantile(willingness_discernment_agree_list,0.05),np.quantile(willingness_discernment_agree_list,0.95)
np.quantile(willingness_discernment_disagree_list,0.05),np.quantile(willingness_discernment_disagree_list,0.95)
t_res

# %% analysis block 149
boot_strap(valid_predictions_task.query("expert_ai_agreement==1"),valid_predictions_task.query("expert_ai_agreement==0"),"selfCorrect")
boot_strap(res_agree,res_disagree,"truth_discernment")

# %% analysis block 150
boot_strap(valid_predictions_task.query("expert_ai_agreement==1 and label==1"),valid_predictions_task.query("expert_ai_agreement==0 and label==1"),"finalWill")
boot_strap(valid_predictions_task.query("expert_ai_agreement==1 and label==0"),valid_predictions_task.query("expert_ai_agreement==0 and label==0"),"finalWill")
boot_strap(res_agree,res_disagree,"willingness_discernment")

# %% analysis block 151
boot_strap(valid_predictions_task.query("expert_ai_agreement==1 and label==1"),valid_predictions_task.query("expert_ai_agreement==0 and label==1"),"finalWill")
boot_strap(valid_predictions_task.query("expert_ai_agreement==1 and label==0"),valid_predictions_task.query("expert_ai_agreement==0 and label==0"),"finalWill")
boot_strap(res_agree,res_disagree,"willingness_discernment")

# %% analysis block 210
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import matplotlib.font_manager as font_manager

def vis_df_generate():
    accuracy_df = valid_predictions_task[["treatment","selfCorrect"]]
    willingness_real_df = valid_predictions_task.query("label==1")[["treatment","finalWill"]]
    willingness_fake_df = valid_predictions_task.query("label==0")[["treatment","finalWill"]]
    truth_discernment_df = res[["treatment","truth_discernment"]]
    willingness_discernment_df = res[["treatment","willingness_discernment"]]
    return [accuracy_df,truth_discernment_df,willingness_real_df,willingness_fake_df,willingness_discernment_df]
def bar_vis_rq3():
    import matplotlib as mpl
    
    all_accuracy_df = valid_predictions_task[["treatment","selfCorrect"]]
    all_willingness_real_df = valid_predictions_task.query("label==1")[["treatment","finalWill"]]
    all_willingness_fake_df = valid_predictions_task.query("label==0")[["treatment","finalWill"]]
    all_truth_discernment_df = res[["treatment","truth_discernment"]]
    all_willingness_discernment_df = res[["treatment","willingness_discernment"]]
    all_df_list = [all_accuracy_df,all_truth_discernment_df,all_willingness_real_df,all_willingness_fake_df,all_willingness_discernment_df]
    
    agree_accuracy_df = valid_predictions_task.query("expert_ai_agreement==1")[["treatment","selfCorrect"]]
    agree_willingness_real_df = valid_predictions_task.query("expert_ai_agreement==1").query("label==1")[["treatment","finalWill"]]
    agree_willingness_fake_df = valid_predictions_task.query("expert_ai_agreement==1").query("label==0")[["treatment","finalWill"]]
    agree_truth_discernment_df = res_agree[["treatment","truth_discernment"]]
    agree_willingness_discernment_df = res_agree[["treatment","willingness_discernment"]]
    agree_df_list = [agree_accuracy_df,agree_truth_discernment_df,agree_willingness_real_df,agree_willingness_fake_df,agree_willingness_discernment_df]

    disagree_accuracy_df = valid_predictions_task.query("expert_ai_agreement==0")[["treatment","selfCorrect"]]
    disagree_willingness_real_df = valid_predictions_task.query("expert_ai_agreement==0").query("label==1")[["treatment","finalWill"]]
    disagree_willingness_fake_df = valid_predictions_task.query("expert_ai_agreement==0").query("label==0")[["treatment","finalWill"]]
    disagree_truth_discernment_df = res_disagree[["treatment","truth_discernment"]]
    disagree_willingness_discernment_df = res_disagree[["treatment","willingness_discernment"]]
    disagree_df_list = [disagree_accuracy_df,disagree_truth_discernment_df,disagree_willingness_real_df,disagree_willingness_fake_df,disagree_willingness_discernment_df]
    
    df_mat = [all_df_list,agree_df_list,disagree_df_list]
    
    font = font_manager.FontProperties(family='calibri',weight='bold',style='normal', size=80)

#     df_list = vis_df_generate()
# figsize=(14,12)
    dep_number = 5
    fig, axs = plt.subplots(1,dep_number,figsize=(86,14))
    dep_list = ["selfCorrect","truth_discernment","finalWill","finalWill","willingness_discernment"]
    y_label_list = ["(a) Accuracy","(b) Truth Discernment","(c) Sharing Intention: Real","(d) Sharing Intention: Fake","(e) Sharing Discernment"]
    ylim_list = [[0.4,0.78],[-0.2,0.6],[4.6,5.6],[4.6,5.3],[-0.25,0.5]]
    hatch_list = ('', '/', '\\')
    mpl.rcParams['hatch.linewidth'] = 7
    mpl.rcParams['hatch.color'] = "white"
    color_list = ["#2A9C9D","#ffa600","gray"]
    font_size = 75
    index = 0
    width = 0.8
    treatment_list = ["No AI","AI Presented"]
    for ax in axs.flat:
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_xlabel(y_label_list[index],fontsize=font_size,fontname="calibri",weight="heavy")
    #     ax.set_yticklabels(fontsize=45)
    #     ax.set_yticks(x-0.2)
        ax.tick_params(axis='x', which='minor', labelsize=10)

        dep_var = dep_list[index]
        for condition in [0,1,2]:
            df_list = df_mat[condition]
            for treatment in [0,1]:
                loc = treatment*0.1 + condition*0.3
                dep = df_list[index].query("treatment==@treatment")[dep_var]
                if condition ==0:
                    temp_bar = ax.barh(loc, dep.mean(), width*0.1,color=color_list[treatment],hatch=hatch_list[treatment],label=treatment_list[treatment])
                else:
                    temp_bar = ax.barh(loc, dep.mean(), width*0.1,color=color_list[treatment],hatch=hatch_list[treatment])
                ax.errorbar(
                        dep.mean(),loc,xerr=sem(dep),ecolor="black",alpha=0.9,clip_on=True,ls='dashed',lw=8)
                ax.set_xlim(ylim_list[index])
    #         ax.errorbar(
    #             treatment,dep.mean()+sem(dep),alpha=0.9,xerr=0.05,color="black",clip_on=True,ls='dashed',lw=8)
    #         ax.errorbar(
    #             treatment,dep.mean()-sem(dep),alpha=0.9,xerr=0.05,color="black",clip_on=True,ls='dashed',lw=8)
        ax.tick_params(
            axis="x",
            which='both',
            labelsize=70
            )
        if index >= 1:
            print("ax")
            ax.tick_params(
            which='both', 
            right=False,# both major and minor ticks are affected
    #         bottom=False,
            left=False,# ticks along the bottom edge are off
    #         top=False,         # ticks along the top edge are off
    #         labelbottom=False
            labelleft=False
            )
        else:
            x = np.array([0.05,0.33,0.65])  # the label locations
            ax.set_yticks(x)
            ax.set_yticklabels(["All","Expert-AI Agree \n (Expert Correct)","Expert-AI Disagree \n (Expert Incorrect)"],{"fontsize":font_size})
    #         ax.set_yticklabels(["experimental"],{"fontsize":45})
#             plt.legend(prop=font,ncol=3,bbox_to_anchor=(0.0, 1.1, 0.1, 0.2))
    #         ax.bar(df_list[index]["treatment"], )
        if index==2:
            handles, labels = ax.get_legend_handles_labels()
            fig.legend(handles, labels, prop=font,ncol=2,bbox_to_anchor =(0.6,1.23))
            ax = fig.add_axes([0.6,1.08, 0.0, 0.0])

#                         legend_elements = [Line2D([0], [0], color='b', lw=4, label='Line'),
#                            Line2D([0], [0], marker='o', color='w', label='Scatter',
#                                   markerfacecolor='g', markersize=15),
#                            Patch(facecolor='orange', edgecolor='r',
#                                  label='Color Patch')]

        # Create the figure
#             fig, ax = plt.subplots()
#             ax.legend(handles=legend_elements, loc='center')

    
        index +=1
    fig.tight_layout(pad=-2.0)
    
    

    plt.savefig("./generated_images/experiment1/revision_exp1_"+"all"+"plot.png",dpi=45,bbox_inches='tight')
bar_vis_rq3()

# %% analysis block 224
def bar_vis_appendix():
    import matplotlib as mpl
    
    all_accuracy_df = valid_predictions_task.query("prev_length==4")[["treatment","selfCorrect"]]
    all_willingness_real_df = valid_predictions_task.query("prev_length==4").query("label==1")[["treatment","finalWill"]]
    all_willingness_fake_df = valid_predictions_task.query("prev_length==4").query("label==0")[["treatment","finalWill"]]
#     all_truth_discernment_df = res[["treatment","truth_discernment"]]
#     all_willingness_discernment_df = res[["treatment","willingness_discernment"]]
    all_df_list = [all_accuracy_df,all_willingness_real_df,all_willingness_fake_df]
    
    agree_accuracy_df = valid_predictions_task.query("prev_length==6")[["treatment","selfCorrect"]]
    agree_willingness_real_df = valid_predictions_task.query("prev_length==6").query("label==1")[["treatment","finalWill"]]
    agree_willingness_fake_df = valid_predictions_task.query("prev_length==6").query("label==0")[["treatment","finalWill"]]
#     agree_truth_discernment_df = res_agree[["treatment","truth_discernment"]]
#     agree_willingness_discernment_df = res_agree[["treatment","willingness_discernment"]]
    agree_df_list = [agree_accuracy_df,agree_willingness_real_df,agree_willingness_fake_df]

    disagree_accuracy_df = valid_predictions_task.query("prev_length==8")[["treatment","selfCorrect"]]
    disagree_willingness_real_df = valid_predictions_task.query("prev_length==8").query("label==1")[["treatment","finalWill"]]
    disagree_willingness_fake_df = valid_predictions_task.query("prev_length==8").query("label==0")[["treatment","finalWill"]]
#     disagree_truth_discernment_df = res_disagree[["treatment","truth_discernment"]]
#     disagree_willingness_discernment_df = res_disagree[["treatment","willingness_discernment"]]
    disagree_df_list = [disagree_accuracy_df,disagree_willingness_real_df,disagree_willingness_fake_df]
    
    df_mat = [all_df_list,agree_df_list,disagree_df_list]
    
    font = font_manager.FontProperties(family='calibri',weight='bold',style='normal', size=80)

#     df_list = vis_df_generate()
# figsize=(14,12)
    dep_number = 3
    fig, axs = plt.subplots(1,dep_number,figsize=(50,14))
    dep_list = ["selfCorrect","finalWill","finalWill"]
    y_label_list = ["(a) Accuracy","(c) Sharing Intention:\n Real","(d) Sharing Intention:\n Fake"]
    ylim_list = [[0.4,0.80],[4.7,5.6],[4.6,5.6]]
    hatch_list = ('', '/', '\\')
    mpl.rcParams['hatch.linewidth'] = 7
    mpl.rcParams['hatch.color'] = "white"
    color_list = ["#2A9C9D","#ffa600","gray"]
    font_size = 80
    index = 0
    width = 0.8
    treatment_list = ["No AI","AI Presented"]
    for ax in axs.flat:
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_xlabel(y_label_list[index],fontsize=font_size,fontname="Calibri",weight="heavy")
    #     ax.set_yticklabels(fontsize=45)
    #     ax.set_yticks(x-0.2)
        ax.tick_params(axis='x', which='minor', labelsize=10)

        dep_var = dep_list[index]
        for condition in [0,1,2]:
            df_list = df_mat[condition]
            for treatment in [0,1]:
                loc = treatment*0.1 + condition*0.3
                dep = df_list[index].query("treatment==@treatment")[dep_var]
                if condition ==0:
                    temp_bar = ax.barh(loc, dep.mean(), width*0.1,color=color_list[treatment],hatch=hatch_list[treatment],label=treatment_list[treatment])
                else:
                    temp_bar = ax.barh(loc, dep.mean(), width*0.1,color=color_list[treatment],hatch=hatch_list[treatment])
                ax.errorbar(
                        dep.mean(),loc,xerr=sem(dep),ecolor="black",alpha=0.9,clip_on=True,ls='dashed',lw=8)
                ax.set_xlim(ylim_list[index])
    #         ax.errorbar(
    #             treatment,dep.mean()+sem(dep),alpha=0.9,xerr=0.05,color="black",clip_on=True,ls='dashed',lw=8)
    #         ax.errorbar(
    #             treatment,dep.mean()-sem(dep),alpha=0.9,xerr=0.05,color="black",clip_on=True,ls='dashed',lw=8)
        ax.tick_params(
            axis="x",
            which='both',
            labelsize=70
            )
        if index >= 1:
            print("ax")
            ax.tick_params(
            which='both', 
            right=False,# both major and minor ticks are affected
    #         bottom=False,
            left=False,# ticks along the bottom edge are off
    #         top=False,         # ticks along the top edge are off
    #         labelbottom=False
            labelleft=False
            )
        else:
            x = np.array([0.05,0.33,0.65])  # the label locations
            ax.set_yticks(x)
            ax.set_yticklabels(["3 Peer\nJudgements","5 Peer\nJudgements","7 Peer\nJudgements"],{"fontsize":font_size})
    #         ax.set_yticklabels(["experimental"],{"fontsize":45})
#             plt.legend(prop=font,ncol=3,bbox_to_anchor=(0.0, 1.1, 0.1, 0.2))
    #         ax.bar(df_list[index]["treatment"], )
        if index==2:
            handles, labels = ax.get_legend_handles_labels()
            fig.legend(handles, labels, prop=font,ncol=2,bbox_to_anchor =(0.75,1.13))
            ax = fig.add_axes([0.6,1.08, 0.0, 0.0])

#                         legend_elements = [Line2D([0], [0], color='b', lw=4, label='Line'),
#                            Line2D([0], [0], marker='o', color='w', label='Scatter',
#                                   markerfacecolor='g', markersize=15),
#                            Patch(facecolor='orange', edgecolor='r',
#                                  label='Color Patch')]

        # Create the figure
#             fig, ax = plt.subplots()
#             ax.legend(handles=legend_elements, loc='center')

    
        index +=1
    fig.tight_layout(pad=3.0)
    
    

    plt.savefig("./generated_images/experiment1/exp1_"+"appendix_"+"plot.png",dpi=45,bbox_inches='tight')

