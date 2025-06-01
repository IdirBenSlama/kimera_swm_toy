"""Zetetic metrics utilities – no silent assumptions.

This module provides statistical metrics and confidence intervals for evaluating
contradiction detection performance. Every function is designed to surface
macro-level performance indicators that can guide micro-level optimizations.

Functions:
    roc_stats(y_true, y_score) -> dict
    pr_stats(y_true, y_score) -> dict
    bootstrap_ci(metric_fn, y_true, y_score, n=1000, seed=0) -> (lo, hi)
    mcnemar_test(a_correct, b_correct) -> (stat, p)
    accuracy_stats(y_true, y_pred) -> dict
"""
from __future__ import annotations
import numpy as np
from sklearn import metrics
from scipy import stats
from typing import Callable, Tuple, Union
import warnings


def roc_stats(y_true: np.ndarray, y_score: np.ndarray) -> dict:
    """Compute ROC curve and AUROC.
    
    Args:
        y_true: Binary labels (0/1)
        y_score: Prediction scores/probabilities
        
    Returns:
        dict with keys: fpr, tpr, auroc, thresholds
    """
    y_true = np.asarray(y_true)
    y_score = np.asarray(y_score)
    
    if len(np.unique(y_true)) < 2:
        warnings.warn("Only one class present in y_true. ROC AUC score is not defined.")
        return {"fpr": [0, 1], "tpr": [0, 1], "auroc": 0.5, "thresholds": [1, 0]}
    
    fpr, tpr, thresholds = metrics.roc_curve(y_true, y_score)
    auc = metrics.auc(fpr, tpr)
    
    return {
        "fpr": fpr.tolist(),
        "tpr": tpr.tolist(), 
        "auroc": float(auc),
        "thresholds": thresholds.tolist()
    }


def pr_stats(y_true: np.ndarray, y_score: np.ndarray) -> dict:
    """Compute Precision-Recall curve and AUPR.
    
    Args:
        y_true: Binary labels (0/1)
        y_score: Prediction scores/probabilities
        
    Returns:
        dict with keys: precision, recall, aupr, thresholds
    """
    y_true = np.asarray(y_true)
    y_score = np.asarray(y_score)
    
    if len(np.unique(y_true)) < 2:
        warnings.warn("Only one class present in y_true. PR AUC score is not defined.")
        baseline = np.mean(y_true)
        return {"precision": [baseline], "recall": [1], "aupr": baseline, "thresholds": [0]}
    
    precision, recall, thresholds = metrics.precision_recall_curve(y_true, y_score)
    ap = metrics.average_precision_score(y_true, y_score)
    
    return {
        "precision": precision.tolist(),
        "recall": recall.tolist(),
        "aupr": float(ap),
        "thresholds": thresholds.tolist()
    }


def accuracy_stats(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    """Compute accuracy, precision, recall, F1.
    
    Args:
        y_true: Binary labels (0/1)
        y_pred: Binary predictions (0/1)
        
    Returns:
        dict with accuracy, precision, recall, f1
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    
    return {
        "accuracy": float(metrics.accuracy_score(y_true, y_pred)),
        "precision": float(metrics.precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(metrics.recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(metrics.f1_score(y_true, y_pred, zero_division=0))
    }


def bootstrap_ci(metric_fn: Callable[[np.ndarray, np.ndarray], float],
                 y_true: np.ndarray,
                 y_score: np.ndarray,
                 n: int = 1000,
                 seed: int = 0,
                 alpha: float = 0.05) -> Tuple[float, float]:
    """Bootstrap confidence interval for a metric.
    
    Args:
        metric_fn: Function that takes (y_true, y_score) and returns a scalar
        y_true: True labels
        y_score: Predicted scores
        n: Number of bootstrap samples
        seed: Random seed for reproducibility
        alpha: Significance level (0.05 for 95% CI)
        
    Returns:
        (lower_bound, upper_bound) of confidence interval
    """
    rng = np.random.default_rng(seed)
    stats_list = []
    
    for _ in range(n):
        # Bootstrap sample with replacement
        idx = rng.integers(0, len(y_true), len(y_true))
        try:
            stat = metric_fn(y_true[idx], y_score[idx])
            stats_list.append(stat)
        except (ValueError, ZeroDivisionError):
            # Skip invalid bootstrap samples
            continue
    
    if not stats_list:
        return 0.0, 0.0
        
    lo = np.quantile(stats_list, alpha/2)
    hi = np.quantile(stats_list, 1 - alpha/2)
    return float(lo), float(hi)


def mcnemar_test(a_correct: np.ndarray, b_correct: np.ndarray) -> Tuple[float, float]:
    """McNemar's test for comparing two classifiers.
    
    Args:
        a_correct: Boolean array indicating correct predictions for classifier A
        b_correct: Boolean array indicating correct predictions for classifier B
        
    Returns:
        (test_statistic, p_value)
    """
    a_correct = np.asarray(a_correct, dtype=bool)
    b_correct = np.asarray(b_correct, dtype=bool)
    
    # Create contingency table
    both_correct = np.sum(a_correct & b_correct)
    only_a_correct = np.sum(a_correct & ~b_correct)
    only_b_correct = np.sum(~a_correct & b_correct)
    both_wrong = np.sum(~a_correct & ~b_correct)
    
    # McNemar's test focuses on disagreements
    n01 = only_a_correct  # A correct, B wrong
    n10 = only_b_correct  # A wrong, B correct
    
    if n01 + n10 == 0:
        # No disagreements - classifiers are identical
        return 0.0, 1.0
    
    # McNemar test statistic with continuity correction
    stat = ((abs(n01 - n10) - 1) ** 2) / (n01 + n10)
    p_value = 1 - stats.chi2.cdf(stat, df=1)
    
    return float(stat), float(p_value)


def compute_optimal_threshold(y_true: np.ndarray, y_score: np.ndarray, 
                            metric: str = "f1") -> Tuple[float, float]:
    """Find optimal threshold for binary classification.
    
    Args:
        y_true: True binary labels
        y_score: Prediction scores
        metric: Metric to optimize ("f1", "accuracy", "precision", "recall")
        
    Returns:
        (optimal_threshold, best_metric_value)
    """
    thresholds = np.linspace(0, 1, 101)
    best_score = -1
    best_threshold = 0.5
    
    for thresh in thresholds:
        y_pred = (y_score >= thresh).astype(int)
        
        if metric == "f1":
            score = metrics.f1_score(y_true, y_pred, zero_division=0)
        elif metric == "accuracy":
            score = metrics.accuracy_score(y_true, y_pred)
        elif metric == "precision":
            score = metrics.precision_score(y_true, y_pred, zero_division=0)
        elif metric == "recall":
            score = metrics.recall_score(y_true, y_pred, zero_division=0)
        else:
            raise ValueError(f"Unknown metric: {metric}")
            
        if score > best_score:
            best_score = score
            best_threshold = thresh
    
    return float(best_threshold), float(best_score)