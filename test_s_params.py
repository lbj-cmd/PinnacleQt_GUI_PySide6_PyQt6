# -*- coding: utf-8 -*-
# 测试S参数查看器的功能

import sys
import os
import tempfile
import numpy as np
import skrf as rf

print("skrf版本:", rf.__version__)
print("numpy版本:", np.__version__)

# 检查Network类的属性
print("\nNetwork类的属性:")
print([attr for attr in dir(rf.Network) if not attr.startswith('_')])

# 使用skrf内置的示例数据测试
print("\n\n测试使用内置示例数据:")
try:
    # 创建一个简单的Network对象
    freq = rf.Frequency(0, 1, 10, 'GHz')
    # 创建一个2端口网络
    n = rf.Network(
        frequency=freq,
        s=np.random.randn(len(freq.f), 2, 2) + 1j * np.random.randn(len(freq.f), 2, 2),
        z0=50
    )
    print("Network创建成功")
    print(f"频率点数: {len(n.f)}")
    print(f"S参数形状: {n.s.shape}")
    print(f"特征阻抗: {n.z0}")
    print(f"默认端口阻抗: {n.z0[0] if hasattr(n, 'z0') and n.z0.ndim > 0 else n.z0}")
    
    # 保存为.s2p文件
    test_file = tempfile.mktemp(suffix='.s2p')
    n.write_touchstone(test_file, z0=50)
    print(f"\n保存文件成功: {test_file}")
    
    # 读取文件
    n2 = rf.Network(test_file)
    print("读取文件成功")
    print(f"读取后S参数形状: {n2.s.shape}")
    print(f"S11: {n2.s[0, 0, 0]}")
    
    # 清理
    os.remove(test_file)
    print(f"\n测试文件已删除: {test_file}")
    
except Exception as e:
    print("错误:", str(e))
    import traceback
    traceback.print_exc()

print("\n\n测试直接创建2端口网络:")
try:
    f = np.linspace(0, 1e9, 101)
    s11 = 0.1 * np.exp(-1j * 2 * np.pi * f * 0.1e-9)
    s21 = 0.9 * np.exp(-1j * 2 * np.pi * f * 0.2e-9)
    s12 = 0.9 * np.exp(-1j * 2 * np.pi * f * 0.2e-9)
    s22 = 0.1 * np.exp(-1j * 2 * np.pi * f * 0.1e-9)
    
    s_data = np.array([[s11, s12], [s21, s22]]).T
    print(f"创建的S数据形状: {s_data.shape}")
    
    n = rf.Network(f=f, s=s_data, z0=50)
    print("Network创建成功")
    
except Exception as e:
    print("错误:", str(e))
    import traceback
    traceback.print_exc()