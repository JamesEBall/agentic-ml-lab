# Benchmarks & SOTA: iris-classifier

## Summary
The Iris dataset is a solved benchmark. Near-perfect classification (97-100%) is achievable with standard ML algorithms. The primary challenge is not accuracy but rather getting reliable estimates from only 150 samples.

## Benchmark Results (Stratified 5-Fold CV)

| Model                        | Accuracy (mean) | Notes                              |
|------------------------------|------------------|------------------------------------|
| LogisticRegression           | ~96%             | Linear baseline, fast, interpretable |
| LDA                          | ~98%             | Optimal for Gaussian class distributions |
| KNN (k=5)                    | ~96-97%          | No training phase, sensitive to k  |
| Decision Tree                | ~94-96%          | Prone to overfitting on small data |
| RandomForest (n=100)         | ~95-97%          | Robust, feature importance available |
| SVM (RBF, tuned C/gamma)     | ~97-98%          | Best general-purpose performance   |
| Gradient Boosting            | ~95-97%          | Marginal gain over RF on this data |
| Neural Network (MLP)         | ~96-98%          | Overkill, but works                |

## Key Observations
- All models exceed 94% accuracy, confirming the dataset is relatively easy.
- Variance across folds/splits is significant (2-4%) due to the small sample size.
- Setosa is always classified correctly; errors come from versicolor/virginica overlap.
- Single train/test splits can yield anywhere from 93% to 100% depending on which samples land in test set.

## Our Target
- Primary metric: Accuracy >= 95%
- This is comfortably within reach of even the simplest baseline (LogisticRegression).
