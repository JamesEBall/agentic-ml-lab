"""Visualization utilities for the Agentic ML Research Lab.

Provides ~20 plot functions for EDA, training monitoring, and evaluation.
All functions save plots to disk and return the figure for further customization.
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns

# Default style
sns.set_theme(style="whitegrid", font_scale=1.1)
DEFAULT_FIGSIZE = (10, 6)
DEFAULT_DPI = 300


def _save_fig(fig, save_path: str | None, dpi: int = DEFAULT_DPI):
    """Save figure to path, creating directories as needed."""
    if save_path:
        os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
        fig.savefig(save_path, dpi=dpi, bbox_inches="tight")
        print(f"Saved: {save_path}")
    return fig


# ========== EDA Plots ==========

def plot_distributions(df, columns=None, save_path=None):
    """Plot histograms for numeric columns."""
    import pandas as pd
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
    n = len(columns)
    if n == 0:
        return None
    ncols = min(3, n)
    nrows = (n + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(5 * ncols, 4 * nrows))
    axes = np.array(axes).flatten() if n > 1 else [axes]
    for i, col in enumerate(columns):
        sns.histplot(df[col].dropna(), ax=axes[i], kde=True)
        axes[i].set_title(col)
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)
    fig.suptitle("Feature Distributions", y=1.02, fontsize=14)
    fig.tight_layout()
    return _save_fig(fig, save_path)


def plot_categorical_bars(df, columns=None, save_path=None):
    """Plot bar charts for categorical columns."""
    if columns is None:
        columns = df.select_dtypes(include=["object", "category"]).columns.tolist()
    n = len(columns)
    if n == 0:
        return None
    ncols = min(3, n)
    nrows = (n + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(5 * ncols, 4 * nrows))
    axes = np.array(axes).flatten() if n > 1 else [axes]
    for i, col in enumerate(columns):
        counts = df[col].value_counts().head(20)
        counts.plot.bar(ax=axes[i])
        axes[i].set_title(col)
        axes[i].tick_params(axis="x", rotation=45)
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)
    fig.suptitle("Categorical Feature Distributions", y=1.02, fontsize=14)
    fig.tight_layout()
    return _save_fig(fig, save_path)


def plot_target_distribution(series, name="target", save_path=None):
    """Plot target variable distribution (auto-detects continuous vs categorical)."""
    fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)
    nunique = series.nunique()
    if nunique <= 20:
        counts = series.value_counts().sort_index()
        counts.plot.bar(ax=ax, color=sns.color_palette("husl", len(counts)))
        ax.set_ylabel("Count")
        for i, v in enumerate(counts):
            ax.text(i, v + 0.5, str(v), ha="center", fontsize=10)
    else:
        sns.histplot(series.dropna(), ax=ax, kde=True)
        ax.set_ylabel("Frequency")
    ax.set_title(f"Target Distribution: {name}")
    ax.set_xlabel(name)
    fig.tight_layout()
    return _save_fig(fig, save_path)


def plot_correlation_matrix(df, save_path=None):
    """Plot correlation matrix heatmap for numeric columns."""
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.shape[1] < 2:
        return None
    corr = numeric_df.corr()
    size = max(8, len(corr) * 0.5)
    fig, ax = plt.subplots(figsize=(size, size))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=len(corr) <= 15, fmt=".2f",
                cmap="RdBu_r", center=0, ax=ax, square=True)
    ax.set_title("Feature Correlation Matrix")
    fig.tight_layout()
    return _save_fig(fig, save_path)


def plot_missing_values(df, save_path=None):
    """Plot missing value heatmap."""
    missing = df.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=False)
    if len(missing) == 0:
        fig, ax = plt.subplots(figsize=(6, 2))
        ax.text(0.5, 0.5, "No missing values found", ha="center", va="center",
                fontsize=14, transform=ax.transAxes)
        ax.set_axis_off()
        return _save_fig(fig, save_path)
    fig, ax = plt.subplots(figsize=(10, max(4, len(missing) * 0.4)))
    pct = (missing / len(df) * 100).values
    bars = ax.barh(range(len(missing)), pct, color=sns.color_palette("Reds_r", len(missing)))
    ax.set_yticks(range(len(missing)))
    ax.set_yticklabels(missing.index)
    ax.set_xlabel("Missing %")
    ax.set_title("Missing Values by Feature")
    for i, v in enumerate(pct):
        ax.text(v + 0.5, i, f"{v:.1f}%", va="center")
    fig.tight_layout()
    return _save_fig(fig, save_path)


def plot_outliers(df, columns=None, save_path=None):
    """Plot box plots to visualize outliers."""
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
    n = len(columns)
    if n == 0:
        return None
    ncols = min(4, n)
    nrows = (n + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(4 * ncols, 4 * nrows))
    axes = np.array(axes).flatten() if n > 1 else [axes]
    for i, col in enumerate(columns):
        sns.boxplot(y=df[col].dropna(), ax=axes[i])
        axes[i].set_title(col)
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)
    fig.suptitle("Outlier Detection (Box Plots)", y=1.02, fontsize=14)
    fig.tight_layout()
    return _save_fig(fig, save_path)


def plot_pairplot(df, target_col=None, max_features=6, save_path=None):
    """Plot pairplot for top correlated features."""
    numeric_df = df.select_dtypes(include=[np.number])
    cols = numeric_df.columns.tolist()
    if target_col and target_col in df.columns:
        # Select top correlated with target
        if target_col in numeric_df.columns:
            corr = numeric_df.corr()[target_col].abs().sort_values(ascending=False)
            cols = corr.head(max_features).index.tolist()
        plot_df = df[cols + ([target_col] if target_col not in cols else [])]
        g = sns.pairplot(plot_df, hue=target_col if df[target_col].nunique() <= 10 else None,
                         diag_kind="kde")
    else:
        cols = cols[:max_features]
        g = sns.pairplot(df[cols], diag_kind="kde")
    g.figure.suptitle("Feature Pairplot", y=1.02)
    if save_path:
        _save_fig(g.figure, save_path)
    return g.figure


# ========== Training Plots ==========

def plot_training_curves(history: dict, save_path=None):
    """Plot training and validation loss/metric curves.

    Args:
        history: Dict with keys like 'train_loss', 'val_loss', 'train_acc', etc.
                 Values are lists of per-epoch values.
    """
    # Separate loss and metric curves
    loss_keys = [k for k in history if "loss" in k.lower()]
    metric_keys = [k for k in history if "loss" not in k.lower()]

    n_plots = (1 if loss_keys else 0) + (1 if metric_keys else 0)
    if n_plots == 0:
        return None

    fig, axes = plt.subplots(1, n_plots, figsize=(7 * n_plots, 5))
    if n_plots == 1:
        axes = [axes]

    idx = 0
    if loss_keys:
        for key in loss_keys:
            axes[idx].plot(history[key], label=key)
        axes[idx].set_title("Loss")
        axes[idx].set_xlabel("Epoch")
        axes[idx].set_ylabel("Loss")
        axes[idx].legend()
        idx += 1

    if metric_keys:
        for key in metric_keys:
            axes[idx].plot(history[key], label=key)
        axes[idx].set_title("Metrics")
        axes[idx].set_xlabel("Epoch")
        axes[idx].set_ylabel("Value")
        axes[idx].legend()

    fig.suptitle("Training Curves", fontsize=14)
    fig.tight_layout()
    return _save_fig(fig, save_path)


def plot_learning_rate(lr_history: list, save_path=None):
    """Plot learning rate schedule over training."""
    fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)
    ax.plot(lr_history)
    ax.set_title("Learning Rate Schedule")
    ax.set_xlabel("Step")
    ax.set_ylabel("Learning Rate")
    ax.set_yscale("log")
    fig.tight_layout()
    return _save_fig(fig, save_path)


# ========== Evaluation Plots ==========

def plot_confusion_matrix(y_true, y_pred, labels=None, save_path=None):
    """Plot confusion matrix heatmap."""
    from sklearn.metrics import confusion_matrix
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    fig, ax = plt.subplots(figsize=(max(6, len(cm) * 0.8), max(5, len(cm) * 0.7)))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax,
                xticklabels=labels or "auto", yticklabels=labels or "auto")
    ax.set_title("Confusion Matrix")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    fig.tight_layout()
    return _save_fig(fig, save_path)


def plot_roc_curve(y_true, y_prob, save_path=None):
    """Plot ROC curve with AUC."""
    from sklearn.metrics import roc_curve, auc
    if y_prob.ndim == 2 and y_prob.shape[1] == 2:
        y_prob = y_prob[:, 1]
    fpr, tpr, _ = roc_curve(y_true, y_prob)
    roc_auc = auc(fpr, tpr)
    fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)
    ax.plot(fpr, tpr, lw=2, label=f"ROC (AUC = {roc_auc:.3f})")
    ax.plot([0, 1], [0, 1], "k--", lw=1, label="Random")
    ax.set_title("ROC Curve")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.legend()
    fig.tight_layout()
    return _save_fig(fig, save_path)


def plot_precision_recall_curve(y_true, y_prob, save_path=None):
    """Plot precision-recall curve."""
    from sklearn.metrics import precision_recall_curve, average_precision_score
    if y_prob.ndim == 2 and y_prob.shape[1] == 2:
        y_prob = y_prob[:, 1]
    precision, recall, _ = precision_recall_curve(y_true, y_prob)
    ap = average_precision_score(y_true, y_prob)
    fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)
    ax.plot(recall, precision, lw=2, label=f"PR (AP = {ap:.3f})")
    ax.set_title("Precision-Recall Curve")
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.legend()
    fig.tight_layout()
    return _save_fig(fig, save_path)


def plot_predicted_vs_actual(y_true, y_pred, save_path=None):
    """Plot predicted vs actual for regression."""
    fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)
    ax.scatter(y_true, y_pred, alpha=0.5, s=10)
    lims = [min(min(y_true), min(y_pred)), max(max(y_true), max(y_pred))]
    ax.plot(lims, lims, "r--", lw=1, label="Perfect")
    ax.set_title("Predicted vs Actual")
    ax.set_xlabel("Actual")
    ax.set_ylabel("Predicted")
    ax.legend()
    fig.tight_layout()
    return _save_fig(fig, save_path)


def plot_residuals(y_true, y_pred, save_path=None):
    """Plot residual distribution and residuals vs predicted."""
    residuals = np.array(y_true) - np.array(y_pred)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    # Residual distribution
    sns.histplot(residuals, kde=True, ax=ax1)
    ax1.axvline(0, color="r", linestyle="--")
    ax1.set_title("Residual Distribution")
    ax1.set_xlabel("Residual")
    # Residuals vs predicted
    ax2.scatter(y_pred, residuals, alpha=0.5, s=10)
    ax2.axhline(0, color="r", linestyle="--")
    ax2.set_title("Residuals vs Predicted")
    ax2.set_xlabel("Predicted")
    ax2.set_ylabel("Residual")
    fig.suptitle("Residual Analysis", fontsize=14)
    fig.tight_layout()
    return _save_fig(fig, save_path)


# ========== Cross-Run Comparison Plots ==========

def plot_comparison_bar(run_results: list[dict], metric: str, save_path=None):
    """Bar chart comparing a metric across runs.

    Args:
        run_results: List of dicts with 'run_name' and 'metrics' keys.
        metric: Which metric to compare.
    """
    names = [r["run_name"] for r in run_results]
    values = [r["metrics"].get(metric, 0) for r in run_results]
    fig, ax = plt.subplots(figsize=(max(8, len(names) * 1.2), 6))
    colors = sns.color_palette("husl", len(names))
    bars = ax.bar(range(len(names)), values, color=colors)
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=45, ha="right")
    ax.set_ylabel(metric)
    ax.set_title(f"{metric} Comparison Across Runs")
    # Highlight best
    best_idx = int(np.argmax(values))
    bars[best_idx].set_edgecolor("black")
    bars[best_idx].set_linewidth(2)
    for i, v in enumerate(values):
        ax.text(i, v, f"{v:.4f}", ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    return _save_fig(fig, save_path)


def plot_metric_over_runs(run_results: list[dict], metric: str, save_path=None):
    """Line plot showing metric progression over sequential runs."""
    names = [r["run_name"] for r in run_results]
    values = [r["metrics"].get(metric, 0) for r in run_results]
    fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)
    ax.plot(range(len(names)), values, "o-", lw=2, markersize=8)
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=45, ha="right")
    ax.set_ylabel(metric)
    ax.set_title(f"{metric} Progression Over Experiments")
    # Highlight best
    best_idx = int(np.argmax(values))
    ax.plot(best_idx, values[best_idx], "r*", markersize=20, label="Best")
    ax.legend()
    fig.tight_layout()
    return _save_fig(fig, save_path)


def plot_training_curves_overlay(histories: dict[str, dict], metric: str = "val_loss",
                                  save_path=None):
    """Overlay training curves from multiple runs.

    Args:
        histories: Dict of {run_name: history_dict}.
        metric: Which metric key to plot from each history.
    """
    fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)
    for name, history in histories.items():
        if metric in history:
            ax.plot(history[metric], label=name)
    ax.set_title(f"{metric} Across Runs")
    ax.set_xlabel("Epoch")
    ax.set_ylabel(metric)
    ax.legend()
    fig.tight_layout()
    return _save_fig(fig, save_path)


def plot_parameter_sensitivity(results: list[dict], param: str, metric: str,
                                save_path=None):
    """Plot how a metric changes with a parameter across runs.

    Args:
        results: List of dicts with 'params' and 'metrics'.
        param: Parameter name to plot on x-axis.
        metric: Metric name to plot on y-axis.
    """
    param_vals = []
    metric_vals = []
    for r in results:
        if param in r["params"] and metric in r["metrics"]:
            try:
                param_vals.append(float(r["params"][param]))
                metric_vals.append(float(r["metrics"][metric]))
            except (ValueError, TypeError):
                continue
    if not param_vals:
        return None
    fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)
    ax.plot(param_vals, metric_vals, "o-", lw=2, markersize=8)
    ax.set_xlabel(param)
    ax.set_ylabel(metric)
    ax.set_title(f"Sensitivity: {metric} vs {param}")
    fig.tight_layout()
    return _save_fig(fig, save_path)
