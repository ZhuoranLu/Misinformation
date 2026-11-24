# Human–AI Interaction and Misinformation

Data and analysis code for a series of papers on how AI and social influence affect people's detection and sharing of misinformation. Each paper has its own directory, data documentation, analysis files, and citation.

## Papers and datasets

| Paper | Venue | Materials in this repository |
| --- | --- | --- |
| [The Effects of AI-based Credibility Indicators on the Detection and Spread of Misinformation under Social Influence](papers/cscw2022-credibility-indicators/) | CSCW 2022 | Three original data files and the descriptive-analysis notebook |
| [Understanding the Effects of AI-based Credibility Indicators When People Are Influenced By Both Peers and Experts](papers/chi2025-peers-and-experts/) | CHI 2025 | Participant-pseudonymized data for three experiments, original analysis code, and a one-command runner |
| [Large Language Model (LLM)-driven Adversarial Social Influences in Online Information Spread: Risks and Interventions](papers/chi2026-adversarial-social-influence/) | CHI 2026 | Publication and citation; data and analysis are not yet included |
| [One AI Signal, Many Human Judgments: A Bayesian Cascade Analysis of AI-based Credibility Indicators in Online Information Spread](papers/hcomp2026-bayesian-cascade/) | HCOMP 2026 | Publication and citation; data and analysis are not yet included |

## Organization

```text
papers/
├── cscw2022-credibility-indicators/
│   ├── README.md
│   ├── descriptiveStatistics.ipynb
│   └── experiment*.csv
├── chi2025-peers-and-experts/
│   ├── README.md
│   ├── data/
│   ├── run.command
│   ├── analysis.py
│   ├── analysis.R
│   └── analysis_code/
├── chi2026-adversarial-social-influence/
│   └── README.md
└── hcomp2026-bayesian-cascade/
    └── README.md
papers.json
references.bib
```

The CSCW 2022 data files and notebook previously at the repository root have moved together into `papers/cscw2022-credibility-indicators/`. Their contents and filenames are unchanged, including the notebook's relative data paths.

## Run the CHI 2025 analysis

Download or clone the **whole repository**, then run:

```bash
./papers/chi2025-peers-and-experts/run.command
```

On macOS, you can also double-click that `run.command` file. Python and R are required; the runner installs the pinned Python dependencies in a local virtual environment. Results are written into that paper's `results/` directory. See the [paper-specific instructions](papers/chi2025-peers-and-experts/README.md) for data definitions and the tested environment.

## Cite the relevant paper

Please cite the paper associated with the data you use. Each paper directory includes its citation, and [references.bib](references.bib) contains all four entries. [papers.json](papers.json) provides a machine-readable index of titles, DOIs, directories, and material availability.

## Adding another paper

Add a directory under `papers/` named for its venue, year, and topic. Keep that paper's data, analysis, dependencies, and instructions together; update the index above, `papers.json`, and `references.bib`. State which materials are actually available rather than implying that a publication listing includes a dataset.
