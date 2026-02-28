# Hacker News Post

## Title

Show HN: 16 ML agents born from a VAE project where every metric lied to me

## Body

I spent months building a CS:GO playstyle discovery system (hierarchical Transformer beta-VAE on the ESTA dataset). It taught me more about ML failure modes than any course:

- My "active dimensions" metric said 15/16 dims were active. Visualizing per-dim KL revealed 2 were actually doing anything — the rest sat at the free_bits floor and got counted as "active."
- Silhouette score was positive and improving. It was measuring map geometry separation, not playstyle. 20.3% of my latent variance was explained by which map the round was played on.
- Cyclical annealing was supposed to help. Structure appeared, then got destroyed every cycle.
- The hyperbolic VAE I spent weeks implementing? Marginal improvement. Changing beta from 1.0 to 0.1? 10x improvement.

Every one of these cost GPU hours I'll never get back. So I built a framework to stop it from happening again.

**Agentic ML Research Lab** is 16 specialized agents that run the full ML research lifecycle in Claude Code. The agents are markdown files — no framework, no SDK. Claude reads the prompt and follows it.

The interesting part isn't the automation. It's the adversarial agents:

- **Devil's Advocate** challenges your approach before you waste compute. Data leakage? Wrong metric? Overfitting risk on a tiny dataset?
- **Optimization Guard** does a pre-flight check on every config. Estimates training time, profiles a single batch on your hardware, blocks runs that would blow budget.
- **The Bureaucrat** demands confidence intervals. "Your 96.7% accuracy on 30 samples has a 95% CI of ±7%. That is NOT 96.7% accuracy." Tracks cost per percentage point of improvement.
- **Post-Hoc Analyst** does the work nobody wants to do: feature attribution, error clustering in PCA space, and asking uncomfortable questions like "what is this metric actually measuring?"

The whole thing encodes 14 concrete lessons from the VAE project as detection signals. The Iterator agent knows to visualize per-dim KL distributions instead of trusting scalar "active dims" counts. It knows to regress latent dimensions against potential confounds. It knows that O(B²) operations hang on MPS.

**The 5-phase loop:**

1. Problem Intake — interviews you, detects your GPU, writes a problem spec with falsifiable success criteria
2. Research Sprint — 4 agents search papers/datasets/benchmarks/code in parallel while viz agent does EDA
3. Plan Refinement — Devil's Advocate + Blue Sky challenge the plan, you approve
4. Experiments — simple hyperparameter changes first, complex architecture second, MLflow tracks everything
5. Analysis — statistical audit, post-hoc interpretation, you decide: iterate, pivot, or done

Tested end-to-end with Iris classification (overkill, but that's the point of a smoke test — 4 models, MLflow tracking, confusion matrices, comparison charts, all automated).

The agents are just markdown. You can read every prompt, edit them, tune them like hyperparameters. If your Bureaucrat is too aggressive, tone it down. If your Blue Sky agent isn't creative enough, rewrite it.

GitHub: https://github.com/JamesEBall/agentic-ml-lab

The ESTA lessons table is in the README. The full writeup of all 14 failure modes with detection signals and fixes is in docs/lessons_from_esta.md.
