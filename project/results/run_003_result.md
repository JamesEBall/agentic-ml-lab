# Experiment Result

## Run ID: 003
## Run Name: svm_rbf
## Status: success

## Configuration
- **Model:** SVC
- **Key parameters:** {'kernel': 'rbf', 'C': 1.0, 'gamma': 'scale', 'random_state': 42}
- **Config file:** `project/configs/run_003_svm_rbf.yaml`

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
- **CV accuracy:** 0.9750 (+/- 0.0204)

## Visualizations
- Confusion matrix: `project/visualizations/training/run_003_confusion_matrix.png`

## Analysis
svm_rbf achieved 96.7% test accuracy with 5-fold CV accuracy of 97.5%.
