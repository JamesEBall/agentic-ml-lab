# Problem Specification

## Project Name
iris-classifier

## Problem Statement
Build a classifier for the classic Iris dataset — predict flower species (setosa, versicolor, virginica) from sepal and petal measurements.

## Problem Type
classification

## Domain
tabular

## Data

### Source
sklearn.datasets.load_iris (built-in, no download required)

### Format
In-memory NumPy arrays via scikit-learn

### Size
- Rows: 150
- Features: 4
- Disk size: ~5 KB
- Classes/categories: 3 (setosa, versicolor, virginica)

### Schema
| Column | Type | Description | Notes |
|--------|------|-------------|-------|
| sepal_length | float | Sepal length in cm | |
| sepal_width | float | Sepal width in cm | |
| petal_length | float | Petal length in cm | |
| petal_width | float | Petal width in cm | |
| species | int (0,1,2) | Target: setosa, versicolor, virginica | |

### Quality Notes
- Missing values: None
- Class balance: Perfectly balanced (50 per class)
- Known issues: None — clean benchmark dataset
- Labeling method: Ground truth botanical classification

## Success Criteria

### Primary Metric
- **Metric:** accuracy
- **Target:** >= 0.95
- **Mode:** higher is better

### Secondary Metrics
- f1: target >= 0.95 (weighted)
- precision: track
- recall: track

### Business Constraints
- Latency: N/A
- Model size: N/A
- Interpretability: Nice to have (feature importance)
- Other: N/A

## Compute Environment

### Platform
Local machine (macOS)

### Hardware
- GPU: Apple M1 Pro (14-core GPU), MPS backend available
- RAM: 16 GB
- Storage: Ample

### Connection
Local terminal — run scripts directly

### Special Considerations
- MPS backend available via `torch.device("mps")` but sklearn models run on CPU (fine for this dataset size)
- Dataset is tiny (150 rows) — all models will train in seconds

## Preferences
- Framework: scikit-learn (appropriate for tabular + small dataset)
- Time budget: Quick test (~5 minutes total)
- Previous approaches tried: None
- Approaches to avoid: None

## Notes
This is a test run to validate the Agentic ML Research Lab framework end-to-end.
