#!/usr/bin/env python3
"""EDA script for the Iris dataset.

Loads the Iris dataset from sklearn, builds a pandas DataFrame,
and uses the visualization utilities from utils/viz.py to generate
a full suite of exploratory data analysis plots.
"""

import sys
sys.path.insert(0, ".")

import os
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from datetime import datetime

from utils.viz import (
    plot_distributions,
    plot_target_distribution,
    plot_correlation_matrix,
    plot_missing_values,
    plot_outliers,
    plot_pairplot,
)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
OUTPUT_DIR = "project/visualizations/eda"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# 1. Load dataset
# ---------------------------------------------------------------------------
print("=" * 60)
print("Iris Dataset — Exploratory Data Analysis")
print("=" * 60)

iris = load_iris()
feature_names = iris.feature_names
target_names = iris.target_names

df = pd.DataFrame(iris.data, columns=feature_names)
df["target"] = iris.target
df["species"] = df["target"].map({i: name for i, name in enumerate(target_names)})

print(f"\nDataset shape: {df.shape}")
print(f"Features: {feature_names}")
print(f"Target classes: {list(target_names)}")
print(f"\nFirst 5 rows:\n{df.head()}")
print(f"\nDescriptive statistics:\n{df.describe()}")
print(f"\nClass distribution:\n{df['species'].value_counts()}")

# ---------------------------------------------------------------------------
# 2. Generate plots
# ---------------------------------------------------------------------------
numeric_cols = list(feature_names)

# 2a. Feature distributions
print("\n[1/6] Plotting feature distributions...")
plot_distributions(
    df,
    columns=numeric_cols,
    save_path=os.path.join(OUTPUT_DIR, "feature_distributions.png"),
)

# 2b. Target distribution
print("[2/6] Plotting target distribution...")
plot_target_distribution(
    df["species"],
    name="species",
    save_path=os.path.join(OUTPUT_DIR, "target_distribution.png"),
)

# 2c. Correlation matrix
print("[3/6] Plotting correlation matrix...")
plot_correlation_matrix(
    df[numeric_cols],
    save_path=os.path.join(OUTPUT_DIR, "correlation_matrix.png"),
)

# 2d. Missing values check
print("[4/6] Checking missing values...")
plot_missing_values(
    df,
    save_path=os.path.join(OUTPUT_DIR, "missing_values.png"),
)

# 2e. Outlier detection
print("[5/6] Plotting outlier box plots...")
plot_outliers(
    df,
    columns=numeric_cols,
    save_path=os.path.join(OUTPUT_DIR, "outliers.png"),
)

# 2f. Pairplot
print("[6/6] Plotting pairplot (this may take a moment)...")
plot_pairplot(
    df,
    target_col="species",
    max_features=4,
    save_path=os.path.join(OUTPUT_DIR, "pairplot.png"),
)

# ---------------------------------------------------------------------------
# 3. Write EDA summary
# ---------------------------------------------------------------------------
print("\nWriting EDA summary...")

# Compute summary statistics for the report
desc = df[numeric_cols].describe()
corr = df[numeric_cols].corr()

# Find highly correlated pairs
high_corr_pairs = []
for i in range(len(numeric_cols)):
    for j in range(i + 1, len(numeric_cols)):
        r = corr.iloc[i, j]
        if abs(r) >= 0.7:
            high_corr_pairs.append((numeric_cols[i], numeric_cols[j], r))
high_corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)

# Detect outliers via IQR method
outlier_info = {}
for col in numeric_cols:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    n_outliers = int(((df[col] < lower) | (df[col] > upper)).sum())
    if n_outliers > 0:
        outlier_info[col] = n_outliers

missing_total = int(df.isnull().sum().sum())

summary_md = f"""# EDA Summary: Iris Dataset

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Dataset Overview

| Property | Value |
|----------|-------|
| Samples | {len(df)} |
| Features | {len(numeric_cols)} |
| Target classes | {len(target_names)} ({', '.join(target_names)}) |
| Missing values | {missing_total} |

## Feature Statistics

| Feature | Mean | Std | Min | Max |
|---------|------|-----|-----|-----|
"""

for col in numeric_cols:
    summary_md += (
        f"| {col} | {desc.loc['mean', col]:.2f} | {desc.loc['std', col]:.2f} "
        f"| {desc.loc['min', col]:.1f} | {desc.loc['max', col]:.1f} |\n"
    )

summary_md += f"""
## Class Distribution

| Class | Count | Percentage |
|-------|-------|------------|
"""
for name in target_names:
    count = int((df["species"] == name).sum())
    pct = count / len(df) * 100
    summary_md += f"| {name} | {count} | {pct:.1f}% |\n"

summary_md += """
## Correlation Analysis

### Highly Correlated Feature Pairs (|r| >= 0.7)

| Feature A | Feature B | Correlation |
|-----------|-----------|-------------|
"""
if high_corr_pairs:
    for a, b, r in high_corr_pairs:
        summary_md += f"| {a} | {b} | {r:.3f} |\n"
else:
    summary_md += "| — | — | No highly correlated pairs found |\n"

summary_md += f"""
## Missing Values

{"No missing values detected in any feature." if missing_total == 0 else f"Total missing values: {missing_total}"}

## Outlier Detection (IQR Method)

"""
if outlier_info:
    summary_md += "| Feature | Outlier Count |\n|---------|---------------|\n"
    for col, n in outlier_info.items():
        summary_md += f"| {col} | {n} |\n"
else:
    summary_md += "No outliers detected using the 1.5*IQR rule.\n"

summary_md += f"""
## Generated Visualizations

| Plot | File |
|------|------|
| Feature distributions | `feature_distributions.png` |
| Target distribution | `target_distribution.png` |
| Correlation matrix | `correlation_matrix.png` |
| Missing values | `missing_values.png` |
| Outlier box plots | `outliers.png` |
| Feature pairplot | `pairplot.png` |

## Key Observations

1. **Balanced classes:** All three species have exactly 50 samples each (perfectly balanced).
2. **No missing data:** The dataset is complete with zero missing values.
3. **Strong correlations:** Petal length and petal width are highly correlated, as are sepal length and petal length/width. This suggests potential redundancy among petal-related features.
4. **Separability:** The pairplot reveals that *setosa* is linearly separable from the other two classes on most feature pairs. *Versicolor* and *virginica* show more overlap, particularly in sepal measurements.
5. **Outliers:** A small number of outliers exist in sepal width, but overall the feature distributions are well-behaved.
"""

summary_path = os.path.join(OUTPUT_DIR, "eda_summary.md")
with open(summary_path, "w") as f:
    f.write(summary_md)
print(f"Saved: {summary_path}")

print("\n" + "=" * 60)
print("EDA complete. All outputs saved to:", OUTPUT_DIR)
print("=" * 60)
