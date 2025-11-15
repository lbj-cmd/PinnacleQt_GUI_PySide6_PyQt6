#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试史密斯圆图修复后的绘制功能
"""

import skrf as rf
import matplotlib.pyplot as plt

# 创建一个简单的网络
freq = rf.Frequency(0.1, 10, 100, 'GHz')
network = rf.Network()
network.f = freq.f
network.s = (0.5 + 0.5j) * freq.f / freq.f[-1] + 0.1j  # 创建一个简单的S11曲线

# 创建一个绘图区域
fig, ax = plt.subplots(figsize=(8, 8))

# 绘制史密斯圆图
try:
    rf.plotting.smith(network.s[:, 0, 0], ax=ax, draw_labels=True)
    ax.set_title("史密斯圆图 - S11")
    plt.tight_layout()
    plt.savefig("test_smith_fix.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("史密斯圆图绘制成功！已保存为test_smith_fix.png")
    print("验证内容：")
    print("1. 背景网格是否显示")
    print("2. S11红色曲线是否显示")
    print("3. 标题是否正确")
except Exception as e:
    print(f"绘制失败：{e}")
    import traceback
    traceback.print_exc()