# %% analysis block 2
def t_test_multi(df,measure,t_con,t_exp):
    print("dep:",measure)
    con = df.query("treatment==@t_con")[measure]
    exp = df.query("treatment==@t_exp")[measure]
    print("con mean, std:",np.round(con.mean(),2),np.round(con.std(),2))
    print("high" if t_exp==1 else "low"," mean, std:",np.round(exp.mean(),2),np.round(exp.std(),2))
    test_res = ttest_ind(con,exp)
    print("t (" ,len(df)-1,") = ",np.round(test_res[0],2)," p = ",np.round(test_res[1],10))
    print("d = ",cohen_d(df,measure,t_con,t_exp,cohen_d_helper))
    #     print("kruskal:")
#     print(kruskal(con,exp))
    print(" ")

# %% analysis block 3
def cohen_d(df,measurement,con_treatment,exp_treatment,helper):
    con = df.query("treatment==@con_treatment")[measurement]
    exp = df.query("treatment==@exp_treatment")[measurement]
    return helper(con,exp)

def cohen_d_helper(con,exp):
    std_pooled = ((np.std(con)**2+np.std(exp)**2)/2)**(0.5)
    return np.abs(np.mean(con)-np.mean(exp))/std_pooled

def cohen_w_helper(con,exp):
    cohen_w = chisquare_effectsize([np.sum(con), np.sum(con == False)], 
                               [np.sum(exp), np.sum(exp == False)])
    return cohen_w

# %% analysis block 54
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

# %% analysis block 55
def anova_test(df,dep):
    nan_sub = -100
    groups = 3
    print(df.isna().sum().sum())
    print("F("+str(groups-1)+","+str(len(df)-groups)+")")
        
    control = df.replace(np.nan,nan_sub).query("treatment==0").query(dep+"!=@nan_sub")
    high =  df.replace(np.nan,nan_sub).query("treatment==1").query(dep+"!=@nan_sub")
    low =  df.replace(np.nan,nan_sub).query("treatment==2").query(dep+"!=@nan_sub")

    print(len(control)+len(high)+len(low))
    tukey = pairwise_tukeyhsd(endog=df.replace(np.nan,nan_sub).query(dep+"!=@nan_sub")[dep],
                          groups=df.replace(np.nan,nan_sub).query(dep+"!=@nan_sub")['treatment'],
                          alpha=0.05)
    print(f_oneway(control[dep],high[dep],low[dep]))
    print("control",control[dep].mean(),control[dep].std())
    print("high: treatment = 2",high[dep].mean(),high[dep].std())
    print("low: treatment = 2",low[dep].mean(),low[dep].std())

    print(tukey)

# %% analysis block 58
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

res_high_correct = generate_res(valid_predictions_task.query("high_correct==True"))
res_high_incorrect = generate_res(valid_predictions_task.query("high_correct==False"))

res_low_correct = generate_res(valid_predictions_task.query("low_correct==True"))
res_low_incorrect = generate_res(valid_predictions_task.query("low_correct==False"))


res_agree_high_correct = generate_res(valid_predictions_task_agree.query("high_correct==True"))
res_agree_high_incorrect = generate_res(valid_predictions_task_agree.query("high_correct==False"))
res_agree_low_correct = generate_res(valid_predictions_task_agree.query("low_correct==True"))
res_agree_low_incorrect = generate_res(valid_predictions_task_agree.query("low_correct==False"))

res_disagree_high_correct = generate_res(valid_predictions_task_disagree.query("high_correct==True"))
res_disagree_high_incorrect = generate_res(valid_predictions_task_disagree.query("high_correct==False"))
res_disagree_low_correct = generate_res(valid_predictions_task_disagree.query("low_correct==True"))
res_disagree_low_incorrect = generate_res(valid_predictions_task_disagree.query("low_correct==False"))


res_4 = generate_res(valid_predictions_task.query("prev_length==4"))
res_6 = generate_res(valid_predictions_task.query("prev_length==6"))
res_8 = generate_res(valid_predictions_task.query("prev_length==8"))

# %% analysis block 64
t_test_multi(valid_predictions_task.query("high_correct == True"),"selfCorrect",0,1)
cohen_d(valid_predictions_task.query("high_correct == True"),"selfCorrect",0,1,cohen_d_helper)
# t_test_multi(valid_predictions_task.query("high_correct == False"),"selfCorrect",0,1)
# t_test_multi(valid_predictions_task.query("low_correct == True"),"selfCorrect",0,2)
# t_test_multi(valid_predictions_task.query("low_correct == False"),"selfCorrect",0,2)
t_test_multi(res_high_correct,"truth_discernment",0,1)
cohen_d(res_high_correct,"truth_discernment",0,1,cohen_d_helper)

