# Misinformation

This is a repository for the data and analysis code for a series of works in AI & misinformation, including: 

The Effects of AI-based Credibility Indicators on the Detection and Spread of Misinformation under Social Influence. <br>
Zhuoran Lu, Patrick Li, Weilong Wang, and Ming Yin. <br>
The 25th ACM Conference on Computer-Supported Cooperative Work and Social Computing (CSCW), Online, November 2022 <br>

Understanding the Effects of AI-based Credibility Indicators When People Are Influenced By Both Peers and Experts. [in preparation] <br>
Zhuoran Lu, Patrick Li, Weilong Wang, and Ming Yin. <br>
The 43rd ACM Conference on Human Factors in Computing Systems (CHI), Yokohama, May 2025. <br>

Large Language Model (LLM)-driven Adversarial Social Influences in Online Information Spread: Risks and Interventions. [in preparation] <br>
Zhuoran Lu*, Gionnieve Lim*, and Ming Yin. <br>
The 44th ACM Conference on Human Factors in Computing Systems (CHI), Barcelona, May 2026. <br>


## Repository Structure

### 3 Data Files: 

Individual level data for Experiment 1: experimentOneIndividualLevelRes.csv

Individual level data of subjects' decisions under social influence in Experiment 2 : experimentTwoWithInfluenceIndividualLevelRes.csv

Individual level data of subjects' decisions with no social influence in Experiment 2 : experimentTwoNoInfluenceIndividualLevelRes.csv

#### Interpretation

* `treatment` Int. The treatment of each subject assigned in each experiment. `0`: control treatment (no AI), `1`: AI was presented before subjects independently processed the information. (AI-before), `2`: AI was presented after subjects independently processed the information. (AI after),
* `workerId` Int. The unique ID for each subject assigned in each experiment.
* `finalCorrectness` Bool. Whether the final decision of the subject on the veracity of this news was correct or not.
* `mlCorrectness` Bool. Whether the AI model's prediction on the veracity of this news was correct or not.




### A Descriptive Analysis

descriptiveStatistics.ipynb

## 

Fully cleaned analysis will be updated soon. This is a preliminary version of the repository.

## Licensing & Citing

When using or building upon the data in an academic publication, please consider citing as follows:

Lu, Z., Li, P., Wang, W., & Yin, M. (2022). The Effects of AI-based Credibility Indicators on the Detection and Spread of Misinformation under Social Influence. Proceedings of the ACM on Human-Computer Interaction, 6(CSCW2), 1-27.

https://doi.org/10.1145/3555562
