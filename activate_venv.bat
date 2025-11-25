@echo off
REM 激活虚拟环境的批处理脚本

if exist "venv\Scripts\activate.bat" (
    echo 正在激活虚拟环境...
    call venv\Scripts\activate.bat
    echo 虚拟环境已激活！
    echo.
    echo 现在你可以运行项目了：
    echo python main.py
) else (
    echo 错误：虚拟环境不存在，请先运行创建脚本
    pause
)