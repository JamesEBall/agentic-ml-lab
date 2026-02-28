# Agentic ML Agent Harness 🧪

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-native-orange.svg)](https://docs.anthropic.com/en/docs/claude-code)

**16 specialized agents that run the full ML research lifecycle** — from "I have a CSV" to "here's what the model learned and why." Built natively in Claude Code. The agents are just markdown prompt templates. No framework, no SDK, no magic.


## Setup

```bash
git clone https://github.com/JamesEBall/agentic-ml-lab.git
cd agentic-ml-lab
chmod +x setup.sh && ./setup.sh
```

Then open in Claude Code and describe your problem. `CLAUDE.md` teaches Claude the workflow.

## How It Works

You describe an ML problem. Claude reads the agent prompts and orchestrates them — some interactively, some in parallel in the background. The whole thing runs through 5 phases:

```
Phase 1: Problem Intake ──── "what are you trying to do? what GPU do you have?"
    ↓
Phase 2: Research Sprint ──── 4 agents search papers/datasets/benchmarks/code in parallel
    ↓                         while the viz agent does EDA on your data
Phase 3: Plan Refinement ──── Devil's Advocate pokes holes. Blue Sky proposes wild ideas.
    ↓                         You approve the plan.
Phase 4: Experiments ──────── Optimization Guard → Model Builder → train → evaluate → adjust
    ↓                         MLflow tracks everything. Git commits after each run.
Phase 5: Analysis ─────────── Bureaucrat audits the stats. Post-Hoc Analyst explains *why*.
    ↓                         You decide: iterate, pivot, or ship.
```

## The Agents

Each agent is a `.md` file in `agents/`. Claude reads the prompt and follows it. You can edit any of them — they're just instructions.

### 🔧 The Workhorses

| Agent | File | What it does |
|-------|------|-------------|
| Problem Intake | `01-problem-intake.md` | Interviews you. Detects your GPU (NVIDIA, MPS, CPU). Writes the problem spec. |
| Research Orchestrator | `02-research-orchestrator.md` | Spawns 4 sub-agents in parallel, synthesizes findings into a research brief. |
| Dataset Discovery | `02a-dataset-discovery.md` | Searches HuggingFace, Kaggle, Papers With Code, UCI for relevant datasets. |
| Benchmark Search | `02b-benchmark.md` | Finds SOTA leaderboards and realistic baseline targets. |
| Paper Search | `02c-paper-search.md` | Finds papers with code, recent surveys, foundational work. |
| Blog & Material | `02d-blog-material.md` | Tutorials, GitHub repos with stars, pretrained models, Kaggle notebooks. |
| Plan Refinement | `03-plan-refinement.md` | Presents research findings, incorporates critique, gets your approval. |
| Experiment Design | `04-experiment-design.md` | Generates YAML configs. One variable at a time. Simplest first. |
| Model Builder | `09-model-builder.md` | Writes correct training scripts from configs. Handles sklearn, PyTorch, XGBoost. |
| Iterator/Evaluator | `05-iterator-evaluator.md` | The engine. Runs experiments, detects pathologies (plateau, collapse, overfitting), decides next steps. |

### 👁️ The Visualization Agent

| Agent | File | What it does |
|-------|------|-------------|
| Visualization | `08-visualization.md` | Runs in **every phase**. ~20 plot types (EDA, training curves, evaluation, cross-run comparison). |

The key difference: this agent **actually looks at every image it generates** (via Claude's vision on the saved PNGs) and writes semantic interpretations. Not "saved correlation_matrix.png" — instead: *"petal_length and petal_width are correlated at r=0.96, suggesting one could be dropped. sepal_width is the most independent feature (r=-0.11 to -0.42)."*

PCA loadings are mandatory. If it does dimensionality reduction, it decomposes what each component means in terms of the original features.

### 🔴 The Critics

These agents exist because unchallenged ML plans waste compute.

| Agent | File | Personality |
|-------|------|------------|
| Devil's Advocate | `06-devils-advocate.md` | Reads your plan and finds everything wrong with it. Data leakage? Wrong metric? Overfitting risk? Tells you before you burn GPU hours. |
| Blue Sky | `07-blue-sky.md` | The opposite energy. "What if a lookup table solves 80% of this?" Ranks ideas by upside/effort ratio. |
| Optimization Guard | `10-optimization-guard.md` | Pre-flight check before every run. Estimates training time, catches insane learning rates, blocks configs over budget. Enforces: *what's the cheapest way to test this hypothesis?* |
| The Bureaucrat | `11-bureaucrat.md` | Deeply, perpetually concerned about statistical validity. "Your 96.7% accuracy has a 95% CI of ±7% on 30 samples. That is NOT 96.7% accuracy." Demands p-values. Tracks cost per % improvement. |
| Post-Hoc Analyst | `12-post-hoc-analyst.md` | Works after the numbers are in. Feature attribution, error clustering in PCA space, model agreement maps, and epistemological reflection — "what do these results actually *prove*?" |

## Lessons from ESTA

Full writeup: [`docs/lessons_from_esta.md`](docs/lessons_from_esta.md) | Original design doc: [`docs/bootstrap_prompt.md`](docs/bootstrap_prompt.md)

These are the critical failure modes discovered during the ESTA playstyle discovery project that the agents now encode:

| Lesson | What Happened | How It Was Fixed |
|--------|--------------|------------------|
| Posterior collapse | free_bits=0.1 let model use 2 of 32 dims while reporting 15/16 "active" | Raised free_bits to 1.0, lowered beta to 0.1 |
| Cyclical annealing | Structure appeared then was destroyed each cycle | Disabled cyclical, used linear warmup only |
| Euclidean on hyperbolic | PCA on Lorentz spatial coords = mathematical error | Must use tangent-space PCA via logarithmic map |
| Map confound (20.3% R^2) | Clusters were separating maps, not playstyles | Always regress latent space against potential confounds |
| Continuous not discrete | No discrete playstyle clusters exist after removing confounds | Switch from cluster metrics to manifold metrics |
| Player consistency 0.949 | Players vary almost as much within as between each other | Round-level identity signal is near zero |
| Misleading silhouette | Positive score measured map separation, not playstyle | Color UMAP by confounds to audit what silhouette measures |
| TC on MPS (50-80s/batch) | alpha-TCVAE O(B^2*D) computation hung on Apple Silicon | Switch to proxy method (off-diagonal covariance) |
| Misleading active dims | Threshold count included dims at free_bits floor | Visualize per-dim KL distribution, not scalar count |
| Simple beats complex | beta change = 10x improvement; hyperbolic VAE = marginal | Always test boring baselines before novel architecture |
| No upfront criteria | Moved goalposts after seeing results | Define falsifiable success criteria before training |
| Slow data preprocessing | LZMA decompression took minutes per batch of demo files | Profile loading first, convert to Parquet/HDF5, cache it |
| Null data crashes | Null players list in demo files crashed mid-pipeline | Defensive null checks on all external data, skip bad records |
| Wrong compute target | Agents ran training locally instead of on the Mac Mini | problem_spec.md compute section is law — always check it |

## Architecture

```
CLAUDE.md              <- The brain. 5-phase workflow, agent spawning patterns, MLflow conventions.
agents/                <- 16 agent prompt templates (.md files)
templates/             <- 8 structured output templates (problem_spec, research_brief, experiment_plan, etc.)
utils/
|-- mlflow_helper.py   <- init, start_run, log_metrics/params/artifacts, compare_runs, get_best_run
|-- metrics.py         <- 15 metrics: accuracy, F1, AUC, RMSE, MAE, R^2, MAPE, MCC, NDCG, ...
|-- viz.py             <- ~20 plot functions (distributions, correlation, training curves, confusion matrix, ...)
|-- config.py          <- YAML load/save/merge/validate/diff
|-- data_loader.py     <- CSV, Parquet, JSON, Excel, HuggingFace datasets, auto-detection, train/val/test split
|-- file_io.py         <- Status updates (append-only log), project directory management
docs/
|-- bootstrap_prompt.md    <- Original design document from the ESTA project
|-- lessons_from_esta.md   <- 11 critical lessons with detection signals and fixes
project/               <- Working directory: data/, configs/, results/, visualizations/, scripts/, research/
mlruns/                <- MLflow tracking store (gitignored)
```

Agents communicate through files in `project/`. Status updates go to `project/status.md` (append-only). Configs are YAML. Visualizations land in `project/visualizations/{eda,training,analysis}/`.

## Validated End-to-End

Smoke-tested with Iris classification (yes, overkill — that's the point):

```
Phase 1  Problem spec + M1 Pro MPS detection          ✓
Phase 2  7 EDA visualizations + research brief         ✓
Phase 3  Experiment plan (4 models)                    ✓
Phase 4  4 runs, MLflow tracking, per-run confusion matrices
         ├─ Logistic Regression   96.7% accuracy       ✓
         ├─ Random Forest         90.0%                ✓
         ├─ SVM (RBF)            96.7%                 ✓
         └─ KNN                  100.0%                ✓
Phase 5  Comparison chart + iteration report            ✓
```

## MLflow

```bash
source venv/bin/activate
mlflow ui --backend-store-uri file:./mlruns
# → http://localhost:5000
```

## Requirements

- Python 3.10+
- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code)
- Git + GitHub CLI (`gh`)
- See `requirements.txt` (torch, sklearn, mlflow, matplotlib, seaborn, plotly, datasets, omegaconf, ...)

## Contributing

The agents are just markdown. Fork, edit a prompt, see what happens. If your Bureaucrat is too aggressive or your Blue Sky agent isn't creative enough, tune them like hyperparameters — that's the whole point.
