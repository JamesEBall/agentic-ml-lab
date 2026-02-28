# Agentic ML Research Lab — Bootstrap Prompt

Give this entire prompt to a new Claude Code instance. It contains everything needed to build a reusable agentic ML research pipeline, informed by hard-won lessons from a real project (ESTA playstyle discovery).

---

## Your Mission

Build a reusable agentic ML research framework — an autonomous "AI lab" that takes a user's problem description and runs the full lifecycle: problem understanding → literature review → dataset discovery → experiment design → training → evaluation → iteration. It should work for any ML training task, not just the one described below.

This should be its own repo/tool. The output is a Claude Code-native workflow using background subagents, task tracking, and iterative refinement loops.

---

## Architecture: The Agent Roster

### 1. Problem Intake Agent (Interactive, Foreground)

**Purpose:** Loop through questions until the ML task is well-defined.

**Behavior:**
- Starts with the user's initial problem description
- Asks clarifying questions ONE AT A TIME using AskUserQuestion (not walls of text)
- Builds an internal "problem spec" document as it goes
- Questions should cover:
  - What is the input data? (modality, format, size, availability)
  - What is the desired output? (classification, generation, embedding, clustering?)
  - What does success look like? (metrics, baselines, "good enough" thresholds)
  - What compute is available? (GPU type, memory, training budget)
  - Any domain constraints? (real-time inference, interpretability, fairness?)
  - What has been tried before? (if anything)
- Exits when it has enough to write a 1-page problem spec
- Writes the spec to `project/problem_spec.md`

**Key lesson from ESTA:** The core philosophy was "discover what playstyle IS, not define it a priori." The intake agent should identify whether the user wants supervised (labels exist) or unsupervised (discover structure) and tailor everything downstream. Many ML projects fail because the problem is defined wrong, not because the model is wrong.

### 2. Research Orchestrator (Background)

**Purpose:** Spawns and manages a team of research sub-agents. Loops until it has enough priors.

**Sub-agents it spawns (all in background, in parallel):**

#### 2a. Dataset Discovery Agent
- Searches for relevant public datasets (HuggingFace, Kaggle, Papers With Code, domain-specific repos)
- Evaluates dataset size, quality, licensing
- Checks if the user's data is sufficient or needs augmentation
- Reports: dataset options, sizes, download links, preprocessing needs

#### 2b. Benchmark Agent
- Finds existing benchmarks and leaderboards for the task type
- Identifies SOTA methods and their reported metrics
- Establishes realistic performance targets
- Reports: benchmark table with method, metric, date, paper link

#### 2c. Paper Search Agent
- Searches arXiv, Semantic Scholar, Google Scholar for relevant papers
- Focuses on: methods (architectures, losses, training tricks), datasets, evaluation methodology
- Prioritizes recent work (2024-2026) but includes seminal papers
- Reports: annotated bibliography with key insights per paper

#### 2d. Blog/Material Agent
- Searches for practical guides, blog posts, GitHub repos, tutorials
- Focuses on implementation details that papers skip
- Finds common failure modes and debugging guides for the task type
- Reports: curated list with relevance scores

**Orchestrator behavior:**
- Waits for all sub-agents to complete
- Synthesizes findings into `project/research_brief.md`
- Identifies gaps: "We found no paper addressing X" or "No public dataset for Y"
- Loops: if gaps are critical, spawns targeted follow-up agents
- Exits when it can answer: "What are the top 3 approaches worth trying, and why?"

### 3. Plan Refinement Agent (Foreground)

**Purpose:** Takes research brief + problem spec → produces an experiment plan. Presents to user for approval.

**Behavior:**
- Reads `problem_spec.md` and `research_brief.md`
- Designs an ablation strategy: which components to vary, which to hold fixed
- Proposes architecture choices with justification from literature
- Defines evaluation metrics and success criteria
- Creates `project/experiment_plan.md` with:
  - Baseline model specification
  - Ablation matrix (what to test)
  - Training hyperparameters (with ranges, not just single values)
  - Evaluation protocol (which metrics, how often, what thresholds)
  - Compute budget estimate
  - Risk factors and fallback plans
- Uses EnterPlanMode to get user approval before proceeding

**Key lesson from ESTA:** The ablation strategy was critical. We tested 18 experiment variants across loss functions, architectures, and training tricks. The ablation revealed that simple changes (lowering beta from 1.0 to 0.1, raising free_bits from 0.1 to 1.0) had 10x more impact than complex architectural additions. The plan should always include "boring baselines" alongside novel approaches.

### 4. Experiment Design Agent (Background)

**Purpose:** Translates the approved plan into runnable training configs and scripts.

