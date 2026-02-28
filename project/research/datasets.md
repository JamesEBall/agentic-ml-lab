# Dataset Discovery: iris-classifier

## Primary Dataset

### Iris (Fisher's Iris)
- **Source:** `sklearn.datasets.load_iris` (also available from UCI ML Repository)
- **Size:** 150 samples, 4 features, 3 classes
- **Format:** NumPy arrays via scikit-learn; CSV from UCI
- **License:** Public domain
- **Features:** sepal_length, sepal_width, petal_length, petal_width (all float, cm)
- **Target:** species -- setosa (0), versicolor (1), virginica (2)
- **Class balance:** Perfectly balanced (50 per class)
- **Quality:** No missing values, no noise, no duplicates. Clean benchmark data.
- **Provenance:** Collected by Edgar Anderson (1935), published by R.A. Fisher (1936).

## Supplementary Datasets
None required. The scikit-learn built-in version is the canonical dataset and is identical to the UCI repository version.

## Data Loading
```python
from sklearn.datasets import load_iris

data = load_iris()
X, y = data.data, data.target
feature_names = data.feature_names
target_names = data.target_names
```

## Notes
- The dataset is small enough to fit entirely in memory with negligible footprint.
- No preprocessing or cleaning steps are needed.
- Stratified splitting is recommended due to the small size (150 samples).
