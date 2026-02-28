# Agentic ML Research Lab -- Orchestration Guide

You are operating inside the **Agentic ML Research Lab**, a Claude Code-native framework for running the full ML research lifecycle. This file defines how you orchestrate agents, track experiments, and communicate results.

## Origin Story

This framework was born from building ESTA (Esports Temporal-Spatial Analytics) -- a CS:GO playstyle discovery system using a Hierarchical Transformer beta-VAE. After months of manual training, debugging posterior collapse, fighting MPS backend issues, and discovering that our evaluation metrics were measuring map geometry instead of player behavior, we distilled every hard-won lesson into this reusable pipeline.

**Read `docs/lessons_from_esta.md` before your first experiment.** It documents 11 critical failure modes with detection signals and fixes.

## Core Philosophy

1. **Data first** -- Always look at the data before modeling. The Visualization Agent runs in every phase.
2. **Iteration > initial design** -- Simple hyperparameter changes often have 10x more impact than architectural changes. The loop matters more than the plan.
3. **Track everything** -- Every experiment goes through MLflow. Every result gets committed to git.
4. **Challenge assumptions** -- Devil's Advocate and Blue Sky agents exist for a reason. Use them.
5. **Don't waste compute** -- The Optimization Guard and Bureaucrat review every experiment. Cheap experiments that test the right thing beat expensive experiments that test the wrong thing.
6. **Statistical rigor** -- Point estimates without confidence intervals are not results. The Bureaucrat demands proper methodology.
7. **View and interpret every image** -- Never generate a plot without reading it back (via the Read tool on the saved PNG) and writing a semantic interpretation. "Saved correlation_matrix.png" is not acceptable. Describe what the plot *means* for the problem.
8. **Understand why, not just what** -- The Post-Hoc Analyst examines results through mathematical decomposition and philosophical reflection. Every experiment should yield *insight*, not just metrics.
9. **Define success criteria BEFORE training** -- Concrete, falsifiable metrics with thresholds. No moving goalposts. If criteria must change, document the revision explicitly.
10. **Audit every metric** -- A metric can be positive and still be measuring the wrong thing. Always ask "what is this metric actually measuring?" (See: silhouette measuring map separation, active dims counting free_bits floor as "active")

## Directory Layout

```
agents/          # Agent prompt templates (read these, spawn via Agent tool)
templates/       # Document templates agents fill in -> project/
utils/           # Python utilities for MLflow, metrics, viz, config, data, file I/O
project/         # Working directory for the current project
  data/          # Datasets
  configs/       # YAML experiment configs
  results/       # Experiment outputs
  visualizations/# All plots and charts
  logs/          # Training logs
docs/            # Project documentation
  bootstrap_prompt.md   # Original design document from ESTA
  lessons_from_esta.md  # 11 critical lessons with detection signals
mlruns/          # MLflow tracking store (gitignored)
```

## The Agent Roster (16 Agents)

### Phase 1: Problem Intake (Foreground, Interactive)
| Agent | File | Role |
|-------|------|------|
| Problem Intake | `agents/01-problem-intake.md` | Interviews user, detects compute environment, writes problem spec |

### Phase 2: Research Sprint (Background, Parallel)
| Agent | File | Role |
|-------|------|------|
| Research Orchestrator | `agents/02-research-orchestrator.md` | Coordinates 4 parallel research sub-agents |
| Dataset Discovery | `agents/02a-dataset-discovery.md` | Finds relevant datasets across HuggingFace, Kaggle, Papers With Code |
| Benchmark Search | `agents/02b-benchmark.md` | Finds SOTA benchmarks, leaderboards, baselines |
| Paper Search | `agents/02c-paper-search.md` | Searches arXiv, Semantic Scholar for relevant papers |
| Blog & Material | `agents/02d-blog-material.md` | Finds tutorials, code repos, pretrained models |

### Phase 3: Plan Refinement (Mixed)
| Agent | File | Role |
|-------|------|------|
| Plan Refinement | `agents/03-plan-refinement.md` | Refines experiment plan interactively with user |
| Devil's Advocate | `agents/06-devils-advocate.md` | Challenges assumptions, finds confounds, demands rigor |
| Blue Sky | `agents/07-blue-sky.md` | Proposes creative alternative approaches |

