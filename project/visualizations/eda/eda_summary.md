# EDA Summary: Iris Dataset

**Generated:** 2026-02-28 22:30:23

## Dataset Overview

| Property | Value |
|----------|-------|
| Samples | 150 |
| Features | 4 |
| Target classes | 3 (setosa, versicolor, virginica) |
| Missing values | 0 |

## Feature Statistics

| Feature | Mean | Std | Min | Max |
|---------|------|-----|-----|-----|
| sepal length (cm) | 5.84 | 0.83 | 4.3 | 7.9 |
| sepal width (cm) | 3.06 | 0.44 | 2.0 | 4.4 |
| petal length (cm) | 3.76 | 1.77 | 1.0 | 6.9 |
| petal width (cm) | 1.20 | 0.76 | 0.1 | 2.5 |

## Class Distribution

| Class | Count | Percentage |
|-------|-------|------------|
| setosa | 50 | 33.3% |
| versicolor | 50 | 33.3% |
| virginica | 50 | 33.3% |

## Correlation Analysis

### Highly Correlated Feature Pairs (|r| >= 0.7)

| Feature A | Feature B | Correlation |
|-----------|-----------|-------------|
| petal length (cm) | petal width (cm) | 0.963 |
| sepal length (cm) | petal length (cm) | 0.872 |
| sepal length (cm) | petal width (cm) | 0.818 |

## Missing Values

No missing values detected in any feature.

## Outlier Detection (IQR Method)

| Feature | Outlier Count |
|---------|---------------|
| sepal width (cm) | 4 |

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
