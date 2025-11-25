# -*- coding: utf-8 -*-
# Name:         smith_chart_panel.py
# Author:       小菜
# Date:         2024/4/01 00:00
# Description:  史密斯圆图面板

import skrf as rf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QFileDialog)
from PySide6.QtCore import Qt


class SmithChartPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.initialize_ui()

    def initialize_ui(self):
        """初始化UI布局"""
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        # 添加加载文件按钮
        self.load_btn = QPushButton("加载 .s1p 文件")
        self.load_btn.clicked.connect(self.load_s1p_file)
        self.layout.addWidget(self.load_btn)

        # 创建matplotlib图表区域
        self.figure = plt.figure(figsize=(8, 8))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

    def load_s1p_file(self):
        """加载s1p文件并绘制史密斯圆图"""
        file_path, _ = QFileDialog.getOpenFileName(self, "打开 .s1p 文件", "", "Touchstone files (*.s1p)")
        if file_path:
            # 加载s1p文件
            ntwk = rf.Network(file_path)
            # 清空图表
            self.figure.clear()
            # 创建轴对象
            ax = self.figure.add_subplot(111)
            # 绘制史密斯圆图背景
            rf.plotting.smith(ax=ax, chart_type='z', draw_labels=True)
            # 绘制S11参数曲线
            ax.plot(ntwk.s[:,0,0].real, ntwk.s[:,0,0].imag, label='S11')
            # 添加图例
            ax.legend()
            # 设置轴范围为史密斯圆图标准范围
            ax.axis([-1.1, 1.1, -1.1, 1.1])
            # 更新图表
            self.canvas.draw()
