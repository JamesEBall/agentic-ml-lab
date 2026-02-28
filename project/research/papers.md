# Key Papers: iris-classifier

## Foundational

### 1. Fisher, R.A. (1936) "The use of multiple measurements in taxonomic problems"
- **Publication:** Annals of Eugenics, 7(2), 179-188
- **Key takeaway:** Introduced Linear Discriminant Analysis (LDA) and demonstrated that linear combinations of measurements can effectively separate biological species. The Iris dataset originated here.
- **Relevance:** Establishes that linear separability is a core property of this dataset.

### 2. Anderson, E. (1935) "The irises of the Gaspe Peninsula"
- **Publication:** Bulletin of the American Iris Society, 59, 2-5
- **Key takeaway:** The botanical study that collected the original 150 Iris measurements across three species. Provides the ground truth and biological context.
- **Relevance:** Data provenance -- understanding what the features physically represent.

## Reference Textbooks

### 3. Duda, R.O., Hart, P.E., Stork, D.G. "Pattern Classification" (2nd ed., 2001)
- **Key takeaway:** Uses Iris as a running example throughout. Provides detailed analysis of decision boundaries, feature space geometry, and classifier comparison on this dataset.
- **Relevance:** Standard reference for understanding why different classifiers perform as they do on Iris.

### 4. Hastie, T., Tibshirani, R., Friedman, J. "The Elements of Statistical Learning" (2nd ed., 2009)
- **Key takeaway:** Covers the statistical foundations of all methods we plan to use (logistic regression, SVM, random forests, KNN). Uses Iris and similar small datasets as examples.
- **Relevance:** Theoretical justification for model selection and regularization choices.

## Notes
The Iris dataset is a pedagogical benchmark, not an active research frontier. No recent papers push SOTA on this dataset specifically. The references above provide all the theoretical grounding needed.
