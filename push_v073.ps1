#!/usr/bin/env pwsh
# PowerShell script to push v0.7.3 changes and tags

Write-Host "Pushing v0.7.3 to remote repository..." -ForegroundColor Green

try {
    # Push commits
    Write-Host "Pushing commits..." -ForegroundColor Yellow
    git push
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to push commits"
    }
    
    # Push tags
    Write-Host "Pushing tags..." -ForegroundColor Yellow
    git push --tags
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to push tags"
    }
    
    Write-Host "✅ v0.7.3 successfully pushed!" -ForegroundColor Green
    Write-Host "🎉 Phase 19.2 complete and published!" -ForegroundColor Cyan
    
} catch {
    Write-Host "❌ Push failed: $_" -ForegroundColor Red
    exit 1
}