### Phase 4: Experiment Execution (Background, Iterative)
| Agent | File | Role |
|-------|------|------|
| Experiment Design | `agents/04-experiment-design.md` | Generates concrete YAML run configs |
| Iterator/Evaluator | `agents/05-iterator-evaluator.md` | Core engine: runs experiments, detects pathologies, decides next steps |
| Visualization | `agents/08-visualization.md` | EDA, training curves, cross-run comparison -- views and interprets every image |
| Model Builder | `agents/09-model-builder.md` | Translates configs into correct, runnable training code |
| Optimization Guard | `agents/10-optimization-guard.md` | Pre-flight: estimates time, catches bad configs, enforces budgets |

### Phase 5: Analysis & Decision (Mixed)
| Agent | File | Role |
|-------|------|------|
| The Bureaucrat | `agents/11-bureaucrat.md` | Audits statistical rigor, computes CIs, tracks costs |
| Post-Hoc Analyst | `agents/12-post-hoc-analyst.md` | Deep interpretive analysis -- feature attribution, error clustering, epistemological reflection |

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
4. **CRITICAL: Define falsifiable success criteria** with concrete thresholds BEFORE any training
5. Fill in `templates/problem_spec.md` -> save to `project/problem_spec.md`
6. **Git commit:** `"Phase 1: Problem specification for {project_name}"`
7. **Git push**

### Phase 2: Research Sprint (Background, Parallel)

**Agents:** `agents/02-research-orchestrator.md` + 4 sub-agents + `agents/08-visualization.md`
**Mode:** Background (parallel)

1. Read `agents/02-research-orchestrator.md` and spawn it as a background agent
2. The orchestrator spawns 4 research sub-agents in parallel:
   - `agents/02a-dataset-discovery.md` -- Find relevant datasets
   - `agents/02b-benchmark.md` -- Find SOTA benchmarks and baselines
   - `agents/02c-paper-search.md` -- Search for relevant papers
   - `agents/02d-blog-material.md` -- Find blogs, tutorials, code examples
3. **Simultaneously** spawn `agents/08-visualization.md` for EDA:
   - Load the data
   - Generate distribution plots, correlation matrices, sample previews
   - Save all plots to `project/visualizations/eda/`
4. Orchestrator compiles findings into `templates/research_brief.md` -> `project/research_brief.md`
5. **Git commit:** `"Phase 2: Research brief and EDA for {project_name}"`
6. **Git push**

### Phase 3: Plan Refinement (Foreground, Interactive)

**Agents:** `agents/03-plan-refinement.md` (foreground) + `agents/06-devils-advocate.md` + `agents/07-blue-sky.md` (background)
**Mode:** Mixed

1. Spawn Devil's Advocate (`agents/06-devils-advocate.md`) in background -- reads problem_spec + research_brief, writes critique
2. Spawn Blue Sky (`agents/07-blue-sky.md`) in background -- proposes creative alternatives
3. In foreground, run Plan Refinement (`agents/03-plan-refinement.md`):
   - Present research findings to user
   - Show EDA visualizations
   - Present Devil's Advocate critique and Blue Sky ideas when they complete
   - Discuss and iterate on the experiment plan
   - **Ensure plan includes "boring baselines" (simple hyperparameter sweeps) alongside novel approaches**
   - User approves final plan
4. Fill in `templates/experiment_plan.md` -> `project/experiment_plan.md`
5. Update `agents/08-visualization.md` with training visualization plan
6. **Git commit:** `"Phase 3: Experiment plan for {project_name}"`
7. **Git push**

### Phase 4: Experiment Execution (Background, Iterative)

**Agents:** `agents/04-experiment-design.md` + `agents/05-iterator-evaluator.md` + `agents/08-visualization.md` + `agents/09-model-builder.md` + `agents/10-optimization-guard.md`
**Mode:** Background (iterative loop)

1. Spawn Experiment Design (`agents/04-experiment-design.md`) to generate initial YAML configs
2. **Schedule simple hyperparameter changes FIRST, complex architectural changes SECOND**
3. For each experiment run:
   a. **Optimization Guard** (`agents/10-optimization-guard.md`) reviews the config first:
      - Estimates training time
      - Checks for misconfigurations (bad LR, too many epochs, wrong device)
      - **Profiles a single batch forward+backward on target hardware**
      - Verifies compute budget
      - APPROVE / WARN / REJECT
   b. **Model Builder** (`agents/09-model-builder.md`) writes the training script:
      - Translates config to runnable Python code
      - Handles framework detection (sklearn, PyTorch, XGBoost)
      - Sets up data pipeline with proper train/test isolation
   c. Iterator/Evaluator (`agents/05-iterator-evaluator.md`) executes the run:
      - Run training (on detected compute environment)
      - Log metrics/params/artifacts to MLflow
      - **Detect pathologies** (see Pathology Detection below)
      - Make decision: continue / adjust hyperparams / stop early
   d. Visualization Agent creates per-run training plots
   e. Fill in `templates/experiment_result.md` for this run
   f. **Git commit:** `"Phase 4: Experiment run {run_id} -- {brief_result}"`
