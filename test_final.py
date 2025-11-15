#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终测试脚本 - 验证史密斯圆图绘制功能
"""

import skrf as rf
import matplotlib.pyplot as plt
import numpy as np
import os

def main():
    # 创建测试网络
    freq = rf.Frequency(0.1, 10, 100, 'GHz')
    network = rf.Network()
    network.f = freq.f
    network.s = np.zeros((len(freq), 1, 1), dtype=complex)
    
    # 创建简单的S11数据
    for i in range(len(freq)):
        f = freq.f[i]
        # 模拟一个简单的阻抗
        network.s[i, 0, 0] = (50 - 1j*(1000/(2*np.pi*f))) / (50 + 1j*(1000/(2*np.pi*f)))
    
    try:
        # 绘制方式1：使用network.plot_s_smith()
        print("正在使用network.plot_s_smith()绘制...")
        fig, ax = plt.subplots(figsize=(8, 8))
        network.plot_s_smith(m=0, n=0, ax=ax, draw_labels=True)
        ax.set_title("Smith Chart - S11 (Method 1)")
        plt.tight_layout()
        plt.savefig("final_test_1.png", dpi=150, bbox_inches='tight', fontsize=10)
        plt.close()
        print("✅ 方式1绘制成功！")
        
        # 绘制方式2：手动绘制
        print("\n正在使用手动方式绘制...")
        fig, ax = plt.subplots(figsize=(8, 8))
        # 绘制史密斯圆图背景
        rf.plotting.smith(ax=ax, draw_labels=True, border=True)
        # 绘制S11数据
        s11 = network.s[:, 0, 0]
        ax.plot(s11.real, s11.imag, 'r-', linewidth=2, label='S11')
        ax.legend(loc='upper right')
        ax.set_title("Smith Chart - S11 (Method 2)")
        plt.tight_layout()
        plt.savefig("final_test_2.png", dpi=150, bbox_inches='tight', fontsize=10)
        plt.close()
        print("✅ 方式2绘制成功！")
        
        print("\n🎉 所有测试绘制完成！")
        return True
        
    except Exception as e:
        print(f"❌ 绘制失败：{e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()