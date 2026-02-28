# Problem Specification

## Project Name
{project_name}

## Problem Statement
{Clear description of what we're trying to solve}

## Problem Type
{classification | regression | generation | clustering | ranking | other}

## Domain
{NLP | computer vision | tabular | time series | audio | multimodal | other}

## Data

### Source
{Where the data comes from — path, URL, API, etc.}

### Format
{CSV, Parquet, images, text files, etc.}

### Size
- Rows: {N}
- Features: {N}
- Disk size: {size}
- Classes/categories: {N} (if applicable)

### Schema
| Column | Type | Description | Notes |
|--------|------|-------------|-------|
| ... | ... | ... | ... |

### Quality Notes
- Missing values: {description}
- Class balance: {description}
- Known issues: {description}
- Labeling method: {description}

## Success Criteria

### Primary Metric
- **Metric:** {metric_name}
- **Target:** >= {value}
- **Mode:** {higher is better | lower is better}

### Secondary Metrics
- {metric_name}: target {value}
- {metric_name}: target {value}

### Business Constraints
- Latency: {requirement or N/A}
- Model size: {requirement or N/A}
- Interpretability: {requirement or N/A}
- Other: {requirement or N/A}

## Compute Environment

### Platform
{local machine | Lambda Labs | RunPod | Colab | AWS | GCP | Azure | other}

### Hardware
- GPU: {model and count, or "CPU-only"}
- RAM: {amount}
- Storage: {amount}

### Connection
{How to run training — local terminal, SSH command, API call, web UI, etc.}

### Special Considerations
{MPS backend for Mac, CUDA version requirements, memory limitations, etc.}

## Preferences
- Framework: {PyTorch | sklearn | XGBoost | auto | etc.}
- Time budget: {description}
- Previous approaches tried: {description or "None"}
- Approaches to avoid: {description or "None"}

## Notes
{Any additional context from the user}
