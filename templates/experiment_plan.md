# Experiment Plan

## Project: {project_name}
## Date: {date}
## Status: {draft | approved | in-progress | completed}

## Objective
{One sentence: what are we trying to learn from these experiments?}

## Experiment Sequence

### Run 001: {name} (Baseline)
- **Model:** {model type}
- **Key params:** {list}
- **Purpose:** Establish performance floor
- **Success criteria:** {metric} > {value}
- **Estimated runtime:** {time}

### Run 002: {name}
- **Model:** {model type}
- **Key params:** {list}
- **Change from previous:** {what changed and why}
- **Purpose:** {what we're testing}
- **Success criteria:** {metric} > {value}
- **Estimated runtime:** {time}

### Run 003: {name}
...

{Add more runs as needed}

## Hyperparameter Search Space
{If doing systematic search, define the space}

| Parameter | Range | Scale | Priority |
|-----------|-------|-------|----------|
| ... | ... | ... | ... |

## Stopping Criteria
- **Success:** {metric} >= {target} for 2+ runs
- **Diminishing returns:** Less than {X}% improvement for 3 consecutive runs
- **Budget:** Maximum {N} runs or {T} hours of compute
- **Failure:** All runs below baseline after {N} attempts → re-evaluate approach

## Data Split
- Train: {%}
- Validation: {%}
- Test: {%} (held out, only used for final evaluation)
- Cross-validation: {yes/no, k-fold}

## Visualization Plan
- Per-run: training curves, loss plots, metric progression
- Cross-run: comparison bars, parameter sensitivity plots
- Final: summary figure for presentation

## Decision Framework
After each run, the Iterator/Evaluator will:
1. Compare to baseline and previous best
2. Check for pathologies
3. Decide: continue | adjust | stop

## Notes
{Any additional context or decisions from the refinement discussion}
