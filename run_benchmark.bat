@echo off
REM Batch script to run Kimera benchmark - Windows compatible
echo Kimera-SWM v0.7.0 Benchmark Runner (Batch)
echo ==========================================

REM Check if we're in the right directory
if not exist "src\kimera" (
    echo [ERROR] Not in Kimera project root directory
    echo Please run from the project root where src\kimera exists
    pause
    exit /b 1
)

REM Check for data file
if not exist "data\toy_contradictions.csv" (
    echo [ERROR] Dataset not found: data\toy_contradictions.csv
    pause
    exit /b 1
)

REM Check for API key (basic check)
if "%OPENAI_API_KEY%"=="" (
    echo [INFO] No API key found. Running Kimera-only mode.
    set "CMD=poetry run python -m benchmarks.llm_compare data/toy_contradictions.csv --max-pairs 20 --stats --kimera-only"
) else (
    echo [INFO] API key found. Running full comparison.
    set "CMD=poetry run python -m benchmarks.llm_compare data/toy_contradictions.csv --max-pairs 20 --stats --async 4"
)

echo [CMD] %CMD%
echo.

REM Execute the command
%CMD%

if %ERRORLEVEL% equ 0 (
    echo.
    echo [SUCCESS] Benchmark completed successfully!
    echo.
    echo Generated files:
    if exist "benchmark_results.csv" (
        echo   [OK] benchmark_results.csv
    ) else (
        echo   [MISSING] benchmark_results.csv
    )
    if exist "metrics.yaml" (
        echo   [OK] metrics.yaml
    ) else (
        echo   [MISSING] metrics.yaml
    )
    if exist "roc.png" (
        echo   [OK] roc.png
    ) else (
        echo   [MISSING] roc.png
    )
    echo.
    echo To explore results:
    echo   1. Open tools/explorer.html in your browser
    echo   2. Load benchmark_results.csv
    echo   3. Check 'Only disagreements' to see failure patterns
) else (
    echo.
    echo [ERROR] Benchmark failed with exit code %ERRORLEVEL%
)

echo.
echo Benchmark run completed.
pause