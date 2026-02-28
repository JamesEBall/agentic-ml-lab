# Lessons from ESTA Playstyle Discovery

Hard-won lessons from building a CS:GO playstyle discovery system using a Hierarchical Transformer beta-VAE on ~6,662 rounds of pro match data. Every lesson below cost real compute hours and debugging time. These are the things the Iterator/Evaluator and Devil's Advocate agents must encode.

---

## 1. Posterior Collapse and free_bits

**The problem:** With beta=1.0 and free_bits=0.1, the model collapsed to using only 2 of 32 latent dimensions. The "active dims" metric reported 15/16 active (KL > 0.1 threshold), but this was **catastrophically misleading** -- most dims sat at exactly KL=0.1 (the free_bits floor), encoding almost nothing.

**The math:** With D=32 dims and free_bits=0.1, the model needs only total KL=3.2 to satisfy the constraint. Two dimensions at KL=1.6 each satisfies it while 30 dimensions collapse to the prior. The free_bits floor was set too low to force information spread.

**The fix:**
- Raised free_bits from 0.1 to **1.0** -- this forces a minimum of 32 nats total KL, meaning ALL dimensions must contribute
- Lowered beta from 1.0 to **0.1** -- much gentler KL pressure
- Added lambda-beta-VAE (auxiliary L2 reconstruction) -- provides gradient signal to the decoder even when beta pushes KL down

**The lesson for the framework:** Never trust a single "active dims" metric. Always look at the full per-dimension KL distribution. A threshold-based count is meaningless if the threshold is below the free_bits floor.

---

## 2. Cyclical Annealing Destroys Structure

**The problem:** Cyclical beta annealing (ramping beta from 0 to target, then resetting to 0 repeatedly) was supposed to help avoid posterior collapse. Instead, it **destroyed learned latent structure** every time beta reset.

**What happened:** During the low-beta phase, the model learned useful clusters. During the ramp-up phase, the high beta pressure collapsed them. Each cycle was a step forward followed by a step back.

**The fix:** Disabled cyclical annealing entirely. Used a simple linear warmup to beta=0.1 over the first 20 epochs, then held constant.

**The lesson for the framework:** Cyclical annealing may work for large datasets and high-capacity models, but for moderately-sized datasets (~6.6K samples), monotonic warmup to a low beta is far more stable. The Iterator agent should detect UMAP structure appearing and disappearing across cycles as a signal to disable cyclical annealing.

---

## 3. Euclidean Metrics on Hyperbolic Spaces

**The problem:** The post-hoc analysis initially performed PCA directly on the spatial coordinates of the Lorentz embedding. This is equivalent to doing Euclidean PCA on a hyperbolic space -- a **mathematical error**. Points with the same Euclidean distance can be exponentially different in geodesic distance on the hyperboloid.

**The correct approach:**
1. Map all points to the tangent space at the origin using the Lorentz **logarithmic map**
2. Perform PCA in tangent space (where Euclidean operations are valid)
3. Use geodesic distances (via `arcosh(-<x,y>_L)`) instead of Euclidean distances for clustering

**Measured impact:** In this case, the divergence between tangent-space PCA and Euclidean PCA was small (0.4-3.8% per PC), because the spatial norms were modest (mean=0.552). But for data with larger norms (further from origin on the hyperboloid), the error would be catastrophic.

**The lesson for the framework:** When using non-Euclidean latent spaces (hyperbolic, spherical, product manifolds), ALL downstream analysis must use geometry-appropriate metrics. The Post-Hoc Analyst and Devil's Advocate agents must flag any use of Euclidean distances/operations on non-Euclidean representations.

---

## 4. The Map Confound (20.3% R-squared)

**The problem:** The latent space silhouette score was 0.273 (HDBSCAN) -- seemingly reasonable. But when we checked what drove the clusters, **map identity alone explained 20.3% of the variance** in the latent space (linear regression R-squared).

**What this means:** The model learned map geometry first, playstyle second. The HDBSCAN clusters were primarily separating "played on Mirage" from "played on Nuke" -- which is geographic confound, not behavioral discovery.

**The smoking gun:** When we ran HDBSCAN **within** each map (removing the geometric confound), clustering collapsed:
- de_inferno: 0 clusters, 100% noise
- de_mirage: 0 clusters, 100% noise
- de_nuke: 0 clusters, 100% noise
- de_ancient: 2 clusters, 82.9% noise, silhouette -0.107

Within a single map, there was no discrete cluster structure at all.

