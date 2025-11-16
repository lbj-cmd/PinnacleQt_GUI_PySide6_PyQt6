# -*- coding: utf-8 -*- 
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSlider, QLabel, QHBoxLayout
from PySide6.QtCore import Qt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D

class AntennaPattern3D(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.setup_connections()
        self.N = 4  # 默认单元数量
        self.plot_pattern()

    def init_ui(self):
        # 创建主布局
        main_layout = QVBoxLayout(self)

        # 创建滑块控件
        slider_layout = QHBoxLayout()
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(2, 10)
        self.slider.setValue(4)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1)
        
        self.label = QLabel(f"单元数量 N: {self.slider.value()}")
        
        slider_layout.addWidget(QLabel("单元数量 N:"))
        slider_layout.addWidget(self.slider)
        slider_layout.addWidget(self.label)
        slider_layout.addStretch()

        # 创建matplotlib图表
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111, projection='3d')

        # 将控件添加到主布局
        main_layout.addLayout(slider_layout)
        main_layout.addWidget(self.canvas)

        # 设置布局
        self.setLayout(main_layout)

    def setup_connections(self):
        self.slider.valueChanged.connect(self.on_slider_changed)

    def on_slider_changed(self, value):
        self.N = value
        self.label.setText(f"单元数量 N: {value}")
        self.plot_pattern()

    def plot_pattern(self):
        # 清空图表
        self.ax.clear()

        # 计算天线方向图
        theta, phi, pattern = self.calculate_antenna_pattern()

        # 绘制3D曲面
        self.ax.plot_surface(theta, phi, pattern, cmap='viridis', edgecolor='none')

        # 设置坐标轴标签
        self.ax.set_xlabel('Theta (radians)')
        self.ax.set_ylabel('Phi (radians)')
        self.ax.set_zlabel('Radiation Intensity')
        self.ax.set_title(f'3D Antenna Pattern (N={self.N})')

        # 刷新画布
        self.canvas.draw()

    def calculate_antenna_pattern(self):
        """计算简单偶极子天线阵列的3D辐射方向图"""
        # 创建网格
        theta = np.linspace(0, np.pi, 100)
        phi = np.linspace(0, 2 * np.pi, 100)
        theta, phi = np.meshgrid(theta, phi)

        # 偶极子天线的方向图（E面）
        e_pattern = np.sin(theta)

        # 阵列因子
        d = 0.5  # 单元间距（波长）
        k = 2 * np.pi / 1.0  # 波数
        psi = k * d * np.cos(theta)  # 相位差
        psi_half = psi / 2
        # 处理除以零的情况，当psi_half接近0时，sin(N*psi_half)/sin(psi_half) ≈ N
        af = np.where(np.abs(psi_half) < 1e-6, self.N, np.abs(np.sin(self.N * psi_half) / np.sin(psi_half)))

        # 总方向图
        total_pattern = e_pattern * af

        return theta, phi, total_pattern