**Behavior:**
- Generates training configs for each ablation variant
- Sets up W&B (or other tracking) project structure
- Creates evaluation scripts
- Writes a `run_ablation.sh` or equivalent orchestration script
- Ensures reproducibility (seeds, config serialization, checkpoint saving)

### 5. Iterator/Evaluator Agent (Background, Continuous)

**THIS IS THE MOST IMPORTANT AGENT. It's the one you described as "always running."**

**Purpose:** Continuously monitors training results against success criteria. Feeds back to experiment design agent when adjustments are needed.

**Behavior loop:**
```
while not converged:
    1. Read latest metrics from W&B / checkpoints / logs
    2. Compare against success criteria from experiment_plan.md
    3. Detect issues:
       - Loss plateau? → suggest LR adjustment or architecture change
       - Posterior collapse (VAE)? → suggest beta/free_bits adjustment
       - Overfitting? → suggest regularization, data augmentation, early stopping
       - Mode collapse? → suggest diversity loss, different sampling
       - Metric regression? → alert immediately
    4. If metrics are "good enough" per success criteria → signal completion
    5. If metrics are stuck → generate a diagnostic report with:
       - What's wrong (specific metrics, trends)
       - Hypothesized root causes (ranked by likelihood)
       - Suggested fixes (with expected impact)
       - Whether to adjust evaluation methods OR the model
    6. Send report to Experiment Design Agent for plan adjustment
    7. Wait for next eval interval, repeat
```

**Key lessons from ESTA that this agent must encode:**

| Issue | How We Detected It | How We Fixed It |
|-------|-------------------|-----------------|
| MI collapse (beta too high) | UMAP went from clustered to uniform blob | Lowered beta 1.0 → 0.1 |
| False "active dims" | Metric said 15/16 active, but per-dim KL showed only 2 real | Raised free_bits 0.1 → 1.0 |
| Cyclical annealing destructive | Structure appeared then vanished on each cycle | Disabled cyclical, used linear warmup only |
| TC method too slow for hardware | 50-80s/batch on MPS with alpha-TCVAE | Switched to proxy (off-diagonal covariance) |
| W&B "crashed" false alarm | MPS puts process in UN state, W&B loses heartbeat | Check checkpoint timestamps, not W&B status |
| Player consistency gap too low | Silhouette ok but gap between player and random was only 0.048 | Added latent μ contrastive loss |

**The iterator should track:**
- Primary metrics: val_recon, KL, silhouette score, active dims (real, not threshold-based)
- Secondary metrics: player consistency, Fisher criterion, kNN accuracy, archetype-latent correlation
- Training health: gradient norms, learning rate, per-dim KL distribution, loss component breakdown
- Hardware health: GPU/MPS utilization, memory usage, training speed (it/s)

### 6. Devil's Advocate Agent (Background)

**Purpose:** Challenges every design decision. Finds flaws before they become bugs.

**Spawned at every major decision point. Evaluates:**
- Is the evaluation metric actually measuring what we care about?
- Could the results be confounded? (e.g., map-specific features driving clusters instead of playstyle)
- Is the dataset large/diverse enough for the model capacity?
- Are we overfitting to the evaluation set?
- What would a skeptical reviewer say about this approach?

### 7. Blue Sky Research Agent (Background)

**Purpose:** Continuously searches for better approaches while building.

**Behavior:**
- Runs web searches for related solutions, papers, approaches
- Monitors arXiv for new relevant papers
- Looks for tools, libraries, or techniques that could simplify the pipeline
- Reports findings that could change the current approach

---

## The Iteration Loop (The Core Innovation)

```
User describes problem
    ↓
Problem Intake Agent → problem_spec.md
    ↓
Research Orchestrator (spawns 4 sub-agents) → research_brief.md
    ↓
Plan Refinement Agent → experiment_plan.md (user approves)
    ↓
Experiment Design Agent → training configs + scripts
    ↓
┌──────────────────────────────────────────────┐
│  TRAINING LOOP                                │
│                                               │
│  Training runs ←→ Iterator/Evaluator Agent    │
│       ↑                    ↓                  │
│       │              Diagnostic Report        │
│       │                    ↓                  │
│       └── Experiment Design Agent (adjusts)   │
│                                               │
│  Devil's Advocate + Blue Sky run continuously │
└──────────────────────────────────────────────┘
    ↓
Success criteria met → Final evaluation + report
```

**Critical design principle:** The iterator doesn't just report metrics — it provides **actionable recommendations with reasoning**. It says "KL collapsed to 3.2 because free_bits=0.1 allows 2 dims to carry all info. Recommend raising free_bits to 1.0 which forces information spread across all 32 dims. Expected impact: all dims active, recon may increase 10-20% initially but should recover within 10 epochs."

