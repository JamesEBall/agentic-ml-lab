# Research Brief

## Project: iris-classifier
## Date: 2026-02-28

## Executive Summary
The Iris dataset is one of the most well-studied classification benchmarks in machine learning. Linear models already achieve ~96% accuracy because setosa is perfectly linearly separable from the other two classes. Near-perfect classification (97-100%) is achievable with nonlinear models such as SVM with RBF kernel or Random Forest, as only a small overlap region exists between versicolor and virginica.

## Recommended Approach
### Method
Start with LogisticRegression as a baseline, then progress through RandomForestClassifier and SVM (SVC with RBF kernel). LogisticRegression is the recommended primary model for its simplicity and strong performance; SVM or RandomForest can push accuracy to near-perfect if needed.

### Justification
- The dataset has only 150 samples and 4 features -- simple models generalize well and complex models risk overfitting.
- Scikit-learn provides all necessary implementations with minimal setup.
- LogisticRegression establishes a strong interpretable baseline (~96% accuracy).
- SVM with RBF kernel and RandomForest are known to achieve 97-100% on this dataset with proper cross-validation.
- The small dataset size means all models train in under a second, so there is no computational reason to avoid trying multiple approaches.

### Expected Performance
| Metric   | SOTA          | Strong Baseline | Our Target |
|----------|---------------|-----------------|------------|
| Accuracy | 97-100%       | ~96%            | >= 95%     |
| F1 (weighted) | 97-100% | ~96%            | >= 95%     |

## Baseline Strategy
LogisticRegression with default scikit-learn parameters and stratified 5-fold cross-validation. This requires roughly 5 lines of code and typically yields ~96% accuracy. No feature engineering, no hyperparameter tuning -- just load data, fit, and evaluate.

## Research Findings

### Datasets
- **Primary:** `sklearn.datasets.load_iris` -- 150 samples, 4 features, 3 classes, perfectly balanced (50 per class), no missing values.
- **Supplementary:** None needed. The built-in dataset is the canonical version of Fisher's 1936 Iris data.
- **Benchmark:** UCI Machine Learning Repository Iris dataset (identical data, used as the standard benchmark reference).

### Benchmarks & SOTA
| Model              | Typical Accuracy | Notes                                      |
|--------------------|------------------|--------------------------------------------|
| LogisticRegression | ~96%             | Strong linear baseline                     |
| KNN (k=3-5)       | ~96-97%          | Simple, no training, sensitive to k        |
| RandomForest       | ~95-97%          | Robust, provides feature importance        |
| SVM (RBF kernel)   | ~97-98%          | Best general-purpose performer             |
| LDA                | ~98%             | Exploits class separability directly       |
| Neural Network     | ~96-98%          | Overkill for this dataset size             |
| Perfect score      | 100%             | Achievable with favorable train/test split |

Note: Variance across random splits is significant given only 150 samples. Use stratified k-fold cross-validation (k=5 or k=10) for reliable estimates.

### Key Papers
1. **Fisher, R.A. (1936) "The use of multiple measurements in taxonomic problems"** -- The original paper introducing the dataset and Linear Discriminant Analysis. Demonstrated that linear methods suffice for separating Iris species.
2. **Anderson, E. (1935) "The irises of the Gaspe Peninsula"** -- The botanical study that collected the original measurements. Important for understanding the data provenance.
3. **Duda, Hart & Stork, "Pattern Classification" (textbook)** -- Uses Iris extensively as a teaching example for classification algorithms. Provides detailed analysis of decision boundaries.

### Practical Resources
- Best implementation guide: scikit-learn documentation on classification (`sklearn.datasets.load_iris` example)
- Reusable code: scikit-learn's built-in dataset loader eliminates all data preparation
- Pretrained models: Not applicable (dataset is too small to warrant pretrained models)

## EDA Highlights
- **Data shape:** 150 samples x 4 features, 3 balanced classes (50 each). No missing values, no outliers of concern.
- **Key distributions:** Petal length and petal width show strong bimodal/trimodal distributions corresponding to species. Sepal features overlap more across classes.
- **Correlations:** Petal length and petal width are highly correlated (r ~ 0.96). Sepal length correlates moderately with petal features. Sepal width has weak/negative correlation with other features.
- **Anomalies:** None. This is a clean, well-curated benchmark dataset.
- **Class separability:** Setosa is perfectly linearly separable from versicolor and virginica on petal features alone. Versicolor and virginica overlap slightly in petal length/width space (roughly 3-5 ambiguous samples).
- Visualizations: see `project/visualizations/eda/`

## Risks & Unknowns
1. **Small sample size creates high variance in evaluation.** Mitigation: Use stratified k-fold cross-validation (k=5 or k=10) rather than a single train/test split. Report mean and standard deviation of metrics.
2. **Overfitting risk with complex models.** Mitigation: Stick to simple models. If using RandomForest or SVM, limit complexity (e.g., fewer trees, regularization). Compare cross-validation score to training score to detect overfitting.
3. **This is a validation run, not a real-world problem.** Mitigation: Focus on establishing that the framework pipeline works end-to-end rather than chasing marginal accuracy gains. The goal is >= 95% accuracy, which is easily achievable.

## Suggested Experiment Sequence
1. **Baseline:** LogisticRegression with default parameters -- establish floor (~96% expected)
2. **Standard:** RandomForestClassifier with n_estimators=100, default params -- check ensemble performance (~95-97% expected)
3. **Tuned:** SVM (SVC with RBF kernel), tune C and gamma via GridSearchCV -- push toward best performance (~97-98% expected)
4. **Alternative:** KNeighborsClassifier (k=3, 5, 7) -- simple non-parametric check (~96-97% expected)
5. **Advanced:** If time allows, try LDA or a tuned RandomForest with feature importance analysis to add interpretability
