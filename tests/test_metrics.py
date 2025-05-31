"""Tests for kimera.metrics module.

This test suite validates the statistical metrics and confidence intervals
used for evaluating contradiction detection performance.
"""
import numpy as np
import pytest
from kimera.metrics import (
    roc_stats, pr_stats, accuracy_stats, bootstrap_ci, 
    mcnemar_test, compute_optimal_threshold
)


class TestROCStats:
    """Test ROC curve computation."""
    
    def test_perfect_classifier(self):
        """Test ROC stats for a perfect classifier."""
        y_true = np.array([0, 0, 1, 1])
        y_score = np.array([0.1, 0.2, 0.8, 0.9])
        
        roc = roc_stats(y_true, y_score)
        
        assert abs(roc["auroc"] - 1.0) < 1e-6
        assert len(roc["fpr"]) == len(roc["tpr"])
        assert len(roc["fpr"]) == len(roc["thresholds"])
        assert roc["fpr"][0] == 0.0  # Should start at (0,0)
        assert roc["tpr"][-1] == 1.0  # Should end at (1,1)
    
    def test_random_classifier(self):
        """Test ROC stats for a random classifier."""
        np.random.seed(42)
        y_true = np.random.randint(0, 2, 100)
        y_score = np.random.rand(100)
        
        roc = roc_stats(y_true, y_score)
        
        # Random classifier should have AUROC around 0.5
        assert 0.3 < roc["auroc"] < 0.7
        assert isinstance(roc["fpr"], list)
        assert isinstance(roc["tpr"], list)
    
    def test_single_class(self):
        """Test ROC stats when only one class is present."""
        y_true = np.array([0, 0, 0, 0])
        y_score = np.array([0.1, 0.2, 0.3, 0.4])
        
        roc = roc_stats(y_true, y_score)
        
        # Should handle gracefully and return default values
        assert roc["auroc"] == 0.5
        assert len(roc["fpr"]) == 2
        assert len(roc["tpr"]) == 2


class TestPRStats:
    """Test Precision-Recall curve computation."""
    
    def test_perfect_classifier(self):
        """Test PR stats for a perfect classifier."""
        y_true = np.array([0, 0, 1, 1])
        y_score = np.array([0.1, 0.2, 0.8, 0.9])
        
        pr = pr_stats(y_true, y_score)
        
        assert abs(pr["aupr"] - 1.0) < 1e-6
        assert len(pr["precision"]) == len(pr["recall"])
        assert len(pr["precision"]) == len(pr["thresholds"]) + 1  # PR curve has n+1 points
    
    def test_imbalanced_data(self):
        """Test PR stats with imbalanced classes."""
        np.random.seed(0)  # Fixed seed for deterministic test
        # 90% negative, 10% positive
        y_true = np.array([0] * 90 + [1] * 10)
        y_score = np.random.rand(100)
        
        pr = pr_stats(y_true, y_score)
        
        # AUPR should be in valid range for any classifier
        assert 0 < pr["aupr"] < 1
        assert isinstance(pr["precision"], list)
        assert isinstance(pr["recall"], list)
    
    def test_single_class(self):
        """Test PR stats when only one class is present."""
        y_true = np.array([1, 1, 1, 1])
        y_score = np.array([0.1, 0.2, 0.3, 0.4])
        
        pr = pr_stats(y_true, y_score)
        
        # Should handle gracefully
        assert pr["aupr"] == 1.0  # All positive class
        assert len(pr["precision"]) >= 1
        assert len(pr["recall"]) >= 1


class TestAccuracyStats:
    """Test accuracy and related metrics."""
    
    def test_perfect_predictions(self):
        """Test accuracy stats for perfect predictions."""
        y_true = np.array([0, 1, 0, 1, 1])
        y_pred = np.array([0, 1, 0, 1, 1])
        
        stats = accuracy_stats(y_true, y_pred)
        
        assert stats["accuracy"] == 1.0
        assert stats["precision"] == 1.0
        assert stats["recall"] == 1.0
        assert stats["f1"] == 1.0
    
    def test_all_wrong_predictions(self):
        """Test accuracy stats for completely wrong predictions."""
        y_true = np.array([0, 1, 0, 1])
        y_pred = np.array([1, 0, 1, 0])
        
        stats = accuracy_stats(y_true, y_pred)
        
        assert stats["accuracy"] == 0.0
        assert stats["precision"] == 0.0
        assert stats["recall"] == 0.0
        assert stats["f1"] == 0.0
    
    def test_mixed_predictions(self):
        """Test accuracy stats for mixed predictions."""
        y_true = np.array([0, 0, 1, 1, 1])
        y_pred = np.array([0, 1, 1, 1, 0])  # 3/5 correct
        
        stats = accuracy_stats(y_true, y_pred)
        
        assert stats["accuracy"] == 0.6
        assert 0 <= stats["precision"] <= 1
        assert 0 <= stats["recall"] <= 1
        assert 0 <= stats["f1"] <= 1


