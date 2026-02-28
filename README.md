# Agentic ML Research Lab

A Claude Code-native framework for running the full ML research lifecycle with specialized agents. Claude Code orchestrates the entire process — from problem understanding through literature review, experiment design, training, evaluation, and iteration.

## Quick Start

```bash
# 1. Clone and setup
cd ~/agentic-ml-lab
chmod +x setup.sh && ./setup.sh

# 2. Open in Claude Code and describe your ML problem
# Claude reads CLAUDE.md and runs the 5-phase workflow automatically
```

## Architecture

```
User describes problem
    ↓
Phase 1: Problem Intake ─── interactive interview + compute detection
    ↓
Phase 2: Research Sprint ─── 4 parallel research agents + EDA
    ↓
Phase 3: Plan Refinement ─── devil's advocate + blue sky + user approval
    ↓
Phase 4: Experiments ─────── iterative train → evaluate → adjust loop
    ↓
Phase 5: Analysis ────────── comparison viz + user decision
    ↓
Iterate / Pivot / Done
```

## Agent Roster

| Agent | File | Mode | Role |
|-------|------|------|------|
| Problem Intake | `agents/01-problem-intake.md` | Foreground | Interviews user, detects compute |
| Research Orchestrator | `agents/02-research-orchestrator.md` | Background | Coordinates research sprint |
| Dataset Discovery | `agents/02a-dataset-discovery.md` | Background | Finds relevant datasets |
| Benchmark Search | `agents/02b-benchmark.md` | Background | Finds SOTA and baselines |
| Paper Search | `agents/02c-paper-search.md` | Background | Searches research papers |
| Blog & Material | `agents/02d-blog-material.md` | Background | Finds tutorials and code |
| Plan Refinement | `agents/03-plan-refinement.md` | Foreground | Refines experiment plan with user |
| Experiment Design | `agents/04-experiment-design.md` | Background | Generates YAML run configs |
| Iterator/Evaluator | `agents/05-iterator-evaluator.md` | Background | Runs experiments, detects pathologies |
| Devil's Advocate | `agents/06-devils-advocate.md` | Background | Challenges assumptions |
| Blue Sky | `agents/07-blue-sky.md` | Background | Creative alternative ideas |
| Visualization | `agents/08-visualization.md` | Background | EDA, training, and analysis plots |

## Key Philosophy

1. **Data first** — Always look at the data before modeling
2. **Iteration > initial design** — Simple hyperparameter changes often outperform architectural changes by 10x
3. **Track everything** — MLflow logs every experiment
4. **Challenge assumptions** — Devil's Advocate and Blue Sky agents keep you honest

## File Structure

```
├── CLAUDE.md              # Orchestration brain (read this first)
├── agents/                # 12 agent prompt templates
├── templates/             # 8 document templates
├── utils/                 # Python utilities (MLflow, metrics, viz, config, data, I/O)
├── project/               # Per-project working directory
│   ├── data/              # Datasets
│   ├── configs/           # YAML experiment configs
│   ├── results/           # Experiment outputs
│   ├── visualizations/    # All plots (eda/, training/, analysis/)
│   ├── scripts/           # Generated training scripts
│   └── logs/              # Training logs
└── mlruns/                # MLflow tracking (gitignored)
```

## Requirements

- Python 3.10+
- Claude Code CLI
- Git + GitHub CLI (`gh`)
- See `requirements.txt` for Python dependencies

## MLflow

View experiment tracking UI:
```bash
source venv/bin/activate
mlflow ui --backend-store-uri file:./mlruns
```
