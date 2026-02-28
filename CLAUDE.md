# Agentic ML Research Lab — Orchestration Guide

You are operating inside the **Agentic ML Research Lab**, a Claude Code-native framework for running the full ML research lifecycle. This file defines how you orchestrate agents, track experiments, and communicate results.

## Core Philosophy

1. **Data first** — Always look at the data before modeling. The Visualization Agent runs in every phase.
2. **Iteration > initial design** — Simple hyperparameter changes often have 10x more impact than architectural changes. The loop matters more than the plan.
3. **Track everything** — Every experiment goes through MLflow. Every result gets committed to git.
4. **Challenge assumptions** — Devil's Advocate and Blue Sky agents exist for a reason. Use them.

## Directory Layout

```
agents/          # Agent prompt templates (read these, spawn via Agent tool)
templates/       # Document templates agents fill in → project/
utils/           # Python utilities for MLflow, metrics, viz, config, data, file I/O
project/         # Working directory for the current project
  data/          # Datasets
  configs/       # YAML experiment configs
  results/       # Experiment outputs
  visualizations/# All plots and charts
  logs/          # Training logs
mlruns/          # MLflow tracking store (gitignored)
```

## The 5-Phase Workflow

### Phase 1: Problem Intake (Foreground, Interactive)

**Agent:** `agents/01-problem-intake.md`
**Mode:** Foreground (interactive with user)

1. Read `agents/01-problem-intake.md` and follow its instructions
2. Interview the user about their ML problem:
   - What are you trying to predict/generate/classify?
   - What data do you have? Where is it?
   - What metrics matter? What's the success threshold?
   - Any constraints (latency, model size, interpretability)?
3. **Compute environment interview:**
   - "Where will training run?" (local / cloud GPU / Colab / etc.)
   - If local: detect GPU via `nvidia-smi` or `system_profiler SPDisplaysDataType` (Mac)
   - If remote: ask for platform name, research it via web search, ask for SSH/API details
   - Write compute setup instructions into problem_spec.md
4. Fill in `templates/problem_spec.md` → save to `project/problem_spec.md`
5. **Git commit:** `"Phase 1: Problem specification for {project_name}"`
6. **Git push**

### Phase 2: Research Sprint (Background, Parallel)

**Agents:** `agents/02-research-orchestrator.md` + 4 sub-agents + `agents/08-visualization.md`
**Mode:** Background (parallel)

1. Read `agents/02-research-orchestrator.md` and spawn it as a background agent
2. The orchestrator spawns 4 research sub-agents in parallel:
   - `agents/02a-dataset-discovery.md` — Find relevant datasets
   - `agents/02b-benchmark.md` — Find SOTA benchmarks and baselines
   - `agents/02c-paper-search.md` — Search for relevant papers
   - `agents/02d-blog-material.md` — Find blogs, tutorials, code examples
3. **Simultaneously** spawn `agents/08-visualization.md` for EDA:
   - Load the data
   - Generate distribution plots, correlation matrices, sample previews
   - Save all plots to `project/visualizations/eda/`
4. Orchestrator compiles findings into `templates/research_brief.md` → `project/research_brief.md`
5. **Git commit:** `"Phase 2: Research brief and EDA for {project_name}"`
6. **Git push**

### Phase 3: Plan Refinement (Foreground, Interactive)

**Agents:** `agents/03-plan-refinement.md` (foreground) + `agents/06-devils-advocate.md` + `agents/07-blue-sky.md` (background)
**Mode:** Mixed

1. Spawn Devil's Advocate (`agents/06-devils-advocate.md`) in background — reads problem_spec + research_brief, writes critique
2. Spawn Blue Sky (`agents/07-blue-sky.md`) in background — proposes creative alternatives
3. In foreground, run Plan Refinement (`agents/03-plan-refinement.md`):
   - Present research findings to user
   - Show EDA visualizations
   - Present Devil's Advocate critique and Blue Sky ideas when they complete
   - Discuss and iterate on the experiment plan
   - User approves final plan
4. Fill in `templates/experiment_plan.md` → `project/experiment_plan.md`
5. Update `agents/08-visualization.md` with training visualization plan
6. **Git commit:** `"Phase 3: Experiment plan for {project_name}"`
7. **Git push**

### Phase 4: Experiment Execution (Background, Iterative)

**Agents:** `agents/04-experiment-design.md` + `agents/05-iterator-evaluator.md` + `agents/08-visualization.md`
**Mode:** Background (iterative loop)

