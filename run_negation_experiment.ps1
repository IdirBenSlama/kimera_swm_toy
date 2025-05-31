# PowerShell script for negation fix experiment
# Run this in your activated virtual environment

Write-Host "🧪 Kimera Negation Fix Experiment" -ForegroundColor Cyan
Write-Host "=" * 40

# Check if we're in the right directory
if (-not (Test-Path "src\kimera")) {
    Write-Host "❌ Not in Kimera project directory" -ForegroundColor Red
    Write-Host "Please run this from the project root" -ForegroundColor Yellow
    exit 1
}

# Check if data file exists
$dataFile = "data\mixed_contradictions.csv"
if (-not (Test-Path $dataFile)) {
    Write-Host "❌ Data file not found: $dataFile" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Data file found: $dataFile" -ForegroundColor Green

# Step 1: Run baseline (negation fix OFF)
Write-Host "`n🔄 Step 1: Running baseline (negation fix OFF)" -ForegroundColor Yellow
Remove-Item Env:KIMERA_NEGATION_FIX -ErrorAction SilentlyContinue

$baselineCmd = "poetry run python -m benchmarks.llm_compare $dataFile --max-pairs 500 --kimera-only --outfile baseline.csv --no-emoji"
Write-Host "Command: $baselineCmd" -ForegroundColor Gray

try {
    Invoke-Expression $baselineCmd
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Baseline complete" -ForegroundColor Green
    } else {
        Write-Host "❌ Baseline failed" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Baseline error: $_" -ForegroundColor Red
    exit 1
}

# Step 2: Run with negation fix (negation fix ON)
Write-Host "`n🔄 Step 2: Running with negation fix (negation fix ON)" -ForegroundColor Yellow
$Env:KIMERA_NEGATION_FIX = "1"

$negfixCmd = "poetry run python -m benchmarks.llm_compare $dataFile --max-pairs 500 --kimera-only --outfile negfix.csv --no-emoji"
Write-Host "Command: $negfixCmd" -ForegroundColor Gray

try {
    Invoke-Expression $negfixCmd
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Negation fix complete" -ForegroundColor Green
    } else {
        Write-Host "❌ Negation fix failed" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Negation fix error: $_" -ForegroundColor Red
    exit 1
}

# Step 3: Compare results
Write-Host "`n📈 Step 3: Comparing results" -ForegroundColor Yellow

if (Test-Path "compare_results.py") {
    try {
        python compare_results.py baseline.csv negfix.csv
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Comparison complete" -ForegroundColor Green
        } else {
            Write-Host "❌ Comparison failed" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ Comparison error: $_" -ForegroundColor Red
    }
} else {
    Write-Host "⚠️  compare_results.py not found" -ForegroundColor Yellow
}

# Show file info
Write-Host "`n📁 Output Files:" -ForegroundColor Cyan
if (Test-Path "baseline.csv") {
    $size = (Get-Item "baseline.csv").Length
    Write-Host "  baseline.csv: $size bytes" -ForegroundColor Gray
}
if (Test-Path "negfix.csv") {
    $size = (Get-Item "negfix.csv").Length
    Write-Host "  negfix.csv: $size bytes" -ForegroundColor Gray
}

Write-Host "`n🎉 Experiment complete!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Check if AUROC/F1 confidence intervals overlap" -ForegroundColor White
Write-Host "2. If no overlap → significant improvement! 🎯" -ForegroundColor White
Write-Host "3. Open tools\explorer.html to analyze patterns" -ForegroundColor White
Write-Host "4. Identify next error bucket for improvement" -ForegroundColor White