4. After all runs complete (or iteration budget exhausted):
   - **Git push**

### Phase 5: Analysis & Decision (Foreground, Interactive)

**Agents:** `agents/08-visualization.md` + `agents/11-bureaucrat.md` + `agents/12-post-hoc-analyst.md` (background) + interactive presentation
**Mode:** Mixed

1. Spawn Visualization Agent for final cross-run comparison charts
2. Spawn **The Bureaucrat** (`agents/11-bureaucrat.md`) for statistical audit:
   - Computes confidence intervals for all results
   - Runs significance tests for model comparisons
   - Reports compute cost-effectiveness
   - Writes `project/bureaucrat_audit.md`
3. Spawn **Post-Hoc Analyst** (`agents/12-post-hoc-analyst.md`) for deep interpretation:
   - Feature attribution and importance decomposition
   - Error clustering in PCA space -- what characterizes misclassified samples?
   - Model agreement/disagreement analysis
   - **Confound audit**: test whether results are driven by confounding variables
   - **Metric-space correctness**: verify analysis uses correct geometry for the representation space
   - Epistemological reflection on what was actually learned vs assumed
   - Writes `project/post_hoc_analysis.md`
4. Present to user:
   - Best performing configuration and metrics
   - Comparison table across all runs
   - Key visualizations (learning curves, metric comparisons)
   - What worked, what didn't, and why
5. Fill in `templates/iteration_report.md` -> `project/iteration_report.md`
6. User decides: **Iterate** (back to Phase 3 or 4), **Pivot** (back to Phase 1), or **Done**
7. **Git commit:** `"Phase 5: Analysis report -- {decision}"`
8. **Git push**

## Pathology Detection (Iterator Agent Must Check)

These are the pathologies discovered during ESTA development. The Iterator agent must monitor for all of them:

| Pathology | Detection Signal | Recommended Fix |
|-----------|-----------------|-----------------|
| Posterior collapse (VAE) | Per-dim KL: 1-2 bars tall, rest at floor | Lower beta, raise free_bits |
| False "active dims" | Metric says 15/16 active, but per-dim KL shows most at floor | Visualize per-dim KL, raise free_bits, lower threshold |
| Cyclical annealing destroying structure | UMAP structure appears/disappears cyclically | Disable cyclical, use linear warmup only |
| TC computation too slow | >10s per batch, process hangs | Switch to proxy method (off-diagonal covariance) |
| Confounded clusters | Silhouette > 0 but clusters match a confound variable | Condition on confound, re-evaluate. Compute R-squared of confound |
| Misleading silhouette | Positive silhouette driven by confound not target | Color UMAP by confounds, compute confound R-squared |
| Loss plateau | Loss unchanged for >N epochs | Adjust LR, check gradient norms, try different optimizer |
| Overfitting | Train loss decreasing, val loss increasing | Regularization, data augmentation, early stopping |
| Mode collapse (GAN/VAE) | Generated samples lack diversity | Diversity loss, different sampling strategy |
| Hardware crash false alarm | W&B says "crashed" but process alive | Check checkpoint timestamps, `ps aux`, not W&B status |
| Slow data preprocessing | Data loading takes minutes (LZMA, gzip, large CSVs) | Profile loading separately, convert to Parquet/HDF5, cache preprocessed data |
| Null data crash | `TypeError: NoneType` on raw data fields | Defensive null checks on all external data, log and skip bad records |
| Wrong compute target | Training runs locally instead of on designated server | ALWAYS read problem_spec.md compute section before executing ANY training |

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

4. **MPS-specific caveats** (from ESTA experience):
   - `torch.linalg.logdet` not supported
   - `torch.linalg.lu_solve` not supported
   - O(B^2) pairwise operations can cause 50-80s/batch hangs
   - Long-running compute can enter UN (uninterruptible sleep) state
   - W&B heartbeat can be lost during UN state -- verify via checkpoint timestamps
   - PyTorch 2.6 requires `weights_only=False` for `torch.load`

## Key Utilities

