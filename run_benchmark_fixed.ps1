# Fixed PowerShell script to run Kimera benchmark
# Avoids line continuation issues by using single-line commands

Write-Host "Kimera-SWM v0.7.0 Benchmark Runner (Fixed)" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green

# Check if we're in the right directory
if (-not (Test-Path "src\kimera")) {
    Write-Host "[ERROR] Not in Kimera project root directory" -ForegroundColor Red
    Write-Host "Please run from the project root where src\kimera exists" -ForegroundColor Red
    exit 1
}

# Check for data file
if (-not (Test-Path "data\toy_contradictions.csv")) {
    Write-Host "[ERROR] Dataset not found: data\toy_contradictions.csv" -ForegroundColor Red
    exit 1
}

# Check for API key
$apiKey = $env:OPENAI_API_KEY
if (-not $apiKey -or $apiKey.StartsWith("sk-proj-")) {
    Write-Host "[INFO] No valid API key found. Running Kimera-only mode." -ForegroundColor Yellow
    $kimeraOnly = $true
} else {
    Write-Host "[INFO] API key found. Running full comparison." -ForegroundColor Green
    $kimeraOnly = $false
}

# Build command as single line (no continuation issues)
if ($kimeraOnly) {
    $cmd = "poetry run python -m benchmarks.llm_compare data/toy_contradictions.csv --max-pairs 20 --stats --kimera-only"
} else {
    $cmd = "poetry run python -m benchmarks.llm_compare data/toy_contradictions.csv --max-pairs 20 --stats --async 4"
}

Write-Host "[CMD] $cmd" -ForegroundColor Cyan

# Execute the command
try {
    Invoke-Expression $cmd
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n[SUCCESS] Benchmark completed successfully!" -ForegroundColor Green
        
        # Check for generated files
        Write-Host "`nGenerated files:" -ForegroundColor Green
        $files = @("benchmark_results.csv", "metrics.yaml", "roc.png")
        foreach ($file in $files) {
            if (Test-Path $file) {
                $size = (Get-Item $file).Length
                Write-Host "  [OK] $file ($size bytes)" -ForegroundColor Green
            } else {
                Write-Host "  [MISSING] $file" -ForegroundColor Yellow
            }
        }
        
        Write-Host "`nTo explore results:" -ForegroundColor Cyan
        Write-Host "  1. Open tools/explorer.html in your browser" -ForegroundColor Cyan
        Write-Host "  2. Load benchmark_results.csv" -ForegroundColor Cyan
        Write-Host "  3. Check 'Only disagreements' to see failure patterns" -ForegroundColor Cyan
        
    } else {
        Write-Host "`n[ERROR] Benchmark failed with exit code $LASTEXITCODE" -ForegroundColor Red
    }
} catch {
    Write-Host "`n[ERROR] Command execution failed: $_" -ForegroundColor Red
    exit 1
}

Write-Host "`nBenchmark run completed." -ForegroundColor Green