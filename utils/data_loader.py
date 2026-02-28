"""Data loading and validation utilities for the Agentic ML Research Lab."""

import os
import numpy as np
import pandas as pd


def load_data(data_config: dict) -> dict:
    """Load data according to a config specification.

    Args:
        data_config: Dict with keys:
            - source: Path to file, directory, or HuggingFace dataset name
            - format: (optional) csv, parquet, json, excel, hf (auto-detected if omitted)
            - train_split: (optional) fraction for training, default 0.8
            - val_split: (optional) fraction for validation, default 0.1
            - test_split: (optional) fraction for test, default 0.1
            - target: (optional) target column name
            - seed: (optional) random seed for splitting

    Returns:
        Dict with keys: 'train', 'val', 'test', 'full', 'target_col', 'feature_cols'
        Each split is a pandas DataFrame.
    """
    source = data_config["source"]
    fmt = data_config.get("format", _detect_format(source))

    # Load the full dataset
    if fmt == "hf":
        df = _load_huggingface(source, data_config)
    elif fmt == "csv":
        df = pd.read_csv(source)
    elif fmt == "parquet":
        df = pd.read_parquet(source)
    elif fmt == "json":
        df = pd.read_json(source)
    elif fmt == "excel":
        df = pd.read_excel(source)
    elif fmt == "tsv":
        df = pd.read_csv(source, sep="\t")
    elif fmt == "dir":
        df = _load_directory(source)
    else:
        raise ValueError(f"Unsupported format: {fmt}. Use csv, parquet, json, excel, hf, or dir.")

    target_col = data_config.get("target")
    feature_cols = [c for c in df.columns if c != target_col] if target_col else list(df.columns)

    # Split
    train_frac = data_config.get("train_split", 0.8)
    val_frac = data_config.get("val_split", 0.1)
    test_frac = data_config.get("test_split", 0.1)
    seed = data_config.get("seed", 42)

    train, val, test = _split_data(df, train_frac, val_frac, test_frac, seed)

    return {
        "full": df,
        "train": train,
        "val": val,
        "test": test,
        "target_col": target_col,
        "feature_cols": feature_cols,
    }


def validate_data(df: pd.DataFrame) -> dict:
    """Run basic validation checks on a DataFrame.

    Returns dict with validation results.
    """
    results = {
        "shape": df.shape,
        "dtypes": df.dtypes.value_counts().to_dict(),
        "missing_total": int(df.isnull().sum().sum()),
        "missing_by_column": df.isnull().sum().to_dict(),
        "missing_pct": (df.isnull().sum() / len(df) * 100).to_dict(),
        "duplicates": int(df.duplicated().sum()),
        "constant_columns": [c for c in df.columns if df[c].nunique() <= 1],
        "high_cardinality": [c for c in df.select_dtypes(include=["object"]).columns
                            if df[c].nunique() > 100],
    }

    # Numeric summary
    numeric = df.select_dtypes(include=[np.number])
    if len(numeric.columns) > 0:
        results["numeric_summary"] = numeric.describe().to_dict()

    return results


def data_summary(df: pd.DataFrame) -> str:
    """Generate a human-readable data summary string."""
    lines = [
        f"Shape: {df.shape[0]} rows x {df.shape[1]} columns",
        f"Memory: {df.memory_usage(deep=True).sum() / 1024 / 1024:.1f} MB",
        "",
        "Column Types:",
    ]
    for dtype, count in df.dtypes.value_counts().items():
        lines.append(f"  {dtype}: {count}")

    missing = df.isnull().sum()
    if missing.sum() > 0:
        lines.append(f"\nMissing Values: {missing.sum()} total")
        for col in missing[missing > 0].index:
            pct = missing[col] / len(df) * 100
            lines.append(f"  {col}: {missing[col]} ({pct:.1f}%)")
    else:
        lines.append("\nNo missing values")

    dupes = df.duplicated().sum()
    if dupes > 0:
        lines.append(f"\nDuplicate rows: {dupes}")

    return "\n".join(lines)


def _detect_format(source: str) -> str:
    """Auto-detect data format from file extension or source type."""
    if source.startswith(("hf:", "huggingface:")):
        return "hf"
    ext = os.path.splitext(source)[1].lower()
    format_map = {
        ".csv": "csv",
        ".tsv": "tsv",
        ".parquet": "parquet",
        ".pq": "parquet",
        ".json": "json",
        ".jsonl": "json",
        ".xlsx": "excel",
        ".xls": "excel",
    }
    if ext in format_map:
        return format_map[ext]
    if os.path.isdir(source):
        return "dir"
    # Try HuggingFace as fallback for non-path strings
    if not os.path.exists(source) and "/" in source:
        return "hf"
    return "csv"  # Default assumption


def _load_huggingface(source: str, config: dict) -> pd.DataFrame:
    """Load a HuggingFace dataset."""
    from datasets import load_dataset
    name = source.replace("hf:", "").replace("huggingface:", "")
    subset = config.get("subset")
    split = config.get("hf_split", "train")
    ds = load_dataset(name, subset, split=split)
    return ds.to_pandas()


def _load_directory(path: str) -> pd.DataFrame:
    """Load all CSV/Parquet files from a directory into one DataFrame."""
    dfs = []
    for f in sorted(os.listdir(path)):
        fp = os.path.join(path, f)
        if f.endswith(".csv"):
            dfs.append(pd.read_csv(fp))
        elif f.endswith(".parquet"):
            dfs.append(pd.read_parquet(fp))
    if not dfs:
        raise ValueError(f"No CSV or Parquet files found in {path}")
    return pd.concat(dfs, ignore_index=True)


def _split_data(df: pd.DataFrame, train_frac: float, val_frac: float,
                test_frac: float, seed: int):
    """Split DataFrame into train/val/test."""
    assert abs(train_frac + val_frac + test_frac - 1.0) < 1e-6, \
        f"Splits must sum to 1.0, got {train_frac + val_frac + test_frac}"
    n = len(df)
    rng = np.random.RandomState(seed)
    indices = rng.permutation(n)

    train_end = int(n * train_frac)
    val_end = train_end + int(n * val_frac)

    train = df.iloc[indices[:train_end]].reset_index(drop=True)
    val = df.iloc[indices[train_end:val_end]].reset_index(drop=True)
    test = df.iloc[indices[val_end:]].reset_index(drop=True)

    return train, val, test
