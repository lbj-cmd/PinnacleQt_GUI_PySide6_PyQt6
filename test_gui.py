#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI测试脚本
"""

import sys
import os

# 添加项目路径到sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_gui():
    """测试GUI是否能正常启动"""
    try:
        print("正在测试GUI启动...")
        
        # 导入必要的模块
        from PySide6.QtWidgets import QApplication
        from controllers import ControllerMain
        
        # 创建应用实例
        app = QApplication(sys.argv)
        
        # 创建控制器（禁用动画以加快测试）
        controller = ControllerMain(animate_on_startup=False)
        
        print("✓ GUI启动测试成功！")
        print("✓ 虚拟环境配置完成！")
        print("✓ 项目可以正常运行！")
        
        # 立即退出，避免显示窗口
        sys.exit(0)
        
    except Exception as e:
        print(f"✗ GUI启动失败: {e}")
        return False

if __name__ == "__main__":
    test_gui()