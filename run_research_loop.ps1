# PowerShell script for running the research loop
# UTF-8 console setup
chcp 65001

Write-Host "🚀 Starting Kimera Research Loop" -ForegroundColor Green
Write-Host "=" * 50

# Step 1: Test negation fix
Write-Host "`n📋 Step 1: Testing negation fix" -ForegroundColor Cyan
poetry run python test_negation_simple.py

# Step 2: Run baseline (if needed)
Write-Host "`n📊 Step 2: Running baseline benchmark" -ForegroundColor Cyan
if (-not (Test-Path "mixed5k_baseline.csv")) {
    Write-Host "Running baseline benchmark..."
    poetry run python -m benchmarks.llm_compare `
        data/mixed_contradictions.csv `
        --stats --no-cache --kimera-only --outfile mixed5k_baseline.csv --no-emoji
    
    if (Test-Path "metrics.yaml") {
        Copy-Item "metrics.yaml" "metrics_baseline.yaml"
        Write-Host "✓ Baseline metrics saved" -ForegroundColor Green
    }
} else {
    Write-Host "✓ Baseline already exists" -ForegroundColor Green
}

# Step 3: Run with negation fix
Write-Host "`n🔧 Step 3: Running with negation fix" -ForegroundColor Cyan
poetry run python -m benchmarks.llm_compare `
    data/mixed_contradictions.csv `
    --stats --no-cache --kimera-only --outfile mixed5k_negfix.csv --no-emoji

if (Test-Path "metrics.yaml") {
    Copy-Item "metrics.yaml" "metrics_negfix.yaml"
    Write-Host "✓ Negation fix metrics saved" -ForegroundColor Green
}

# Step 4: Compare results
Write-Host "`n📈 Step 4: Comparing results" -ForegroundColor Cyan
poetry run python compare_results.py

# Step 5: Open explorer
Write-Host "`n🔍 Opening results explorer" -ForegroundColor Cyan
if (Test-Path "tools/explorer.html") {
    Start-Process "tools/explorer.html"
    Write-Host "✓ Explorer opened in browser" -ForegroundColor Green
} else {
    Write-Host "⚠ Explorer not found" -ForegroundColor Yellow
}

Write-Host "`n🎉 Research loop completed!" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Load mixed5k_baseline.csv and mixed5k_negfix.csv in explorer"
Write-Host "2. Click 'Only disagreements' to analyze changes"
Write-Host "3. Tag error patterns for next iteration"