# Experiment Result

## Run ID: 004
## Run Name: knn
## Status: success

## Configuration
- **Model:** KNeighborsClassifier
- **Key parameters:** {'n_neighbors': 5}
- **Config file:** `project/configs/run_004_knn.yaml`

## Results

### Primary Metric
- **accuracy:** 1.0000

### All Metrics
| Metric | Test |
|--------|------|
| accuracy | 1.0000 |
| f1 | 1.0000 |
| precision | 1.0000 |
| recall | 1.0000 |

### Cross-Validation
- **CV accuracy:** 0.9750 (+/- 0.0333)

## Visualizations
- Confusion matrix: `project/visualizations/training/run_004_confusion_matrix.png`

## Analysis
knn achieved 100.0% test accuracy with 5-fold CV accuracy of 97.5%.
