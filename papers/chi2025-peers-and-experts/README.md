# AI-based Credibility Indicators, Peers, and Experts

**Understanding the Effects of AI-based Credibility Indicators When People Are Influenced By Both Peers and Experts**<br>
Zhuoran Lu, Patrick Li, Weilong Wang, and Ming Yin. CHI 2025.

[Paper / DOI](https://doi.org/10.1145/3706598.3713871) · [Author PDF](https://mingyin.org/paper/CHI-25/misinfo_expert.pdf) · [Supplementary material](https://mingyin.org/paper/CHI-25/misinfo_expert_supp.pdf)

## Run

Download this entire directory. With Python and R installed, run:

```bash
./run.command
```

On macOS, you can also double-click `run.command`. It installs pinned Python dependencies in `.venv/`, checks the input files, and runs all three experiments and the R models. Tested with Python 3.13 and R 4.2.1. A full run takes several minutes.

Outputs are generated locally in `results/`: statistical tables, bootstrap summaries and draws, model coefficients, figures, and logs. `results/RUN_COMPLETE.json` records successful completion. Generated results are not committed to the repository.

Use `./run.command --check` to check dependencies and file integrity without running the analysis.

## Data

[`data/clean_trials.csv`](data/clean_trials.csv) is the primary dataset: one row per participant and formal Phase 2 task.

| Experiment | Participants | Formal task records | Treatment groups |
| --- | ---: | ---: | --- |
| 1 | 201 | 3,216 | No AI: 92; AI: 109 |
| 2 | 208 | 3,328 | No AI: 106; AI: 102 |
| 3 | 373 | 5,968 | No AI: 127; high-accuracy AI: 123; low-accuracy AI: 123 |
| **Total** | **782** | **12,512** | |

Participant identifiers are replaced with consistent aliases. `workerId` and `participant_id` use the same alias in the combined dataset; no mapping to original identifiers is published. All other observations, labels, treatment assignments, sample membership, and row order are retained.

[`data/data_dictionary.csv`](data/data_dictionary.csv) describes the fields. The additional CSVs supply the coded surveys, placebo-inclusive tasks, and model-specific inputs required by the analysis. Keep them together with the primary dataset.

## Files

- `data/`: anonymized data and field definitions.
- `analysis.py` and `analysis.R`: analysis entry points.
- `analysis_code/`: statistical functions and analysis blocks used by the entry points.
- `run.command`: one-command runner.
- `requirements-lock.txt`: pinned Python dependencies.
- `package_check.py` and `INPUT_CHECKSUMS.json`: input integrity and completion checks.

The original analysis logic, statistical functions, and model choices are retained. Original seed settings are retained as well; participant-level bootstrap draws can depend on identifier ordering and the Python environment. Effect sizes are printed by their original calls in `results/exp*_log.txt`; `results/t_tests.csv` records t-tests.

## Citation

Lu, Z., Li, P., Wang, W., & Yin, M. (2025). Understanding the Effects of AI-based Credibility Indicators When People Are Influenced By Both Peers and Experts. *Proceedings of the 2025 CHI Conference on Human Factors in Computing Systems*. https://doi.org/10.1145/3706598.3713871
