# PowerShell script to run Kimera benchmark with proper line continuation
# Addresses PowerShell-specific command line issues

Write-Host "Kimera-SWM v0.7.0 Benchmark Runner" -ForegroundColor Green
Write-Host "===================================" -ForegroundColor Green

# Check if we're in the right directory
if (-not (Test-Path "src\kimera")) {
    Write-Host "[ERROR] Not in Kimera project root directory" -ForegroundColor Red
    Write-Host "Please run from the project root where src\kimera exists" -ForegroundColor Red
    exit 1
}

# Check for API key
$apiKey = $env:OPENAI_API_KEY
if (-not $apiKey -or $apiKey.StartsWith("sk-proj-")) {
    Write-Host "[INFO] No valid API key found. Running Kimera-only mode." -ForegroundColor Yellow
    $cmd = "poetry run python -m benchmarks.llm_compare data/contradictions_2k.csv --max-pairs 500 --stats --no-cache --kimera-only"
} else {
    Write-Host "[INFO] API key found. Running full comparison." -ForegroundColor Green
    $cmd = "poetry run python -m benchmarks.llm_compare data/contradictions_2k.csv --max-pairs 500 --stats --no-cache --async 8 --mp 4"
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
    } else {
        Write-Host "`n[ERROR] Benchmark failed with exit code $LASTEXITCODE" -ForegroundColor Red
    }
} catch {
    Write-Host "`n[ERROR] Command execution failed: $_" -ForegroundColor Red
    exit 1
}

Write-Host "`nBenchmark run completed." -ForegroundColor Green