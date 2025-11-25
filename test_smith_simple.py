#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试使用network.plot_s_smith()方法
"""

import skrf as rf
import matplotlib.pyplot as plt
import numpy as np

# 创建频率
freq = rf.Frequency(0.1, 10, 100, 'GHz')

# 创建一个简单的网络
network = rf.Network()
network.f = freq.f
network.s = np.zeros((len(freq), 1, 1), dtype=complex)

# 填充S11数据 - 简单的RC负载
for i in range(len(freq)):
    f = freq.f[i]
    # 模拟RC低通滤波器的S11
    network.s[i, 0, 0] = (1 - 1j*(f/1e9)) / (1 + 1j*(f/1e9))

# 测试不同的绘制方法
print("测试1：直接使用network.plot_s_smith()")
try:
    fig, ax = plt.subplots(figsize=(8, 8))
    network.plot_s_smith(m=0, n=0, ax=ax, draw_labels=True)
    ax.set_title("史密斯圆图 - S11")
    plt.tight_layout()
    plt.savefig("test_smith_simple.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ 绘制成功！")
except Exception as e:
    print(f"❌ 绘制失败：{e}")
    import traceback
    traceback.print_exc()

print("\n测试2：仅绘制史密斯圆图背景")
try:
    fig, ax = plt.subplots(figsize=(8, 8))
    rf.plotting.smith(ax=ax, draw_labels=True)
    ax.set_title("史密斯圆图背景")
    plt.tight_layout()
    plt.savefig("test_smith_background.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ 绘制成功！")
except Exception as e:
    print(f"❌ 绘制失败：{e}")
    import traceback
    traceback.print_exc()

print("\n测试3：手动绘制数据")
try:
    fig, ax = plt.subplots(figsize=(8, 8))
    # 绘制背景
    rf.plotting.smith(ax=ax, draw_labels=True)
    # 绘制数据
    s11 = network.s[:, 0, 0]
    ax.plot(s11.real, s11.imag, 'r-', linewidth=2, label='S11')
    ax.legend()
    ax.set_title("史密斯圆图 - 手动绘制")
    plt.tight_layout()
    plt.savefig("test_smith_manual.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ 绘制成功！")
except Exception as e:
    print(f"❌ 绘制失败：{e}")
    import traceback
    traceback.print_exc()