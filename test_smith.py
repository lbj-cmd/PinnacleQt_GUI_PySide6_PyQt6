import skrf as rf
import matplotlib.pyplot as plt

# 创建一个简单的网络
freq = rf.Frequency(0.1, 10, 101, 'GHz')
network = rf.Network(frequency=freq, s=[[0.5+0.5j]]) 

# 绘制史密斯圆图
fig, ax = plt.subplots()
rf.plotting.smith(ax=ax, draw_labels=True)
ax.plot(network.s[:,0,0].real, network.s[:,0,0].imag, 'r-')
plt.title('S11 Smith Chart')
plt.close()
print("史密斯圆图绘制成功")