# %% analysis block 65
t_test_multi(valid_predictions_task.query("high_correct == False"),"selfCorrect",0,1)
cohen_d(valid_predictions_task.query("high_correct == False"),"selfCorrect",0,1,cohen_d_helper)

t_test_multi(res_high_incorrect[~res_high_incorrect["truth_discernment"].isna()],"truth_discernment",0,1)
cohen_d(res_high_incorrect[~res_high_incorrect["truth_discernment"].isna()],"truth_discernment",0,1,cohen_d_helper)

# %% analysis block 66
t_test_multi(valid_predictions_task.query("high_correct == False and label==1"),"finalWill",0,1)
cohen_d(valid_predictions_task.query("high_correct == False and label==1"),"finalWill",0,1,cohen_d_helper)

# %% analysis block 67
t_test_multi(valid_predictions_task.query("low_correct == False"),"selfCorrect",0,2)
cohen_d(valid_predictions_task.query("low_correct == False"),"selfCorrect",0,2,cohen_d_helper)

t_test_multi(res_low_incorrect[~res_low_incorrect["truth_discernment"].isna()],"truth_discernment",0,2)
cohen_d(res_low_incorrect[~res_low_incorrect["truth_discernment"].isna()],"truth_discernment",0,2,cohen_d_helper)

# %% analysis block 68
t_test_multi(valid_predictions_task.query("low_correct == True"),"selfCorrect",0,2)
cohen_d(valid_predictions_task.query("low_correct == True"),"selfCorrect",0,2,cohen_d_helper)

t_test_multi(res_low_correct[~res_low_correct["truth_discernment"].isna()],"truth_discernment",0,2)
cohen_d(res_low_correct[~res_low_correct["truth_discernment"].isna()],"truth_discernment",0,2,cohen_d_helper)

# %% analysis block 69
t_test_multi(res_low_correct[~res_low_correct["truth_discernment"].isna()],"truth_discernment",0,2)
cohen_d(res_low_correct[~res_low_correct["truth_discernment"].isna()],"truth_discernment",0,2,cohen_d_helper)
t_test_multi(res_low_incorrect[~res_low_incorrect["willingness_discernment"].isna()],"willingness_discernment",0,2)
cohen_d(res_low_incorrect[~res_low_incorrect["willingness_discernment"].isna()],"willingness_discernment",0,2,cohen_d_helper)

# %% analysis block 71
t_test_multi(valid_predictions_task.query("high_correct == True and label==1"),"finalWill",0,1)
t_test_multi(valid_predictions_task.query("high_correct == False and label==1"),"finalWill",0,1)
t_test_multi(valid_predictions_task.query("high_correct == True and label==0"),"finalWill",0,1)
t_test_multi(valid_predictions_task.query("high_correct == False  and label==0"),"finalWill",0,1)

# %% analysis block 79
t_test_multi(valid_predictions_task.query("low_correct == True and label==1"),"finalWill",0,2)
t_test_multi(valid_predictions_task.query("low_correct == False  and label==1"),"finalWill",0,2)
t_test_multi(valid_predictions_task.query("low_correct == True  and label==0"),"finalWill",0,2)
t_test_multi(valid_predictions_task.query("low_correct == False  and label==0"),"finalWill",0,2)

# %% analysis block 80
t_test_multi(res_high_correct[~res_high_correct["truth_discernment"].isna()],"truth_discernment",0,1)
t_test_multi(res_high_incorrect[~res_high_incorrect["truth_discernment"].isna()],"truth_discernment",0,1)
t_test_multi(res_low_correct[~res_low_correct["truth_discernment"].isna()],"truth_discernment",0,2)
t_test_multi(res_low_incorrect[~res_low_incorrect["truth_discernment"].isna()],"truth_discernment",0,2)

# %% analysis block 82
t_test_multi(res_high_correct[~res_high_correct["willingness_discernment"].isna()],"willingness_discernment",0,1)
t_test_multi(res_high_incorrect[~res_high_incorrect["willingness_discernment"].isna()],"willingness_discernment",0,1)
t_test_multi(res_low_correct[~res_low_correct["willingness_discernment"].isna()],"willingness_discernment",0,2)
t_test_multi(res_low_incorrect[~res_low_incorrect["willingness_discernment"].isna()],"willingness_discernment",0,2)

# %% analysis block 118
anova_test(valid_predictions_task,"selfCorrect")

# %% analysis block 120
anova_test(valid_predictions_task,"selfCorrect")
anova_test(res,"truth_discernment")
cohen_d(valid_predictions_task,"selfCorrect",0,1,cohen_d_helper)
cohen_d(res,"truth_discernment",0,1,cohen_d_helper)

