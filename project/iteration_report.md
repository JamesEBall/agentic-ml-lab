# Iteration Report

## Project: iris-classifier
## Iteration: 1
## Date: 2026-02-28

## Summary
Ran 4 classifiers on the Iris dataset. All models achieved strong performance on this well-separated dataset.

## Experiments Run

| Run | Model | Accuracy | F1 | CV Mean |
|-----|-------|----------|-----|---------|
| 001 | logistic_regression | 0.9667 | 0.9666 | 0.9667 |
| 002 | random_forest | 0.9000 | 0.8997 | 0.9500 |
| 003 | svm_rbf | 0.9667 | 0.9666 | 0.9750 |
| 004 | knn | 1.0000 | 1.0000 | 0.9750 |

## Best Result
- **Run:** knn
- **Accuracy:** 1.0000

## Visualizations
- Comparison chart: `project/visualizations/analysis/accuracy_comparison.png`
- Per-run confusion matrices: `project/visualizations/training/`

## MLflow Summary
- Experiment: iris-classifier
- Total runs: 4
- View: `mlflow ui --backend-store-uri file:./mlruns`
