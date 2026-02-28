"""Run all Iris classifier experiments with MLflow tracking."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

from utils.mlflow_helper import init_mlflow, start_run, log_params, log_metrics, log_artifact
from utils.metrics import compute_metrics
from utils.config import load_config
from utils.viz import plot_confusion_matrix, plot_comparison_bar

# Load data
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42, stratify=iris.target
)

# Init MLflow
init_mlflow("iris-classifier")

# Define models from configs
configs_dir = os.path.join(os.path.dirname(__file__), '..', 'configs')
viz_dir = os.path.join(os.path.dirname(__file__), '..', 'visualizations', 'training')
results_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
os.makedirs(viz_dir, exist_ok=True)
os.makedirs(results_dir, exist_ok=True)

MODEL_MAP = {
    "LogisticRegression": LogisticRegression,
    "RandomForestClassifier": RandomForestClassifier,
    "SVC": SVC,
    "KNeighborsClassifier": KNeighborsClassifier,
}

config_files = sorted([f for f in os.listdir(configs_dir) if f.endswith('.yaml')])
all_results = []

for config_file in config_files:
    config = load_config(os.path.join(configs_dir, config_file))
    run_name = config["run_name"]
    run_id = config["run_id"]
    model_type = config["model"]["type"]
    model_params = config["model"]["params"]
    metric_names = config["evaluation"]["metrics"]

    print(f"\n{'='*60}")
    print(f"Run {run_id}: {run_name} ({model_type})")
    print(f"{'='*60}")

    # Build model
    model_class = MODEL_MAP[model_type]
    model = model_class(**model_params)

    # Cross-validation on training set
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
    print(f"  CV accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

    # Train on full training set
    model.fit(X_train, y_train)

    # Predict
    y_pred = model.predict(X_test)

    # Compute metrics
    metrics = compute_metrics(y_test, y_pred, metric_names)
    print(f"  Test metrics: {metrics}")

    # Log to MLflow
    with start_run(run_name=run_name, tags=config["mlflow"].get("tags", {})):
        log_params(config["model"]["params"], prefix="model")
        log_params({"model_type": model_type, "cv_folds": 5})
        log_metrics(metrics)
        log_metrics({"cv_accuracy_mean": cv_scores.mean(), "cv_accuracy_std": cv_scores.std()})

        # Confusion matrix
        cm_path = os.path.join(viz_dir, f"run_{run_id}_confusion_matrix.png")
        plot_confusion_matrix(y_test, y_pred, labels=iris.target_names, save_path=cm_path)
        log_artifact(cm_path)

    # Store for comparison
    all_results.append({
        "run_name": run_name,
        "run_id": run_id,
        "model_type": model_type,
        "metrics": metrics,
        "cv_mean": cv_scores.mean(),
        "cv_std": cv_scores.std(),
    })

    # Write result markdown
    result_md = f"""# Experiment Result

## Run ID: {run_id}
## Run Name: {run_name}
## Status: success

## Configuration
- **Model:** {model_type}
- **Key parameters:** {model_params}
- **Config file:** `project/configs/{config_file}`

## Results

### Primary Metric
- **accuracy:** {metrics['accuracy']:.4f}

### All Metrics
| Metric | Test |
|--------|------|
| accuracy | {metrics['accuracy']:.4f} |
| f1 | {metrics['f1']:.4f} |
| precision | {metrics['precision']:.4f} |
| recall | {metrics['recall']:.4f} |

### Cross-Validation
- **CV accuracy:** {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})

## Visualizations
- Confusion matrix: `project/visualizations/training/run_{run_id}_confusion_matrix.png`

## Analysis
{run_name} achieved {metrics['accuracy']:.1%} test accuracy with 5-fold CV accuracy of {cv_scores.mean():.1%}.
"""
    with open(os.path.join(results_dir, f"run_{run_id}_result.md"), "w") as f:
        f.write(result_md)

# --- Cross-Run Comparison ---
print(f"\n{'='*60}")
print("CROSS-RUN COMPARISON")
print(f"{'='*60}")

analysis_dir = os.path.join(os.path.dirname(__file__), '..', 'visualizations', 'analysis')
os.makedirs(analysis_dir, exist_ok=True)

# Comparison bar chart
bar_path = os.path.join(analysis_dir, "accuracy_comparison.png")
plot_comparison_bar(all_results, "accuracy", save_path=bar_path)

# Print summary table
print(f"\n{'Run':<25} {'Accuracy':>10} {'F1':>10} {'CV Mean':>10}")
print("-" * 55)
best_acc = 0
best_name = ""
for r in all_results:
    acc = r["metrics"]["accuracy"]
    f1 = r["metrics"]["f1"]
    print(f"{r['run_name']:<25} {acc:>10.4f} {f1:>10.4f} {r['cv_mean']:>10.4f}")
    if acc > best_acc:
        best_acc = acc
        best_name = r["run_name"]

print(f"\nBest model: {best_name} (accuracy={best_acc:.4f})")

# Write iteration report
report = f"""# Iteration Report

## Project: iris-classifier
## Iteration: 1
## Date: 2026-02-28

## Summary
Ran 4 classifiers on the Iris dataset. All models achieved strong performance on this well-separated dataset.

## Experiments Run

| Run | Model | Accuracy | F1 | CV Mean |
|-----|-------|----------|-----|---------|
"""
for r in all_results:
    report += f"| {r['run_id']} | {r['run_name']} | {r['metrics']['accuracy']:.4f} | {r['metrics']['f1']:.4f} | {r['cv_mean']:.4f} |\n"

report += f"""
## Best Result
- **Run:** {best_name}
- **Accuracy:** {best_acc:.4f}

## Visualizations
- Comparison chart: `project/visualizations/analysis/accuracy_comparison.png`
- Per-run confusion matrices: `project/visualizations/training/`

## MLflow Summary
- Experiment: iris-classifier
- Total runs: {len(all_results)}
- View: `mlflow ui --backend-store-uri file:./mlruns`
"""

with open(os.path.join(os.path.dirname(__file__), '..', 'iteration_report.md'), "w") as f:
    f.write(report)

print("\nAll results written to project/results/")
print("Comparison chart saved to project/visualizations/analysis/")
print("Iteration report saved to project/iteration_report.md")
print("Done!")
