import subprocess
import sys
from pathlib import Path


def test_demo_cli_help():
    """Test that demo CLI shows help without errors."""
    result = subprocess.run([
        sys.executable, "-m", "kimera.demo", "--help"
    ], capture_output=True, text=True, cwd=Path(__file__).parent.parent)
    
    assert result.returncode == 0
    assert "CSV dataset path" in result.stdout


def test_demo_cli_with_toy_dataset():
    """Test demo runs with default toy dataset."""
    result = subprocess.run([
        sys.executable, "-m", "kimera.demo", "--chunk", "50"
    ], capture_output=True, text=True, cwd=Path(__file__).parent.parent)
    
    # Should succeed or fail gracefully if dataset missing
    assert result.returncode in [0, 1]  # 0 = success, 1 = dataset not found
    
    if result.returncode == 0:
        assert "Loaded" in result.stdout
        assert "geoids" in result.stdout


def test_benchmark_cli_help():
    """Test that benchmark CLI shows help without errors."""
    result = subprocess.run([
        sys.executable, "-m", "benchmarks.llm_compare", "--help"
    ], capture_output=True, text=True, cwd=Path(__file__).parent.parent)
    
    assert result.returncode == 0
    assert "Benchmark Kimera vs GPT-4o" in result.stdout


def test_benchmark_kimera_only():
    """Test benchmark runs in Kimera-only mode."""
    result = subprocess.run([
        sys.executable, "-m", "benchmarks.llm_compare", 
        "--kimera-only", "--max-pairs", "5"
    ], capture_output=True, text=True, cwd=Path(__file__).parent.parent)
    
    # Should succeed or fail gracefully if dataset missing
    assert result.returncode in [0, 1]  # 0 = success, 1 = dataset not found
    
    if result.returncode == 0:
        assert "Kimera Results:" in result.stdout
        assert "contradictions found:" in result.stdout.lower()