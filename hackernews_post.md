# Hacker News Post

## Title (80 char limit)

Show HN: Agentic ML Lab – 16 AI agents that run the full ML research lifecycle

## Body

I built a framework where Claude Code orchestrates 16 specialized agents through the entire ML research pipeline: problem definition → literature review → EDA → experiment design → training → evaluation → iteration.

The agents are just markdown prompt templates. No custom infrastructure. Claude Code's Agent tool spawns them as foreground (interactive) or background (parallel) processes. They communicate through files in a shared project directory.

**What makes it interesting:**

The agent roster goes beyond "run experiments." There's a Devil's Advocate that challenges your approach before you waste compute. A Blue Sky agent that proposes creative alternatives. An Optimization Guard that estimates training time and blocks bad configs. A "Bureaucrat" that demands confidence intervals and statistical significance tests for every comparison. And a Post-Hoc Analyst that does feature attribution, error clustering in PCA space, and epistemological reflection on what your results actually prove.

**The key insight that motivated this:**

Building an earlier ML project, I discovered that simple hyperparameter changes (beta 1.0→0.1, free_bits 0.1→1.0) had 10x more impact than complex architectural changes. The iteration loop matters more than the initial design. So the framework is built around fast iteration with aggressive guardrails.

**Practical details:**

- MLflow tracks everything
- Visualization Agent views and semantically interprets every plot it generates (not just "saved plot.png" — actually describes what the data means)
- Detects your compute environment (local GPU, MPS on Mac, cloud) and adapts
- Git commits at every milestone
- Tested end-to-end with Iris classification (yes, it's overkill for Iris — that's the point of a smoke test)

**The 5-phase workflow:**

1. Problem Intake — interactive interview + compute detection
2. Research Sprint — 4 parallel agents search papers, datasets, benchmarks, code
3. Plan Refinement — Devil's Advocate + Blue Sky challenge the plan, user approves
4. Experiments — Optimization Guard → Model Builder → train → evaluate → adjust loop
5. Analysis — Bureaucrat audits statistics, Post-Hoc Analyst decomposes why results happened

Everything is open source. It's a single repo you clone, run setup.sh, and start describing your ML problem.

GitHub: https://github.com/JamesEBall/agentic-ml-lab