cohen_d(valid_predictions_task,"selfCorrect",1,2,cohen_d_helper)
cohen_d(res,"truth_discernment",1,2,cohen_d_helper)

# %% analysis block 123
def vis_df_generate():
    accuracy_df = valid_predictions_task[["treatment","selfCorrect"]]
    willingness_real_df = valid_predictions_task.query("label==1")[["treatment","finalWill"]]
    willingness_fake_df = valid_predictions_task.query("label==0")[["treatment","finalWill"]]
    truth_discernment_df = res[["treatment","truth_discernment"]]
    willingness_discernment_df = res[["treatment","willingness_discernment"]]
    return [accuracy_df,truth_discernment_df,willingness_real_df,willingness_fake_df,willingness_discernment_df]
def bar_vis_rq2_high():
    import matplotlib as mpl
    
    correct_accuracy_df = valid_predictions_task.query("high_correct == True")[["treatment","selfCorrect"]]
    correct_willingness_real_df = valid_predictions_task.query("high_correct == True").query("label==1")[["treatment","finalWill"]]
    correct_willingness_fake_df = valid_predictions_task.query("high_correct== True").query("label==0")[["treatment","finalWill"]]
    correct_truth_discernment_df = res_high_correct[["treatment","truth_discernment"]]
    correct_willingness_discernment_df = res_high_correct[["treatment","willingness_discernment"]]
    
    correct_truth_discernment_df = correct_truth_discernment_df[~correct_truth_discernment_df["truth_discernment"].isna()]
    correct_willingness_discernment_df = correct_willingness_discernment_df[~correct_willingness_discernment_df["willingness_discernment"].isna()]
    
    correct_df_list = [correct_accuracy_df,correct_truth_discernment_df,correct_willingness_real_df,correct_willingness_fake_df,correct_willingness_discernment_df]

    incorrect_accuracy_df = valid_predictions_task.query("high_correct==False")[["treatment","selfCorrect"]]
    incorrect_willingness_real_df = valid_predictions_task.query("high_correct==False").query("label==1")[["treatment","finalWill"]]
    incorrect_willingness_fake_df = valid_predictions_task.query("high_correct==False").query("label==0")[["treatment","finalWill"]]
    incorrect_truth_discernment_df = res_high_incorrect[["treatment","truth_discernment"]]
    incorrect_willingness_discernment_df = res_high_incorrect[["treatment","willingness_discernment"]]
    
    incorrect_truth_discernment_df = incorrect_truth_discernment_df[~incorrect_truth_discernment_df["truth_discernment"].isna()]
    incorrect_willingness_discernment_df = incorrect_willingness_discernment_df[~incorrect_willingness_discernment_df["willingness_discernment"].isna()]
    
    
    incorrect_df_list = [incorrect_accuracy_df,incorrect_truth_discernment_df,incorrect_willingness_real_df,incorrect_willingness_fake_df,incorrect_willingness_discernment_df]
    
    df_mat = [correct_df_list,incorrect_df_list]
    
    font = font_manager.FontProperties(family='calibri',weight='bold',style='normal', size=80)

#     df_list = vis_df_generate()
# figsize=(14,12)
    dep_number = 5
    fig, axs = plt.subplots(1,dep_number,figsize=(80,12))
    dep_list = ["selfCorrect","truth_discernment","finalWill","finalWill","willingness_discernment"]
    y_label_list = ["Accuracy","Truth Discernment","Sharing Intention: Real","Sharing Intention: Fake","Sharing Discernment"]
    ylim_list = [[0.0,0.75],[-0.5,0.45],[4.5,5.8],[4.5,5.8],[-0.4,0.45]]
    hatch_list = ('', '/', '\\')
    mpl.rcParams['hatch.linewidth'] = 7
    mpl.rcParams['hatch.color'] = "white"
    color_list = ["#2A9C9D","#ffa600","gray"]
    font_size = 80
    index = 0
    width = 0.8
    treatment_list = ["No AI","High Accuracy AI"]
    for ax in axs.flat:
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_xlabel(y_label_list[index],fontsize=font_size,fontname="calibri",weight="heavy")
    #     ax.set_yticklabels(fontsize=45)
    #     ax.set_yticks(x-0.2)
        ax.tick_params(axis='x', which='minor', labelsize=10)

        dep_var = dep_list[index]
        for condition in [0,1]:
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
            x = np.array([0,0.35])  # the label locations
            ax.set_yticks(x)
            ax.set_yticklabels(["AI\nCorrect","AI\nIncorrect"],{"fontsize":font_size})
    #         ax.set_yticklabels(["experimental"],{"fontsize":45})