class TestBootstrapCI:
    """Test bootstrap confidence intervals."""
    
    def test_bootstrap_auroc(self):
        """Test bootstrap CI for AUROC."""
        np.random.seed(42)
        y_true = np.array([0, 0, 1, 1] * 25)  # 100 samples
        y_score = y_true + np.random.normal(0, 0.1, 100)  # Nearly perfect
        
        def auroc_fn(yt, ys):
            return roc_stats(yt, ys)["auroc"]
        
        lo, hi = bootstrap_ci(auroc_fn, y_true, y_score, n=100, seed=42)
        
        assert 0 <= lo <= hi <= 1
        assert hi - lo < 0.5  # CI should be reasonably tight for good classifier
    
    def test_bootstrap_accuracy(self):
        """Test bootstrap CI for accuracy."""
        np.random.seed(42)
        y_true = np.random.randint(0, 2, 50)
        y_pred = y_true.copy()
        y_pred[::5] = 1 - y_pred[::5]  # Flip every 5th prediction
        
        def acc_fn(yt, yp):
            return accuracy_stats(yt, yp.round().astype(int))["accuracy"]
        
        lo, hi = bootstrap_ci(acc_fn, y_true, y_pred.astype(float), n=100, seed=42)
        
        assert 0 <= lo <= hi <= 1
        assert hi - lo > 0  # Should have some uncertainty
    
    def test_bootstrap_empty_data(self):
        """Test bootstrap CI with edge cases."""
        y_true = np.array([])
        y_score = np.array([])
        
        def dummy_fn(yt, ys):
            if len(yt) == 0:
                raise ValueError("Empty data")
            return 0.5
        
        lo, hi = bootstrap_ci(dummy_fn, y_true, y_score, n=10)
        
        assert lo == 0.0
        assert hi == 0.0


class TestMcNemarTest:
    """Test McNemar's test for comparing classifiers."""
    
    def test_identical_classifiers(self):
        """Test McNemar's test when classifiers are identical."""
        a_correct = np.array([True, False, True, False, True])
        b_correct = np.array([True, False, True, False, True])
        
        stat, p_value = mcnemar_test(a_correct, b_correct)
        
        assert stat == 0.0
        assert p_value == 1.0
    
    def test_different_classifiers(self):
        """Test McNemar's test with different classifiers."""
        a_correct = np.array([True, True, False, False, True])
        b_correct = np.array([False, True, True, False, False])
        
        stat, p_value = mcnemar_test(a_correct, b_correct)
        
        assert stat >= 0
        assert 0 <= p_value <= 1
    
    def test_one_better_classifier(self):
        """Test McNemar's test when one classifier is clearly better."""
        # Classifier A is correct 80% of time, B is correct 20% of time
        np.random.seed(42)
        a_correct = np.random.rand(100) < 0.8
        b_correct = np.random.rand(100) < 0.2
        
        stat, p_value = mcnemar_test(a_correct, b_correct)
        
        assert stat > 0
        assert p_value < 0.05  # Should be significant


class TestOptimalThreshold:
    """Test optimal threshold computation."""
    
    def test_optimal_f1_threshold(self):
        """Test finding optimal threshold for F1 score."""
        # Create data where threshold 0.6 should be optimal
        y_true = np.array([0, 0, 0, 1, 1, 1])
        y_score = np.array([0.1, 0.3, 0.5, 0.7, 0.8, 0.9])
        
        thresh, f1 = compute_optimal_threshold(y_true, y_score, "f1")
        
        assert 0 <= thresh <= 1
        assert 0 <= f1 <= 1
        assert 0.5 < thresh < 0.8  # Should be around 0.6
    
    def test_optimal_accuracy_threshold(self):
        """Test finding optimal threshold for accuracy."""
        y_true = np.array([0, 0, 1, 1])
        y_score = np.array([0.2, 0.4, 0.6, 0.8])
        
        thresh, acc = compute_optimal_threshold(y_true, y_score, "accuracy")
        
        assert 0 <= thresh <= 1
        assert 0 <= acc <= 1
    
    def test_invalid_metric(self):
        """Test error handling for invalid metric."""
        y_true = np.array([0, 1])
        y_score = np.array([0.3, 0.7])
        
        with pytest.raises(ValueError, match="Unknown metric"):
            compute_optimal_threshold(y_true, y_score, "invalid_metric")


class TestIntegration:
    """Integration tests combining multiple metrics."""
    
    def test_full_evaluation_pipeline(self):
        """Test a complete evaluation pipeline."""
        np.random.seed(42)
        
        # Generate synthetic data
        n_samples = 200
        y_true = np.random.randint(0, 2, n_samples)
        
        # Create two classifiers with different performance
        noise_a = np.random.normal(0, 0.3, n_samples)
        noise_b = np.random.normal(0, 0.5, n_samples)
        
        y_score_a = y_true + noise_a
        y_score_b = y_true + noise_b
        
        # Compute all metrics
        roc_a = roc_stats(y_true, y_score_a)
        roc_b = roc_stats(y_true, y_score_b)
        
        pr_a = pr_stats(y_true, y_score_a)
        pr_b = pr_stats(y_true, y_score_b)
        
        # Find optimal thresholds
        thresh_a, f1_a = compute_optimal_threshold(y_true, y_score_a, "f1")
        thresh_b, f1_b = compute_optimal_threshold(y_true, y_score_b, "f1")
        
        # Binary predictions
        y_pred_a = (y_score_a >= thresh_a).astype(int)
        y_pred_b = (y_score_b >= thresh_b).astype(int)
        
        acc_a = accuracy_stats(y_true, y_pred_a)
        acc_b = accuracy_stats(y_true, y_pred_b)
        
        # McNemar's test
        a_correct = (y_pred_a == y_true)
        b_correct = (y_pred_b == y_true)
        mcnemar_stat, mcnemar_p = mcnemar_test(a_correct, b_correct)
        
        # Assertions
        assert roc_a["auroc"] > roc_b["auroc"]  # A should be better
        assert pr_a["aupr"] > pr_b["aupr"]
        assert acc_a["f1"] > acc_b["f1"]
        assert mcnemar_stat >= 0
        assert 0 <= mcnemar_p <= 1
        
        # Bootstrap CIs
        auroc_ci_a = bootstrap_ci(
            lambda yt, ys: roc_stats(yt, ys)["auroc"], 
            y_true, y_score_a, n=50
        )
        
        assert auroc_ci_a[0] <= roc_a["auroc"] <= auroc_ci_a[1]


if __name__ == "__main__":
    pytest.main([__file__])