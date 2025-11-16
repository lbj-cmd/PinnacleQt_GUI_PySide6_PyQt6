# 虚拟环境配置说明

## 快速开始

### 方法一：使用自动配置脚本（推荐）

1. **双击运行** `setup_project.bat`
2. 脚本会自动：
   - 创建虚拟环境
   - 安装所有依赖
   - 激活虚拟环境

### 方法二：手动配置

1. **创建虚拟环境**：
   ```bash
   python -m venv venv
   ```

2. **激活虚拟环境**：
   - Windows CMD: `venv\Scripts\activate.bat`
   - Windows PowerShell: `venv\Scripts\Activate.ps1`
   - 或者双击运行：`activate_venv.bat`

3. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```

4. **运行项目**：
   ```bash
   python main.py
   ```

## 项目依赖

- **PySide6**: Qt for Python 框架
- **PyQt6**: 备用的 Qt 框架
- **setuptools**: Python 包管理工具
- **wheel**: Python 包构建工具

## 注意事项

1. 确保已安装 Python 3.8+ 版本
2. 在运行项目前，请确保虚拟环境已激活
3. 虚拟环境会隔离项目依赖，避免与系统Python冲突

## 常用命令

- **激活虚拟环境**: `activate_venv.bat`
- **退出虚拟环境**: `deactivate`
- **查看已安装包**: `pip list`
- **更新依赖**: `pip install --upgrade -r requirements.txt`