#             plt.legend(prop=font,ncol=3,bbox_to_anchor=(0.0, 1.1, 0.1, 0.2))
    #         ax.bar(df_list[index]["treatment"], )
        if index==2:
            handles, labels = ax.get_legend_handles_labels()
            fig.legend(handles, labels, prop=font,ncol=2,bbox_to_anchor =(0.6,1.08))
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
    fig.tight_layout(pad=6.0)
#     plt.savefig("./generated_images_230826//experiment3/exp3_high_plot.png",dpi=45,bbox_inches='tight')


    
    

#     plt.savefig("./generated_images/experiment1/exp1_"+"rq2_"+"plot.png",dpi=45,bbox_inches='tight')
bar_vis_rq2_high()

# %% analysis block 127
def bar_vis_rq2_low():
    import matplotlib as mpl
    
    correct_accuracy_df = valid_predictions_task_agree.query("low_correct == True")[["treatment","selfCorrect"]]
    correct_willingness_real_df = valid_predictions_task.query("low_correct == True").query("label==1")[["treatment","finalWill"]]
    correct_willingness_fake_df = valid_predictions_task.query("low_correct== True").query("label==0")[["treatment","finalWill"]]
    correct_truth_discernment_df = res_low_correct[["treatment","truth_discernment"]]
    correct_willingness_discernment_df = res_low_correct[["treatment","willingness_discernment"]]
    
    correct_truth_discernment_df = correct_truth_discernment_df[~correct_truth_discernment_df["truth_discernment"].isna()]
    correct_willingness_discernment_df = correct_willingness_discernment_df[~correct_willingness_discernment_df["willingness_discernment"].isna()]
    
    correct_df_list = [correct_accuracy_df,correct_truth_discernment_df,correct_willingness_real_df,correct_willingness_fake_df,correct_willingness_discernment_df]

    incorrect_accuracy_df = valid_predictions_task.query("low_correct==False")[["treatment","selfCorrect"]]
    incorrect_willingness_real_df = valid_predictions_task.query("low_correct==False").query("label==1")[["treatment","finalWill"]]
    incorrect_willingness_fake_df = valid_predictions_task.query("low_correct==False").query("label==0")[["treatment","finalWill"]]
    incorrect_truth_discernment_df = res_low_incorrect[["treatment","truth_discernment"]]
    incorrect_willingness_discernment_df = res_low_incorrect[["treatment","willingness_discernment"]]
    
    incorrect_truth_discernment_df = incorrect_truth_discernment_df[~incorrect_truth_discernment_df["truth_discernment"].isna()]
    incorrect_willingness_discernment_df = incorrect_willingness_discernment_df[~incorrect_willingness_discernment_df["willingness_discernment"].isna()]
    
    
    incorrect_df_list = [incorrect_accuracy_df,incorrect_truth_discernment_df,incorrect_willingness_real_df,incorrect_willingness_fake_df,incorrect_willingness_discernment_df]
    
    df_mat = [correct_df_list,incorrect_df_list]
    
    font = font_manager.FontProperties(family='calibri',weight='bold',style='normal', size=80)

#     df_list = vis_df_generate()
# figsize=(14,12)
    dep_number = 5
    fig, axs = plt.subplots(1,dep_number,figsize=(80,12))
    dep_list = ["selfCorrect","truth_discernment","finalWill","finalWill","willingness_discernment"]
    y_label_list = ["Accuracy","Truth Discernment","Sharing Intention: Real","Sharing Intention: Fake","Sharing Discernment"]
    ylim_list = [[0.2,0.8],[-0.5,0.5],[4.5,5.8],[4.5,5.8],[-0.4,0.45]]
    hatch_list = ('', '/', '\\')
    mpl.rcParams['hatch.linewidth'] = 7
    mpl.rcParams['hatch.color'] = "white"
    color_list = ["#2A9C9D","#ffa600","gray"]
    font_size = 80
    index = 0
    width = 0.8
    treatment_list = ["No AI","Low Accuracy AI"]
    for ax in axs.flat:
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_xlabel(y_label_list[index],fontsize=font_size,fontname="calibri",weight="heavy")
    #     ax.set_yticklabels(fontsize=45)
    #     ax.set_yticks(x-0.2)
        ax.tick_params(axis='x', which='minor', labelsize=10)

        dep_var = dep_list[index]
        for condition in [0,1]:
            df_list = df_mat[condition]
            for treatment in [0,1]:
                loc = treatment*0.1 + condition*0.3
                ai_treatment = 0 if treatment ==0 else 2
                dep = df_list[index].query("treatment==@ai_treatment")[dep_var]
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
            x = np.array([0,0.35])  # the label locations
            ax.set_yticks(x)
            ax.set_yticklabels(["AI\nCorrect","AI\nIncorrect"],{"fontsize":font_size})
    #         ax.set_yticklabels(["experimental"],{"fontsize":45})
