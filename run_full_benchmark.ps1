# Kimera-SWM v0.7.0 - Full Benchmark Runner
# PowerShell script for comprehensive benchmark with metrics

Write-Host "Kimera-SWM v0.7.0 - Full Benchmark Runner" -ForegroundColor Cyan
Write-Host "=" * 50

# Set UTF-8 encoding to handle any Unicode output safely
$env:PYTHONIOENCODING = "utf-8"

# Check if we're in the right directory
if (-not (Test-Path "src/kimera")) {
    Write-Host "[ERROR] Not in Kimera project root directory" -ForegroundColor Red
    Write-Host "Please run from the project root where src/kimera exists"
    exit 1
}

# Check if data file exists
$dataFile = "data/contradictions_2k.csv"
if (-not (Test-Path $dataFile)) {
    Write-Host "[WARN] Large dataset not found: $dataFile" -ForegroundColor Yellow
    $dataFile = "data/toy_contradictions.csv"
    if (-not (Test-Path $dataFile)) {
        Write-Host "[ERROR] No dataset found. Please ensure data files exist." -ForegroundColor Red
        exit 1
    }
    Write-Host "[INFO] Using smaller dataset: $dataFile" -ForegroundColor Yellow
}

Write-Host "[INFO] Running validation first..." -ForegroundColor Green
python validate_all_green.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Validation failed. Please fix issues before running benchmark." -ForegroundColor Red
    exit 1
}

Write-Host "`n[INFO] Starting benchmark run..." -ForegroundColor Green
Write-Host "Dataset: $dataFile"

# Determine benchmark mode
if ($env:OPENAI_API_KEY) {
    Write-Host "Mode: Kimera vs GPT comparison" -ForegroundColor Green
    $benchmarkCmd = "poetry run python -m benchmarks.llm_compare `"$dataFile`" --max-pairs 500 --stats --async 8 --mp 4"
} else {
    Write-Host "Mode: Kimera-only (no API key detected)" -ForegroundColor Yellow
    $benchmarkCmd = "poetry run python -m benchmarks.llm_compare `"$dataFile`" --max-pairs 500 --stats --kimera-only"
}

Write-Host "Command: $benchmarkCmd"
Write-Host ""

# Run the benchmark
Invoke-Expression $benchmarkCmd

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n[SUCCESS] Benchmark completed!" -ForegroundColor Green
    
    # Check for generated files
    $generatedFiles = @()
    if (Test-Path "benchmark_results.csv") { $generatedFiles += "benchmark_results.csv" }
    if (Test-Path "metrics.yaml") { $generatedFiles += "metrics.yaml" }
    if (Test-Path "roc.png") { $generatedFiles += "roc.png" }
    if (Test-Path "pr.png") { $generatedFiles += "pr.png" }
    
    if ($generatedFiles.Count -gt 0) {
        Write-Host "`nGenerated files:" -ForegroundColor Green
        foreach ($file in $generatedFiles) {
            $size = (Get-Item $file).Length
            Write-Host "  [OK] $file ($size bytes)" -ForegroundColor Green
        }
    }
    
    Write-Host "`nNext steps:" -ForegroundColor Cyan
    Write-Host "1. Open tools/explorer.html in your browser"
    Write-Host "2. Load benchmark_results.csv in the explorer"
    Write-Host "3. Filter to 'Only disagreements' to find error patterns"
    Write-Host "4. Add notes to interesting cases and export findings"
    
    if (Test-Path "metrics.yaml") {
        Write-Host "`nQuick metrics preview:" -ForegroundColor Cyan
        Get-Content "metrics.yaml" | Select-Object -First 10
    }
    
} else {
    Write-Host "`n[ERROR] Benchmark failed with exit code $LASTEXITCODE" -ForegroundColor Red
    Write-Host "Check the output above for error details."
    exit 1
}

Write-Host "`n[INFO] Benchmark run complete. Ready for error analysis!" -ForegroundColor Green