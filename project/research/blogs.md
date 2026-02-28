# Practical Resources: iris-classifier

## Implementation Guides

### scikit-learn Documentation
- **URL:** https://scikit-learn.org/stable/auto_examples/datasets/plot_iris_dataset.html
- **Content:** Official example showing Iris dataset loading and basic visualization.
- **Usefulness:** Canonical reference for data loading and API usage.

### scikit-learn Classifier Comparison
- **URL:** https://scikit-learn.org/stable/auto_examples/classification/plot_classifier_comparison.html
- **Content:** Side-by-side comparison of classifiers (KNN, SVM, RF, etc.) on 2D datasets including Iris projections.
- **Usefulness:** Visual intuition for how different decision boundaries look on this data.

## Code Patterns

### Minimal Baseline (LogisticRegression)
```python
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

X, y = load_iris(return_X_y=True)
scores = cross_val_score(LogisticRegression(max_iter=200), X, y, cv=5, scoring='accuracy')
print(f"Accuracy: {scores.mean():.3f} +/- {scores.std():.3f}")
```

### Full Pipeline with GridSearchCV
```python
from sklearn.datasets import load_iris
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.metrics import classification_report

X, y = load_iris(return_X_y=True)
param_grid = {'C': [0.1, 1, 10], 'gamma': ['scale', 'auto'], 'kernel': ['rbf']}
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
grid = GridSearchCV(SVC(), param_grid, cv=cv, scoring='accuracy', refit=True)
grid.fit(X, y)
print(f"Best: {grid.best_score_:.3f} with {grid.best_params_}")
```

## Key Takeaways from Community
- Always use stratified k-fold CV on Iris; single splits are unreliable with 150 samples.
- Petal features alone often achieve the same accuracy as all 4 features.
- Feature scaling matters for SVM and KNN but not for tree-based models.
- No need for feature engineering -- raw features work well.