**The lesson for the framework:** The Devil's Advocate agent must ALWAYS ask: "Could the clusters be driven by a confound rather than the target variable?" Test by conditioning on potential confounds and re-running clustering. If clusters disappear, the confound was the signal, not the target.

---

## 5. Playstyle is Continuous, Not Discrete

**The problem:** The project assumed playstyle would fall into discrete archetypes (aggressive, passive, lurker, etc.). The data contradicted this.

**The evidence:**
- KMeans sweep: best silhouette was only 0.206 (k=3), driven by map confound
- Within-map clustering: HDBSCAN found 0-2 clusters with 78-100% noise
- Gap statistic showed marginal improvement over uniform null at all k values
- Geodesic distance distribution: continuous with slight heavy tails (kurtosis=2.710)

**What the model actually learned:** The top principal components encoded continuous behavioral gradients:
- PC0 (26.2%): survival duration (quick death vs long alive)
- PC1 (15.7%): weapon economy (rifle vs pistol/eco)
- PC2 (10.8%): sniper role (scoped vs non-scoped)
- PC3 (7.3%): equipment level (but correlated with map at r=-0.475)

These are real behavioral axes, but they form a **continuous manifold**, not discrete clusters.

**The lesson for the framework:** The Problem Intake agent should always ask: "Do you expect discrete categories or a continuous spectrum?" The Iterator agent should test this assumption early by running clustering diagnostics. If the data is continuous, switch the evaluation framework from cluster-based metrics (silhouette, ARI) to manifold-based ones (reconstruction quality, interpolation smoothness, disentanglement scores).

---

## 6. Player Consistency Ratio of 0.949

**The problem:** If playstyle is a per-player trait, then a player's rounds should cluster together in latent space. We measured this with a consistency ratio:

```
ratio = mean(intra-player distances) / mean(inter-player distances)
```

**The result:** 0.949 -- meaning a player's own rounds vary almost as much (94.9% as much) as rounds between different players. Put differently, knowing which player played a round tells you almost nothing about where that round lands in the latent space.

**What this means:** "Playstyle" at the round level is dominated by situational factors (map, economy, weapon role, team situation, opponent behavior). The individual player's persistent behavioral signature is the **smallest component** of variance.

**The lesson for the framework:** The Iterator agent should compute consistency metrics early. If the target grouping variable (player, team, class, etc.) has a ratio above 0.9, the representation is not capturing that variable's signal -- it is capturing something else. This is not necessarily a model failure; it may be a **problem definition failure** (the target variable doesn't have the structure you assumed).

---

## 7. Silhouette Score is Misleading

**The problem:** The overall silhouette score (0.273 with HDBSCAN, 0.206 with KMeans k=3) looked reasonable for a clustering result. But it was measuring **map separation**, not playstyle separation.

**How to detect this:**
1. Compute silhouette using your cluster labels
2. Color the same UMAP by potential confounds (map, economy state, team side)
3. If confound coloring matches cluster coloring, the silhouette is measuring the confound
4. Run an R-squared test: regress latent coordinates against the confound variable

**The lesson for the framework:** The Bureaucrat agent should always demand: "What is the silhouette actually measuring?" A positive silhouette with confounded clusters is worse than a negative silhouette with honest evaluation. Every clustering metric needs a confound audit.

---

## 8. TC Method Performance on MPS (Apple Silicon)

**The problem:** The alpha-TCVAE method (which decomposes KL into index-code MI, total correlation, and dimension-wise KL) requires computing O(B^2 * D) pairwise log-densities. On MPS (Apple Silicon), this caused:
- 50-80 seconds per batch (vs <1s normally)
- Process entering uninterruptible sleep (UN state in `ps`)
- W&B losing heartbeat and reporting "crashed" (but process was actually alive)

**The fix:** Switched to a TC proxy method using off-diagonal covariance of the posterior mean:
```python
# Instead of expensive pairwise computation:
# tc_loss = alpha_tc_decomposition(z, mu, logvar)  # O(B^2 * D), 50-80s

# Use proxy:
# tc_loss = off_diagonal_covariance_penalty(mu)     # O(B * D^2), <0.01s
```

**The lesson for the framework:** The Optimization Guard agent must profile operations on the target hardware BEFORE committing to a training run. Some mathematically clean formulations are computationally impractical on specific backends. The guard should run a single batch forward+backward pass and check timing before approving a full training run.

**Additional MPS caveats:**
- `torch.linalg.logdet` not supported
- `torch.linalg.lu_solve` not supported
- Long-running MPS compute can trigger UN state, confusing process monitors
- Always verify training is alive by checking checkpoint timestamps, not W&B status

