# Iteration Report

## Project: {project_name}
## Iteration: {N}
## Date: {date}

## Summary
{2-3 sentence overview of this iteration's results}

## Experiments Run

| Run | Model | Primary Metric | vs Baseline | Status |
|-----|-------|----------------|-------------|--------|
| ... | ... | ... | ... | ... |

## Best Result
- **Run:** {run_id}
- **Model:** {model description}
- **Primary metric:** {metric}={value}
- **Key parameters:** {list}

## What Worked
1. {Finding — what improved results and why}
2. {Finding}
3. {Finding}

## What Didn't Work
1. {Finding — what didn't help and why}
2. {Finding}
3. {Finding}

## Key Insights
1. {Insight about the problem/data/approach}
2. {Insight}
3. {Insight}

## Visualizations
- Comparison chart: `project/visualizations/analysis/comparison.png`
- Training curves: `project/visualizations/analysis/training_overlay.png`
- Best model evaluation: `project/visualizations/analysis/best_model_eval.png`

## MLflow Summary
- Experiment: {experiment_name}
- Total runs: {N}
- Best run ID: {mlflow_run_id}
- MLflow UI: `mlflow ui --backend-store-uri file:./mlruns`

## Decision
- [ ] **Iterate** — Go back to Phase {3|4} with refined approach
- [ ] **Pivot** — Fundamental change needed, go back to Phase 1
- [ ] **Done** — Results meet success criteria

## Next Steps
{If iterating or pivoting, what specifically should change}
1. {Action item}
2. {Action item}
3. {Action item}
