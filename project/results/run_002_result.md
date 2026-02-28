# Experiment Result

## Run ID: 002
## Run Name: random_forest
## Status: success

## Configuration
- **Model:** RandomForestClassifier
- **Key parameters:** {'n_estimators': 100, 'random_state': 42}
- **Config file:** `project/configs/run_002_random_forest.yaml`

## Results

### Primary Metric
- **accuracy:** 0.9000

### All Metrics
| Metric | Test |
|--------|------|
| accuracy | 0.9000 |
| f1 | 0.8997 |
| precision | 0.9024 |
| recall | 0.9000 |

### Cross-Validation
- **CV accuracy:** 0.9500 (+/- 0.0167)

## Visualizations
- Confusion matrix: `project/visualizations/training/run_002_confusion_matrix.png`

## Analysis
random_forest achieved 90.0% test accuracy with 5-fold CV accuracy of 95.0%.