Always use the Python utilities in `utils/` rather than writing one-off code:
- `utils/mlflow_helper.py` -- All MLflow operations
- `utils/metrics.py` -- Metric computation (classification, regression, ranking)
- `utils/viz.py` -- All visualization (EDA, training curves, evaluation plots)
- `utils/config.py` -- YAML config management
- `utils/data_loader.py` -- Data loading and validation
- `utils/file_io.py` -- Status updates, project directory management

## CRITICAL: Do Not Get Stuck (Anti-Loop Rules)

These rules exist because agents get trapped in retry loops. This is the #1 failure mode in practice.

### The 2-Strike Rule
If a command or script fails with the same error twice, STOP RETRYING. Read the error, diagnose the root cause, fix it, then try once more. Never run the same failing command a third time.

### Script Execution
1. **Every script must be self-contained for imports.** Add this header to every generated Python script:
   ```python
   import sys, os
   PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
   sys.path.insert(0, PROJECT_ROOT)
   ```
2. **Run scripts in the foreground.** Do not use `nohup ... &`, `sleep && tail`, or background processes for scripts that take <5 minutes. You need to see the output immediately.
3. **Never use sleep-poll loops.** If you need to wait for something, use `run_in_background` and let the system notify you. Do not write `sleep 10 && tail -5 logfile` loops.
4. **If a script has an ImportError, fix the script's sys.path.** Do not try running from a different directory. Do not try `cd somewhere && python script.py`. The script itself must resolve its own paths.

### Compute Target Rule
Before executing ANY training script, read `project/problem_spec.md` and check the compute environment section. If it specifies a remote target (SSH, cloud, etc.), ALL training must run there — not locally. No exceptions. No "I'll just run it locally to test." The problem spec is the single source of truth for where training happens.

### Data Loading Rule
Always profile data loading as a separate step before training. If raw data is compressed (LZMA, gzip, bz2) or in a slow format (large CSV, JSON), convert to a fast format (Parquet, HDF5, memory-mapped NumPy) ONCE and use the fast version for all runs. Never re-decompress the same data twice. Always add null checks when processing external data — log and skip malformed records rather than crashing.

### When Stuck
- Write the error and what you tried to `project/status.md`
- Mark the run as `status: failed` with the full traceback
- Move on to the next experiment
- Do NOT keep retrying the same approach

### Common Traps to Avoid
| Trap | What happens | What to do instead |
|------|-------------|-------------------|
| Directory roulette | Agent tries running from 5 different directories | Fix sys.path in the script |
| Sleep-poll loop | Agent sleeps, checks log, sleeps, checks log | Run in foreground or use run_in_background |
| Background everything | Agent loses track of what's running | Only background truly long tasks (>5 min) |
| Retry without reading error | Same error 4 times in a row | Read the traceback. Fix the cause. |
| SSH retry loop | Remote command fails, agent keeps SSHing | Check connection once, then fix locally |
| Training on wrong machine | Runs locally when problem_spec says remote | ALWAYS check problem_spec.md compute section first |
| Re-decompressing data | LZMA/gzip decompression every run | Convert to fast format once, cache it |
| Null crash mid-pipeline | Raw data has missing fields, crash at record N | Add null checks, skip bad records, report count |

## Development Workflow Preferences

- **Always use background agents** for research, journal updates, paper downloads, and similar non-blocking tasks
- **Always run a documentation agent** in the background when building -- keeps docs updated as code changes
- **Always run a devil's advocate agent** in the background -- challenges design decisions, finds flaws
- **Always run a blue sky research agent** in the background -- web searches for related solutions/papers/approaches
- **Push to git regularly** after each phase and any significant milestone
- **Work autonomously** -- don't ask permission, just do it and show results. The user prefers seeing completed work over being asked for approval at every step.

## Important Reminders

- **Always visualize first.** Before any modeling, look at the data.
- **Log everything to MLflow.** If it's not tracked, it didn't happen.
- **Commit often.** Every milestone gets a commit.
- **Simple changes first.** Try hyperparameter adjustments before architectural changes.
- **Read the templates.** They define the expected output format for each agent.
- **Check status.md.** Before starting work, check what other agents have done.
- **Read `docs/lessons_from_esta.md`.** Before your first experiment, absorb the failure modes.
- **Audit every metric.** Ask what it's actually measuring, not what it's supposed to measure.
- **Define success criteria upfront.** No moving goalposts.
- **Never retry the same failure more than twice.** Read the error. Fix the cause. See anti-loop rules above.
