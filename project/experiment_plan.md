# Experiment Plan

## Project: iris-classifier
## Date: 2026-02-28
## Status: approved

## Objective
Find the best classifier for the Iris dataset, establishing baselines and comparing standard approaches.

## Experiment Sequence

### Run 001: logistic_regression (Baseline)
- **Model:** LogisticRegression
- **Key params:** max_iter=200, random_state=42
- **Purpose:** Establish performance floor with simplest linear model
- **Success criteria:** accuracy > 0.90
- **Estimated runtime:** <1 second

### Run 002: random_forest
- **Model:** RandomForestClassifier
- **Key params:** n_estimators=100, random_state=42
- **Change from previous:** Non-linear ensemble method
- **Purpose:** Test if non-linearity improves over linear baseline
- **Success criteria:** accuracy > 0.95
- **Estimated runtime:** <1 second

### Run 003: svm_rbf
- **Model:** SVC (RBF kernel)
- **Key params:** kernel=rbf, C=1.0, gamma=scale, random_state=42
- **Change from previous:** Kernel method for non-linear boundaries
- **Purpose:** Test SVM which historically does well on Iris
- **Success criteria:** accuracy > 0.95
- **Estimated runtime:** <1 second

### Run 004: knn
- **Model:** KNeighborsClassifier
- **Key params:** n_neighbors=5
- **Change from previous:** Instance-based learning, no training phase
- **Purpose:** Test simple distance-based approach
- **Success criteria:** accuracy > 0.95
- **Estimated runtime:** <1 second

## Stopping Criteria
- **Success:** accuracy >= 0.95 for 2+ runs
- **Diminishing returns:** N/A (only 4 quick runs)
- **Budget:** Maximum 4 runs
- **Failure:** All runs below 0.90 → re-evaluate (unlikely for Iris)

## Data Split
- Train: 80%
- Validation: 0% (using cross-validation instead given small dataset)
- Test: 20% (held out for final evaluation)
- Cross-validation: Yes, 5-fold on training set

## Visualization Plan
- Per-run: confusion matrix, classification report
- Cross-run: accuracy comparison bar chart, metric progression
- Final: summary figure with best model evaluation

## Decision Framework
After each run, compare to baseline and previous best. Since all runs are fast, run all 4 then compare.
