# Visualization Plan

## Project: {project_name}
## Date: {date}

## Phase 2: EDA Visualizations

### Required
- [ ] Feature distributions (histograms/KDE)
- [ ] Target variable distribution
- [ ] Correlation matrix heatmap
- [ ] Missing value analysis
- [ ] Outlier detection plots

### Domain-Specific
- [ ] {domain-specific plot 1}
- [ ] {domain-specific plot 2}

### Output Directory
`project/visualizations/eda/`

## Phase 4: Training Visualizations

### Per-Run (automated)
- [ ] Loss curves (train + validation)
- [ ] Primary metric progression
- [ ] Learning rate schedule
- [ ] {model-specific plot}

### Output Directory
`project/visualizations/training/run_{run_id}/`

## Phase 5: Analysis Visualizations

### Cross-Run Comparison
- [ ] Metric comparison bar chart
- [ ] Training curve overlay
- [ ] Parameter sensitivity plots
- [ ] Best model detailed evaluation

### Model-Specific Evaluation
- [ ] {Confusion matrix / residual plot / etc.}
- [ ] {ROC/PR curve / predicted vs actual / etc.}

### Summary Figure
- [ ] Single figure telling the experiment story

### Output Directory
`project/visualizations/analysis/`

## Novel Visualization Ideas
{Search for domain-specific or cutting-edge visualization techniques}
- {Idea 1}
- {Idea 2}

## Style Guide
- Backend: matplotlib + seaborn (static), plotly (interactive)
- Figure size: 10x6 default, 12x8 for complex plots
- Color palette: seaborn default
- Font size: 12pt labels, 14pt titles
- Always include: title, axis labels, legend (if multiple series)
- Save format: PNG (300 DPI) + HTML (for interactive)