#             plt.legend(prop=font,ncol=3,bbox_to_anchor=(0.0, 1.1, 0.1, 0.2))
    #         ax.bar(df_list[index]["treatment"], )
        if index==2:
            handles, labels = ax.get_legend_handles_labels()
            fig.legend(handles, labels, prop=font,ncol=2,bbox_to_anchor =(0.6,1.08))
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
    fig.tight_layout(pad=6.0)
#     plt.savefig("./generated_images_230826//experiment3/exp3_low_plot.png",dpi=45,bbox_inches='tight')

bar_vis_rq2_low()

# %% analysis block 306
from matplotlib.transforms import Bbox

def full_extent(ax, pad=0.0):
    """Get the full extent of an axes, including axes labels, tick labels, and
    titles."""
    # For text objects, we need to draw the figure first, otherwise the extents
    # are undefined.
    ax.figure.canvas.draw()
    items = ax.get_xticklabels() + ax.get_yticklabels() 
#    items += [ax, ax.title, ax.xaxis.label, ax.yaxis.label]
    items += [ax, ax.title]
    bbox = Bbox.union([item.get_window_extent() for item in items])

    return bbox.expanded(1.0 + pad, 1.0 + pad)

def vis_df_generate():
    accuracy_df = valid_predictions_task[["treatment","selfCorrect"]]
    willingness_real_df = valid_predictions_task.query("label==1")[["treatment","finalWill"]]
    willingness_fake_df = valid_predictions_task.query("label==0")[["treatment","finalWill"]]
    truth_discernment_df = res[["treatment","truth_discernment"]]
    willingness_discernment_df = res[["treatment","willingness_discernment"]]
    return [accuracy_df,truth_discernment_df,willingness_real_df,willingness_fake_df,willingness_discernment_df]

def bar_vis_rq4():
    import matplotlib as mpl

    df_list = vis_df_generate()
# figsize=(14,12)
    dep_number = 5
    fig, axs = plt.subplots(1,dep_number,figsize=(90,10))
    dep_list = ["selfCorrect","truth_discernment","finalWill","finalWill","willingness_discernment"]
    y_label_list = ["(a) Accuracy","(b) Truth Discernment","(c) Sharing Intention: Real","(d) Sharing Intention: Fake","(e) Sharing Discernment"]
    ylim_list = [[0.4,0.7],[-0.1,0.29],[5.2,5.55],[5.2,5.55],[-0.05,0.2]]
    hatch_list = ('', '/', '\\')
    mpl.rcParams['hatch.linewidth'] = 7
    mpl.rcParams['hatch.color'] = "white"
    color_list = ["#2A9C9D","#ffa600","gray"]
    font_size = 80
    index = 0
    width = 0.8
    treatment_list = ("Control","Experimental")
    for ax in axs.flat:
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_xlabel(y_label_list[index],fontsize=font_size-4,fontname="calibri",weight="heavy")
    #     ax.set_yticklabels(fontsize=45)
    #     ax.set_yticks(x-0.2)
        ax.tick_params(axis='x', which='minor', labelsize=10)

        dep_var = dep_list[index]
        for treatment in [0,1,2]:
            loc = treatment*0.1
            dep = df_list[index].query("treatment==@treatment")[dep_var]
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
            x = np.array([0,0.1,0.2])  # the label locations
            ax.set_yticks(x)
            ax.set_yticklabels(["No AI","High Accuracy AI","Low Accuracy AI"],{"fontsize":font_size})
    #         ax.set_yticklabels(["experimental"],{"fontsize":45})
        extent = full_extent(ax).transformed(fig.dpi_scale_trans.inverted())
        # Alternatively,
        # extent = ax.get_tightbbox(fig.canvas.renderer).transformed(fig.dpi_scale_trans.inverted())    
#         fig.savefig("./generated_images/experiment1/exp1_"+"rq1"+str(index)+"plot.png",dpi=45, bbox_inches=extent)
    #         ax.bar(df_list[index]["treatment"], )
        index +=1
    fig.tight_layout(pad=6.0)
    plt.subplots_adjust(wspace=0.2, hspace=0)

    plt.savefig("./generated_images_230826/experiment3/exp4_"+"rq4_"+"plot.png",dpi=45)
bar_vis_rq4()