---

## Implementation Notes

### File Structure
```
agentic-ml-lab/
├── agents/
│   ├── intake.py          # Problem intake agent
│   ├── research.py        # Research orchestrator + sub-agents
│   ├── planner.py         # Plan refinement
│   ├── experimenter.py    # Experiment design
│   ├── iterator.py        # The continuous evaluator
│   ├── advocate.py        # Devil's advocate
│   └── bluesky.py         # Blue sky research
├── templates/
│   ├── problem_spec.md    # Template for problem specification
│   ├── research_brief.md  # Template for research synthesis
│   └── experiment_plan.md # Template for experiment plan
├── project/               # Per-project working directory
│   ├── problem_spec.md
│   ├── research_brief.md
│   ├── experiment_plan.md
│   ├── iteration_log.md   # Iterator agent's running log
│   └── checkpoints/
├── utils/
│   ├── wandb_monitor.py   # W&B API helpers
│   ├── metric_tracker.py  # Metric comparison and trend detection
│   └── report_gen.py      # Diagnostic report generation
└── main.py                # Entry point: orchestrates the full pipeline
```

### How It Works in Claude Code

Each "agent" is implemented as a Task tool call with `subagent_type="general-purpose"` and `run_in_background=true`. The main conversation thread acts as the orchestrator.

```
# Pseudocode for the main loop
1. Foreground: Run intake agent (interactive questions)
2. Background: Spawn research orchestrator (which spawns 4 sub-agents)
3. Wait for research completion
4. Foreground: Run plan refinement (uses EnterPlanMode)
5. Background: Spawn experiment design agent
6. Background: Spawn iterator agent (continuous loop)
7. Background: Spawn devil's advocate
8. Background: Spawn blue sky research
9. Main thread: Monitor iterator reports, relay to user, handle escalations
```

### Key Technical Details for the Builder

- **Python 3.9+** minimum (for type hints)
- **W&B integration** is the assumed experiment tracker (but make it pluggable)
- **Background agents communicate via files** in the `project/` directory
- **The iterator agent needs a polling interval** — check metrics every N minutes
- **All agents should write structured markdown** so other agents can parse their outputs
- **Use TaskCreate/TaskUpdate** for tracking multi-step workflows
- **Agents should be resumable** — if Claude Code session restarts, the agent can pick up from its last checkpoint

### Success Criteria for THIS Framework

1. A user can describe an ML problem in plain English and get a working training pipeline within one session
2. The research phase finds relevant papers, datasets, and benchmarks automatically
3. The experiment plan includes ablation strategy with baseline comparisons
4. The iterator agent detects common training pathologies (collapse, overfitting, plateau) and suggests fixes
5. The devil's advocate catches at least one flaw per major decision
6. The whole system works for classification, generation, embedding, and clustering tasks

---

## Real-World Grounding: What We Learned Building ESTA Playstyle Discovery

This framework is born from building a CS:GO playstyle discovery system. Here's what went wrong and right:

**What worked:**
- Background agents for research, documentation, and devil's advocacy saved enormous time
- The ablation approach (18 experiments) found that simple hyperparameter changes beat complex architectural additions
- Behavioral stats as validation (not training signal) kept the representation honest
- W&B integration for tracking per-dim KL, UMAP snapshots, and reconstruction quality

**What we'd do differently:**
- Start with the iterator agent from day 1 — we manually monitored for weeks before automating
- Define success criteria BEFORE training, not after seeing results
- The devil's advocate should have caught the free_bits issue earlier (floor of 0.1 × 16 dims = 1.6 total KL, trivially satisfiable)
- Research agent should have found the beta-TCVAE paper earlier — it would have saved 3 failed training runs

**The model architecture that emerged:**
- Transformer encoder/decoder β-VAE (4 layers, 4 heads, d_model=128)
- 32-dim latent space with free_bits=1.0
- β=0.1 with linear warmup (no cyclical)
- TC penalty via proxy (off-diagonal covariance), γ=2.0
- Span-masked recovery + contrastive learning (from START paper)
- Weighted reconstruction emphasizing behavioral features over position
- Lambda-beta-VAE auxiliary L2 reconstruction term

This architecture wasn't designed up front — it evolved through the exact iteration loop this framework automates.

---

## Start Here

1. Create the repo structure
2. Build the Problem Intake Agent first (it's the entry point)
3. Build the Research Orchestrator next (most complex orchestration)
4. Build the Iterator/Evaluator (most impactful for training quality)
5. Wire them together with the main orchestration loop
6. Test on a simple task (e.g., MNIST VAE) before trying complex problems