1. Spawn Experiment Design (`agents/04-experiment-design.md`) to generate initial YAML configs
2. For each experiment run:
   a. Iterator/Evaluator (`agents/05-iterator-evaluator.md`) executes the run:
      - Write training script based on config
      - Run training (on detected compute environment)
      - Log metrics/params/artifacts to MLflow
      - Detect pathologies (loss plateau, mode collapse, overfitting)
      - Make decision: continue / adjust hyperparams / stop early
   b. Visualization Agent creates per-run training plots
   c. Fill in `templates/experiment_result.md` for this run
   d. **Git commit:** `"Phase 4: Experiment run {run_id} — {brief_result}"`
3. After all runs complete (or iteration budget exhausted):
   - **Git push**

### Phase 5: Analysis & Decision (Foreground, Interactive)

**Agents:** `agents/08-visualization.md` (background) + interactive presentation
**Mode:** Mixed

1. Spawn Visualization Agent for final cross-run comparison charts
2. Present to user:
   - Best performing configuration and metrics
   - Comparison table across all runs
   - Key visualizations (learning curves, metric comparisons)
   - What worked, what didn't, and why
3. Fill in `templates/iteration_report.md` → `project/iteration_report.md`
4. User decides: **Iterate** (back to Phase 3 or 4), **Pivot** (back to Phase 1), or **Done**
5. **Git commit:** `"Phase 5: Analysis report — {decision}"`
6. **Git push**

## Agent Spawning Patterns

### Foreground agents (interactive)
```
Read the agent .md file, then follow its instructions directly in the conversation.
The user sees everything and can interact.
```

### Background agents (parallel work)
```
Use the Agent tool with subagent_type="general-purpose":
- Set run_in_background=true for truly parallel work
- Read the agent .md file content and pass it as the prompt
- Include relevant context (project files, problem spec, etc.)
```

### Agent communication protocol
Agents communicate through files in `project/`:
- **Status updates:** Append to `project/status.md` (append-only log)
- **Deliverables:** Write to the appropriate template location in `project/`
- **Configs:** Write YAML configs to `project/configs/`
- **Visualizations:** Save to `project/visualizations/{phase}/`

Format for status.md entries:
```
## [{timestamp}] {agent_name}
**Status:** {running|completed|blocked|failed}
**Summary:** {one-line summary}
**Details:** {optional details}
---
```

## MLflow Conventions

- **Tracking URI:** `file:./mlruns`
- **Experiment naming:** `{project_name}` (one experiment per project)
- **Run naming:** `{model_type}_{key_param}_{value}` (e.g., `rf_n_estimators_100`)
- **Always log:**
  - All hyperparameters as params
  - All evaluation metrics as metrics
  - Training curves as artifacts
  - Model config YAML as artifact
  - Best model checkpoint as artifact (if applicable)
- **Tags:** `phase`, `iteration`, `status` (success/failed/stopped)

Use `utils/mlflow_helper.py` for all MLflow operations.

## Git Commit Protocol

Commit early and often. Required commits:
1. After Phase 1 completion (problem spec)
2. After Phase 2 completion (research + EDA)
3. After Phase 3 completion (experiment plan)
4. After **each** experiment run in Phase 4
5. After Phase 5 completion (analysis report)
6. Any time the user requests it

Commit message format: `"Phase {N}: {description}"`

Push after each phase completes (not after every single experiment run, unless the user requests it).

## Compute Environment Handling

The Problem Intake agent detects and documents the compute environment:

1. **Local detection:**
   - macOS: `system_profiler SPDisplaysDataType` for GPU info, check for MPS support
   - Linux: `nvidia-smi` for NVIDIA GPUs, check CUDA version
   - CPU-only: note limitations, suggest lighter models/smaller data

2. **Remote platforms:**
   - Ask user for platform name (Lambda, RunPod, Colab, AWS, GCP, etc.)
   - Web search for platform-specific setup guides
   - Ask for connection details (SSH, API keys, etc.)
   - Document how to run scripts on the platform

3. **Write to problem_spec.md** under `## Compute Environment`:
   - Platform name and specs
   - Connection method
   - How to execute training scripts
   - Special considerations (MPS backend, CUDA version, memory limits)

## Key Utilities

Always use the Python utilities in `utils/` rather than writing one-off code:
- `utils/mlflow_helper.py` — All MLflow operations
- `utils/metrics.py` — Metric computation (classification, regression, ranking)
- `utils/viz.py` — All visualization (EDA, training curves, evaluation plots)
- `utils/config.py` — YAML config management
- `utils/data_loader.py` — Data loading and validation
- `utils/file_io.py` — Status updates, project directory management

## Important Reminders

- **Always visualize first.** Before any modeling, look at the data.
- **Log everything to MLflow.** If it's not tracked, it didn't happen.
- **Commit often.** Every milestone gets a commit.
- **Simple changes first.** Try hyperparameter adjustments before architectural changes.
- **Read the templates.** They define the expected output format for each agent.
- **Check status.md.** Before starting work, check what other agents have done.
