# PowerShell 脚本激活虚拟环境

if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "正在激活虚拟环境..." -ForegroundColor Green
    .\venv\Scripts\Activate.ps1
    Write-Host "虚拟环境已激活！" -ForegroundColor Green
    Write-Host ""
    Write-Host "现在你可以运行项目了：" -ForegroundColor Yellow
    Write-Host "python main.py" -ForegroundColor Cyan
} else {
    Write-Host "错误：虚拟环境不存在，请先运行创建脚本" -ForegroundColor Red
}