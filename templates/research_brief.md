# Research Brief

## Project: {project_name}
## Date: {date}

## Executive Summary
{2-3 sentence overview of findings and recommendation}

## Recommended Approach
### Method
{Recommended model/method and why}

### Justification
{Evidence from research supporting this choice}

### Expected Performance
{Based on benchmarks, what performance range to expect}

## Baseline Strategy
{Simplest viable approach for initial comparison — must be dead simple}

## Research Findings

### Datasets
{Summary from Dataset Discovery agent}
- Primary: {dataset}
- Supplementary: {datasets}
- Benchmark: {datasets}

### Benchmarks & SOTA
{Summary from Benchmark agent}
| Metric | SOTA | Strong Baseline | Our Target |
|--------|------|-----------------|------------|
| ... | ... | ... | ... |

### Key Papers
{Summary from Paper Search agent}
1. {Paper title} — {key takeaway}
2. {Paper title} — {key takeaway}
3. {Paper title} — {key takeaway}

### Practical Resources
{Summary from Blog & Material agent}
- Best implementation guide: {link}
- Reusable code: {link}
- Pretrained models: {list}

## EDA Highlights
{Key findings from Visualization agent's EDA}
- Data shape: {description}
- Key distributions: {description}
- Correlations: {description}
- Anomalies: {description}
- Visualizations: see `project/visualizations/eda/`

## Risks & Unknowns
1. {Risk/unknown and how to mitigate}
2. {Risk/unknown and how to mitigate}
3. {Risk/unknown and how to mitigate}

## Suggested Experiment Sequence
1. **Baseline:** {simple method} — establish floor
2. **Standard:** {recommended method with default params} — establish benchmark
3. **Tuned:** {recommended method with tuned params} — optimize
4. **Alternative:** {different approach} — check if we're on the right track
5. **Advanced:** {if time allows, try more complex approach}
