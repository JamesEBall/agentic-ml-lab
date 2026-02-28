"""Metric computation utilities for the Agentic ML Research Lab."""

import numpy as np


def compute_metrics(y_true, y_pred, metric_names: list[str], y_prob=None) -> dict:
    """Compute a set of metrics by name.

    Args:
        y_true: Ground truth labels/values.
        y_pred: Predicted labels/values.
        metric_names: List of metric names to compute.
        y_prob: Predicted probabilities (needed for AUC, log_loss, etc.).

    Returns:
        Dict of {metric_name: value}.
    """
    results = {}
    for name in metric_names:
        fn = METRIC_REGISTRY.get(name.lower())
        if fn is None:
            raise ValueError(f"Unknown metric: {name}. Available: {list(METRIC_REGISTRY.keys())}")
        try:
            results[name] = fn(y_true, y_pred, y_prob)
        except Exception as e:
            results[name] = float("nan")
            print(f"Warning: metric '{name}' failed: {e}")
    return results


# --- Classification Metrics ---

def _accuracy(y_true, y_pred, y_prob=None):
    from sklearn.metrics import accuracy_score
    return accuracy_score(y_true, y_pred)


def _precision(y_true, y_pred, y_prob=None):
    from sklearn.metrics import precision_score
    return precision_score(y_true, y_pred, average="weighted", zero_division=0)


def _recall(y_true, y_pred, y_prob=None):
    from sklearn.metrics import recall_score
    return recall_score(y_true, y_pred, average="weighted", zero_division=0)


def _f1(y_true, y_pred, y_prob=None):
    from sklearn.metrics import f1_score
    return f1_score(y_true, y_pred, average="weighted", zero_division=0)


def _auc_roc(y_true, y_pred, y_prob=None):
    from sklearn.metrics import roc_auc_score
    if y_prob is None:
        raise ValueError("AUC-ROC requires y_prob (predicted probabilities)")
    if y_prob.ndim == 2 and y_prob.shape[1] == 2:
        return roc_auc_score(y_true, y_prob[:, 1])
    return roc_auc_score(y_true, y_prob, multi_class="ovr", average="weighted")


def _log_loss(y_true, y_pred, y_prob=None):
    from sklearn.metrics import log_loss
    if y_prob is None:
        raise ValueError("Log loss requires y_prob")
    return log_loss(y_true, y_prob)


def _matthews_corrcoef(y_true, y_pred, y_prob=None):
    from sklearn.metrics import matthews_corrcoef
    return matthews_corrcoef(y_true, y_pred)


# --- Regression Metrics ---

def _mse(y_true, y_pred, y_prob=None):
    from sklearn.metrics import mean_squared_error
    return mean_squared_error(y_true, y_pred)


def _rmse(y_true, y_pred, y_prob=None):
    from sklearn.metrics import mean_squared_error
    return mean_squared_error(y_true, y_pred, squared=False)


def _mae(y_true, y_pred, y_prob=None):
    from sklearn.metrics import mean_absolute_error
    return mean_absolute_error(y_true, y_pred)


def _r2(y_true, y_pred, y_prob=None):
    from sklearn.metrics import r2_score
    return r2_score(y_true, y_pred)


def _mape(y_true, y_pred, y_prob=None):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    mask = y_true != 0
    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100


# --- Ranking Metrics ---

def _ndcg(y_true, y_pred, y_prob=None):
    from sklearn.metrics import ndcg_score
    y_true = np.array(y_true).reshape(1, -1)
    y_pred = np.array(y_pred).reshape(1, -1)
    return ndcg_score(y_true, y_pred)


# --- Metric Registry ---

METRIC_REGISTRY = {
    # Classification
    "accuracy": _accuracy,
    "precision": _precision,
    "recall": _recall,
    "f1": _f1,
    "auc_roc": _auc_roc,
    "auc": _auc_roc,
    "log_loss": _log_loss,
    "logloss": _log_loss,
    "mcc": _matthews_corrcoef,
    "matthews_corrcoef": _matthews_corrcoef,
    # Regression
    "mse": _mse,
    "rmse": _rmse,
    "mae": _mae,
    "r2": _r2,
    "mape": _mape,
    # Ranking
    "ndcg": _ndcg,
}


def list_metrics() -> list[str]:
    """Return list of available metric names."""
    return sorted(METRIC_REGISTRY.keys())
