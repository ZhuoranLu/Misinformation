# AI-based Credibility Indicators under Social Influence

**The Effects of AI-based Credibility Indicators on the Detection and Spread of Misinformation under Social Influence**<br>
Zhuoran Lu, Patrick Li, Weilong Wang, and Ming Yin.<br>
*Proceedings of the ACM on Human-Computer Interaction*, 6(CSCW2), 2022.<br>
[Paper / DOI](https://doi.org/10.1145/3555562)

## Included materials

| File | Contents | Rows in the released file |
| --- | --- | ---: |
| `experimentOneIndividualLevelRes.csv` | Experiment 1 individual-level records | 5,278 |
| `experimentTwoWithInfluenceIndividualLevelRes.csv` | Experiment 2 decisions under social influence | 5,453 |
| `experimentTwoNoInfluenceIndividualLevelRes.csv` | Experiment 2 decisions without social influence | 4,463 |
| `descriptiveStatistics.ipynb` | Original descriptive analysis | — |

These are the repository's original public files, moved here without changing their contents. The row counts describe the files, not participant counts or a newly defined analysis sample. This release contains the descriptive notebook, not a newly reconstructed full analysis pipeline.

## Original variable definitions

- `treatment`: `0` = control (no AI); `1` = AI before the participant independently processes the information; `2` = AI after the participant independently processes the information.
- `workerId`: the participant identifier used in the released data.
- `finalCorrectness`: whether the participant's final news-veracity decision was correct.
- `mlCorrectness`: whether the AI prediction was correct.

## Use the notebook

Keep the notebook beside its three CSV files. Open it in Jupyter with this directory as the working directory; its original relative filenames are preserved. Install the libraries imported by the notebook in your Jupyter environment.

## Citation

Lu, Z., Li, P., Wang, W., & Yin, M. (2022). The Effects of AI-based Credibility Indicators on the Detection and Spread of Misinformation under Social Influence. *Proceedings of the ACM on Human-Computer Interaction, 6*(CSCW2), 1–27. https://doi.org/10.1145/3555562