---

## 9. Active Dims Metric is Misleading with Threshold-Based Detection

**The problem:** The standard "active dimensions" metric counts latent dimensions where KL > threshold (commonly 0.01 or 0.1). With free_bits=0.1 and threshold=0.1, the metric reported 15/16 dims active. But the per-dim KL bar chart showed the truth: 2 dims at KL~1.5, 13 dims at KL~0.1 (exactly the free_bits floor), 1 dim at KL~0.0.

**Why the metric lies:** The free_bits mechanism sets a floor on per-dim KL. Any dim with KL at or slightly above the floor passes the threshold check, even though it encodes negligible information. A dim with KL=0.11 is "active" by the metric but encoding less than 0.01 nats of useful information above the floor.

**Better alternatives:**
1. **Per-dim KL bar chart**: Visual inspection of the full distribution, not a scalar summary
2. **Effective dimensionality**: Using the eigenvalue spectrum of the posterior covariance
3. **KL above free_bits floor**: Count dims where `KL - free_bits > meaningful_threshold`
4. **Variance explained per dim**: How much reconstruction quality degrades when each dim is zeroed out

**The lesson for the framework:** The Iterator agent should never rely on a single scalar metric. Always visualize the distribution behind the metric. The Visualization agent should generate per-dim KL bar charts at every evaluation interval.

---

## 10. Simple Changes Beat Complex Architecture

**The ablation result:** Across 18 experiment variants testing different architectures, losses, and training tricks:

| Change | Impact |
|--------|--------|
| beta 1.0 -> 0.1 | **10x improvement** in latent utilization |
| free_bits 0.1 -> 1.0 | **All 32 dims active** (vs 2 before) |
| Disable cyclical annealing | **Stable training**, no structure destruction |
| Add TC proxy penalty | Minor improvement in disentanglement |
| Add contrastive loss | Minor improvement in player consistency (0.048 gap) |
| Lambda-beta-VAE | Helpful but not transformative |
| Switch to Hyperbolic VAE | Different geometry, same underlying issues |
| Add CPLearn HDC loss | Marginal effect |

**The lesson for the framework:** The Plan Refinement agent should always include "boring baselines" -- simple hyperparameter sweeps -- alongside novel architectural changes. The Experiment Design agent should schedule simple changes FIRST, so the Iterator has a strong baseline before testing complex additions.

---

## 11. Philosophical Lesson: Define Success Criteria BEFORE Training

**The mistake:** We trained a model, then tried to figure out what "good" looks like after seeing results. This led to:
- Moving goalposts ("silhouette of 0.2 is actually fine because...")
- Post-hoc rationalization of confounded results
- Weeks of training without clear pass/fail criteria

**What we should have done:**
1. Define: "Success = silhouette > 0.3 on clusters NOT explained by map identity"
2. Define: "Success = player consistency ratio < 0.85"
3. Define: "Success = at least 3 interpretable behavioral axes in top 5 PCs"
4. Set these BEFORE the first training run

**The lesson for the framework:** The Problem Intake agent and Plan Refinement agent must produce concrete, falsifiable success criteria. The Iterator agent evaluates against these criteria, not against moving goalposts. If criteria are met, the project succeeds. If not, the criteria can be revised -- but that revision must be a conscious, documented decision, not an implicit drift.

---

## Summary Table

| Lesson | Detection Signal | Recommended Action |
|--------|-----------------|-------------------|
| Posterior collapse | Per-dim KL shows 1-2 tall bars, rest at floor | Lower beta, raise free_bits |
| Cyclical annealing destructive | UMAP structure appears/disappears cyclically | Disable cyclical, use linear warmup |
| Wrong metric space | Using Euclidean ops on non-Euclidean space | Use tangent-space PCA, geodesic distances |
| Confounded clusters | R-squared of confound > 0.1 on latent space | Condition on confound, re-evaluate |
| Continuous not discrete | Silhouette < 0.3, within-condition 0 clusters | Switch to continuous evaluation metrics |
| Low player consistency | Intra/inter ratio > 0.9 | Target variable may lack structure |
| Misleading silhouette | Confound coloring matches cluster coloring | Always audit what silhouette measures |
| TC too slow on MPS | >10s per batch | Switch to proxy method |
| Misleading active dims | Dims at free_bits floor counted as active | Visualize per-dim KL, don't trust scalar |
| Simple > complex | Hyperparameter change outperforms architecture | Test simple changes first |
| No success criteria | Post-hoc rationalization of results | Define criteria before training |
