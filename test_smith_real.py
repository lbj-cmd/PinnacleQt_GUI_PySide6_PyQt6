#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用真实S1P文件测试史密斯圆图修复后的绘制功能
"""

import skrf as rf
import matplotlib.pyplot as plt
import os

def test_smith_plotting():
    """测试史密斯圆图绘制功能"""
    
    # 检查是否有test_S1p.s1p文件
    if not os.path.exists('test_S1p.s1p'):
        # 创建一个简单的S1P文件
        print("正在创建测试S1P文件...")
        freq = rf.Frequency(0.1, 1, 10, 'GHz')
        network = rf.Network(freq=freq)
        # 创建一个简单的S11响应（低通滤波器示例）
        network.s[:, 0, 0] = 0.5 / (1 + 0.5j * freq.f / 1e9)
        # 保存为S1P文件
        network.write_touchstone('test_S1p.s1p', format='ma', comment='Test S11 data')
    
    try:
        # 读取S1P文件
        print("正在读取S1P文件...")
        network = rf.read_touchstone('test_S1p.s1p')
        
        # 创建一个绘图区域
        fig, ax = plt.subplots(figsize=(8, 8))
        
        # 绘制史密斯圆图
        print("正在绘制史密斯圆图...")
        
        # 使用skrf的smith函数绘制S11参数
        # 注意：rf.plotting.smith()的第一个参数可以是网络对象或散射参数数组
        rf.plotting.smith(network, ax=ax, draw_labels=True)
        ax.set_title("史密斯圆图 - S11")
        
        # 或者可以直接传递S11参数数组
        # rf.plotting.smith(network.s[:, 0, 0], ax=ax, draw_labels=True)
        
        plt.tight_layout()
        plt.savefig("test_smith_real.png", dpi=150, bbox_inches='tight')
        plt.close()
        
        print("✅ 史密斯圆图绘制成功！已保存为test_smith_real.png")
        return True
        
    except Exception as e:
        print(f"❌ 绘制失败：{e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_smith_plotting()