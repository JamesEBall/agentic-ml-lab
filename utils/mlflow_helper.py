"""MLflow tracking utilities for the Agentic ML Research Lab."""

import os
import mlflow
from mlflow.tracking import MlflowClient


TRACKING_URI = f"file:{os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mlruns')}"


def init_mlflow(experiment_name: str) -> str:
    """Initialize MLflow with the local tracking URI and create/get experiment.

    Returns the experiment ID.
    """
    mlflow.set_tracking_uri(TRACKING_URI)
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if experiment is None:
        experiment_id = mlflow.create_experiment(experiment_name)
    else:
        experiment_id = experiment.experiment_id
    mlflow.set_experiment(experiment_name)
    return experiment_id


def start_run(run_name: str, tags: dict | None = None):
    """Start an MLflow run. Use as a context manager.

    Example:
        with start_run("my_run", tags={"phase": "4"}) as run:
            log_params(config)
            log_metrics({"accuracy": 0.95})
    """
    return mlflow.start_run(run_name=run_name, tags=tags or {})


def log_params(config: dict, prefix: str = ""):
    """Log parameters from a (possibly nested) config dict.

    Flattens nested dicts with dot notation: {"model": {"lr": 0.01}} → "model.lr"
    """
    flat = _flatten_dict(config, prefix)
    # MLflow has a 500-param limit per batch; chunk if needed
    items = list(flat.items())
    for i in range(0, len(items), 100):
        batch = dict(items[i:i + 100])
        mlflow.log_params(batch)


def log_metrics(metrics: dict, step: int | None = None):
    """Log a dictionary of metrics. Optionally specify step for time-series."""
    mlflow.log_metrics(metrics, step=step)


def log_metric(key: str, value: float, step: int | None = None):
    """Log a single metric."""
    mlflow.log_metric(key, value, step=step)


def log_artifact(path: str):
    """Log a local file or directory as an artifact."""
    mlflow.log_artifact(path)


def log_artifacts(directory: str):
    """Log all files in a directory as artifacts."""
    mlflow.log_artifacts(directory)


def log_model(model, artifact_path: str = "model", **kwargs):
    """Log a model. Auto-detects framework (sklearn, pytorch, etc.)."""
    try:
        import sklearn
        if isinstance(model, sklearn.base.BaseEstimator):
            mlflow.sklearn.log_model(model, artifact_path, **kwargs)
            return
    except ImportError:
        pass

    try:
        import torch
        if isinstance(model, torch.nn.Module):
            mlflow.pytorch.log_model(model, artifact_path, **kwargs)
            return
    except ImportError:
        pass

    # Fallback: pickle the model
    import pickle
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".pkl", delete=False) as f:
        pickle.dump(model, f)
        mlflow.log_artifact(f.name, artifact_path)


def get_best_run(experiment_name: str, metric: str, mode: str = "max") -> dict | None:
    """Get the best run from an experiment by a metric.

    Args:
        experiment_name: Name of the MLflow experiment.
        metric: Metric to sort by.
        mode: "max" or "min".

    Returns:
        Dict with run_id, metrics, and params, or None if no runs.
    """
    client = MlflowClient(TRACKING_URI)
    experiment = client.get_experiment_by_name(experiment_name)
    if experiment is None:
        return None

    order = f"metrics.{metric} {'DESC' if mode == 'max' else 'ASC'}"
    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=[order],
        max_results=1,
    )

    if not runs:
        return None

    run = runs[0]
    return {
        "run_id": run.info.run_id,
        "run_name": run.info.run_name,
        "metrics": run.data.metrics,
        "params": run.data.params,
        "tags": run.data.tags,
    }


def compare_runs(experiment_name: str, metric: str, top_n: int = 10) -> list[dict]:
    """Get top N runs from an experiment sorted by metric (descending).

    Returns list of dicts with run_id, run_name, metrics, params.
    """
    client = MlflowClient(TRACKING_URI)
    experiment = client.get_experiment_by_name(experiment_name)
    if experiment is None:
        return []

    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=[f"metrics.{metric} DESC"],
        max_results=top_n,
    )

    return [
        {
            "run_id": r.info.run_id,
            "run_name": r.info.run_name,
            "metrics": r.data.metrics,
            "params": r.data.params,
        }
        for r in runs
    ]


def _flatten_dict(d: dict, prefix: str = "") -> dict:
    """Flatten a nested dict with dot-separated keys."""
    items = {}
    for k, v in d.items():
        key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            items.update(_flatten_dict(v, key))
        elif isinstance(v, (list, tuple)):
            items[key] = str(v)
        else:
            items[key] = v
    return items
