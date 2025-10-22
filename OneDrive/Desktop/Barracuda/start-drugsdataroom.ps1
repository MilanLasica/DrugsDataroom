# DrugsDataRoom Startup Script
# This script starts both the backend and frontend as a single application

Write-Host "Starting DrugsDataRoom..." -ForegroundColor Green

# Function to check if a port is in use
function Test-Port {
    param([int]$Port)
    try {
        $connection = New-Object System.Net.Sockets.TcpClient
        $connection.Connect("localhost", $Port)
        $connection.Close()
        return $true
    }
    catch {
        return $false
    }
}

# Kill any existing processes on ports 3000 and 8001
Write-Host "Cleaning up existing processes..." -ForegroundColor Yellow
if (Test-Port 3000) {
    $process = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($process) {
        $pid = (Get-NetTCPConnection -LocalPort 3000).OwningProcess
        Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
        Write-Host "Killed process on port 3000" -ForegroundColor Yellow
    }
}

if (Test-Port 8001) {
    $process = Get-NetTCPConnection -LocalPort 8001 -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($process) {
        $pid = (Get-NetTCPConnection -LocalPort 8001).OwningProcess
        Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
        Write-Host "Killed process on port 8001" -ForegroundColor Yellow
    }
}

# Start Backend
Write-Host "Starting Backend (FastAPI) on port 8001..." -ForegroundColor Cyan
Set-Location "elysia"
Start-Process -FilePath "python" -ArgumentList "-c", "import sys; sys.path.append('.'); from elysia.api.app import app; import uvicorn; uvicorn.run(app, host='0.0.0.0', port=8001)" -WindowStyle Hidden

# Wait a moment for backend to start
Start-Sleep -Seconds 3

# Start Frontend
Write-Host "Starting Frontend (Next.js) on port 3000..." -ForegroundColor Cyan
Set-Location "..\elysia-frontend"
Start-Process -FilePath "npm" -ArgumentList "run", "dev" -WindowStyle Hidden

# Wait for services to start
Write-Host "Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check if services are running
$backendRunning = Test-Port 8001
$frontendRunning = Test-Port 3000

if ($backendRunning -and $frontendRunning) {
    Write-Host "✅ DrugsDataRoom is now running!" -ForegroundColor Green
    Write-Host "🌐 Frontend: http://localhost:3000" -ForegroundColor Green
    Write-Host "🔧 Backend API: http://localhost:8001" -ForegroundColor Green
    Write-Host ""
    Write-Host "Press any key to stop the application..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    
    # Stop processes
    Write-Host "Stopping DrugsDataRoom..." -ForegroundColor Yellow
    Get-Process | Where-Object {$_.ProcessName -eq "python" -or $_.ProcessName -eq "node"} | Stop-Process -Force -ErrorAction SilentlyContinue
    Write-Host "Application stopped." -ForegroundColor Red
} else {
    Write-Host "❌ Failed to start DrugsDataRoom. Please check the logs." -ForegroundColor Red
    if (-not $backendRunning) { Write-Host "Backend not running on port 8001" -ForegroundColor Red }
    if (-not $frontendRunning) { Write-Host "Frontend not running on port 3000" -ForegroundColor Red }
}

Set-Location ".."
