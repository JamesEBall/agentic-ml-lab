# Experiment Result

## Run ID: 001
## Run Name: logistic_regression
## Status: success

## Configuration
- **Model:** LogisticRegression
- **Key parameters:** {'max_iter': 200, 'random_state': 42}
- **Config file:** `project/configs/run_001_logistic_regression.yaml`

## Results

### Primary Metric
- **accuracy:** 0.9667

### All Metrics
| Metric | Test |
|--------|------|
| accuracy | 0.9667 |
| f1 | 0.9666 |
| precision | 0.9697 |
| recall | 0.9667 |

### Cross-Validation
- **CV accuracy:** 0.9667 (+/- 0.0167)

## Visualizations
- Confusion matrix: `project/visualizations/training/run_001_confusion_matrix.png`

## Analysis
logistic_regression achieved 96.7% test accuracy with 5-fold CV accuracy of 96.7%.
