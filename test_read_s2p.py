# -*- coding: utf-8 -*-
import skrf as rf
import matplotlib.pyplot as plt
import numpy as np

# 测试读取文件
try:
    n = rf.Network('test_s2p.s2p')
    print('文件读取成功')
    print(f'频率点数: {len(n.f)}')
    print(f'S参数形状: {n.s.shape}')
    print(f'频率: {n.f[0]/1e9:.1f} GHz 到 {n.f[-1]/1e9:.1f} GHz')
    
    # 测试绘制单个参数
    plt.figure()
    freq_ghz = n.f / 1e9
    mag_db_s11 = rf.mag_2_db(np.abs(n.s[:, 0, 0]))
    mag_db_s21 = rf.mag_2_db(np.abs(n.s[:, 1, 0]))
    
    plt.plot(freq_ghz, mag_db_s11, label='S11', linewidth=2)
    plt.plot(freq_ghz, mag_db_s21, label='S21', linewidth=2)
    plt.xlabel('频率 (GHz)')
    plt.ylabel('幅度 (dB)')
    plt.title('S参数对数幅度')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig('test_plot.png', dpi=150)
    plt.close()
    print('绘制成功，生成test_plot.png')
    
except Exception as e:
    print('错误:', str(e))
    import traceback
    traceback.print_exc()