# Experiment Result

## Run ID: {run_id}
## Run Name: {run_name}
## Date: {date}
## Status: {success | failed | stopped_early}

## Configuration
- **Model:** {model type}
- **Key parameters:** {list key hyperparams}
- **Config file:** `project/configs/{config_file}`

## Results

### Primary Metric
- **{metric_name}:** {value}
- **vs. baseline:** {+/- delta} ({percentage} improvement/regression)
- **vs. previous best:** {+/- delta}

### All Metrics
| Metric | Train | Validation | Test |
|--------|-------|------------|------|
| ... | ... | ... | ... |

### Training Summary
- **Epochs completed:** {N} / {total}
- **Training time:** {duration}
- **Best epoch:** {N} (by validation {metric})
- **Final learning rate:** {value} (if applicable)

## Pathology Check
- [ ] Loss plateau: {yes/no — details}
- [ ] Overfitting: {yes/no — train/val gap}
- [ ] Underfitting: {yes/no — both losses high}
- [ ] NaN/Inf: {yes/no}
- [ ] Mode collapse: {yes/no — if generative}
- [ ] Other: {description}

## Visualizations
- Training curves: `project/visualizations/training/run_{run_id}/`
- {Other plots generated}

## Analysis
{2-3 sentences on what this run tells us}

## Decision
- **Action:** {continue | adjust | stop}
- **Reasoning:** {why this decision}
- **Next step:** {what to do next based on this result}

## MLflow
- **Experiment:** {experiment_name}
- **Run ID:** {mlflow_run_id}
