@echo off
echo ========================================
echo   PinnacleQt GUI 项目环境配置脚本
echo ========================================
echo.

REM 检查是否已存在虚拟环境
if exist "venv" (
    echo 检测到已存在虚拟环境，跳过创建...
    goto :install_deps
)

echo 正在创建虚拟环境...
python -m venv venv
if %errorlevel% neq 0 (
    echo 错误：创建虚拟环境失败！
    pause
    exit /b 1
)

:install_deps
echo 正在激活虚拟环境并安装依赖...
call venv\Scripts\activate.bat

REM 升级pip
python -m pip install --upgrade pip

REM 安装依赖
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo 错误：安装依赖失败！
    pause
    exit /b 1
)

echo.
echo ========================================
echo   项目环境配置完成！
echo ========================================
echo.
echo 现在可以运行项目：
echo python main.py
echo.
echo 或者使用：activate_venv.bat 来激活虚拟环境
echo.
pause