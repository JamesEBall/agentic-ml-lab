# Agentic ML Research Lab

A Claude Code-native framework for running the full ML research lifecycle with specialized agents. Claude Code orchestrates the entire process — from problem understanding through literature review, experiment design, training, evaluation, and iteration.

Born from a key insight: **simple hyperparameter changes (beta 1.0→0.1, free_bits 0.1→1.0) had 10x more impact than complex architectural changes.** The iteration loop matters more than the initial design.

## Quick Start

```bash
# 1. Clone and setup
git clone https://github.com/JamesEBall/agentic-ml-lab.git
cd agentic-ml-lab
chmod +x setup.sh && ./setup.sh

# 2. Open in Claude Code and describe your ML problem
# Claude reads CLAUDE.md and runs the 5-phase workflow automatically
```

## Architecture

```
User describes problem
    ↓
Phase 1: Problem Intake ──── interactive interview + compute detection
    ↓
Phase 2: Research Sprint ──── 4 parallel research agents + EDA
    ↓
Phase 3: Plan Refinement ──── devil's advocate + blue sky + bureaucrat + user approval
    ↓
Phase 4: Experiments ──────── optimization guard → model builder → train → evaluate → adjust
    ↓
Phase 5: Analysis ─────────── statistical audit + comparison viz + user decision
    ↓
Iterate / Pivot / Done
```

## Agent Roster (16 agents)

| Agent | File | Mode | Role |
|-------|------|------|------|
| Problem Intake | `01-problem-intake.md` | Foreground | Interviews user, detects compute environment |
| Research Orchestrator | `02-research-orchestrator.md` | Background | Coordinates 4 parallel research sub-agents |
| Dataset Discovery | `02a-dataset-discovery.md` | Background | Finds relevant datasets across HF, Kaggle, etc. |
| Benchmark Search | `02b-benchmark.md` | Background | Finds SOTA benchmarks and baselines |
| Paper Search | `02c-paper-search.md` | Background | Searches and synthesizes relevant papers |
| Blog & Material | `02d-blog-material.md` | Background | Finds tutorials, code repos, pretrained models |
| Plan Refinement | `03-plan-refinement.md` | Foreground | Refines experiment plan interactively with user |
| Experiment Design | `04-experiment-design.md` | Background | Generates concrete YAML run configs |
| Iterator/Evaluator | `05-iterator-evaluator.md` | Background | Core engine: runs experiments, detects pathologies, decides next steps |
| Devil's Advocate | `06-devils-advocate.md` | Background | Challenges assumptions, finds weaknesses |
| Blue Sky | `07-blue-sky.md` | Background | Proposes creative alternative approaches |
| Visualization | `08-visualization.md` | Background | EDA, training curves, cross-run comparison — **views and interprets every image** |
| Model Builder | `09-model-builder.md` | Background | Translates configs into correct, runnable training code |
| Optimization Guard | `10-optimization-guard.md` | Background | Pre-flight: estimates time, catches bad configs, enforces budgets |
| The Bureaucrat | `11-bureaucrat.md` | Background | Audits statistical rigor, computes confidence intervals, tracks costs |
| Post-Hoc Analyst | `12-post-hoc-analyst.md` | Background | Deep interpretive analysis — feature attribution, error clustering, epistemological reflection |

## Key Philosophy

1. **Data first** — Always look at the data before modeling
2. **Iteration > initial design** — Simple hyperparameter changes often outperform architectural changes by 10x
3. **Track everything** — MLflow logs every experiment
4. **Challenge assumptions** — Devil's Advocate and Blue Sky agents keep you honest
5. **Don't waste compute** — Optimization Guard reviews configs before execution
6. **Statistical rigor** — The Bureaucrat demands confidence intervals and significance tests
7. **See the data** — Every plot is viewed and interpreted semantically, not just saved to disk
8. **Understand why** — Post-Hoc Analyst decomposes results mathematically and reflects epistemologically

## Validated End-to-End

This framework has been tested with an Iris classifier benchmark:

```
Phase 1: Problem spec + M1 Pro compute detection     ✓
Phase 2: 7 EDA plots + research brief                ✓
Phase 3: Experiment plan (4 models)                   ✓
Phase 4: All 4 runs with MLflow tracking              ✓
         - Logistic Regression: 96.7% accuracy
         - Random Forest: 90.0% accuracy
         - SVM (RBF): 96.7% accuracy
         - KNN: 100.0% accuracy
Phase 5: Comparison visualization + iteration report  ✓
```

## File Structure

```
├── CLAUDE.md              # Orchestration brain — defines the 5-phase workflow
├── agents/                # 16 agent prompt templates (.md files)
├── templates/             # 8 document templates for structured agent output
├── utils/                 # Python utilities
│   ├── mlflow_helper.py   #   MLflow tracking (init, log, compare)
│   ├── metrics.py         #   15 metrics (classification, regression, ranking)
│   ├── viz.py             #   ~20 plot functions (EDA, training, evaluation)
│   ├── config.py          #   YAML config load/save/merge/validate
│   ├── data_loader.py     #   Multi-format loading + train/test splitting
│   └── file_io.py         #   Status updates + project directory management
├── project/               # Per-project working directory
│   ├── data/              # Datasets
│   ├── configs/           # YAML experiment configs
│   ├── results/           # Per-run result reports
│   ├── visualizations/    # All plots (eda/, training/, analysis/)
│   ├── scripts/           # Generated training scripts
│   └── research/          # Research sub-agent outputs
└── mlruns/                # MLflow tracking store (gitignored)
```

## Requirements

- Python 3.10+
- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code)
- Git + GitHub CLI (`gh`)

## MLflow

View the experiment tracking UI:
```bash
source venv/bin/activate
mlflow ui --backend-store-uri file:./mlruns
# Open http://localhost:5000
```
