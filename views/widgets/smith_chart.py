# -*- coding: utf-8 -*-# Name:         smith_chart.py
# Author:       小菜
# Date:         2024/11/15 00:00
# Description: 史密斯圆图面板

import os
import skrf as rf
import matplotlib
matplotlib.use('QtAgg')
# 配置matplotlib使用中文字体
matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
    QLabel, QSizePolicy
)


class SmithChartViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.network = None
        self.init_ui()
        self.setup_connections()

    def init_ui(self):
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 创建控制面板
        control_layout = QHBoxLayout()
        control_layout.setSpacing(10)

        # 加载文件按钮
        self.load_btn = QPushButton("加载 .s1p 文件")
        self.load_btn.setCursor(Qt.PointingHandCursor)
        control_layout.addWidget(self.load_btn)

        # 信息标签
        self.info_label = QLabel("请加载 .s1p 文件")
        self.info_label.setAlignment(Qt.AlignRight)
        control_layout.addWidget(self.info_label)

        # 设置布局伸缩
        control_layout.addStretch(1)
        main_layout.addLayout(control_layout)

        # 创建图表区域
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(self.canvas)

        # 初始化史密斯圆图
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("史密斯圆图 - S11")
        self.canvas.draw()

    def setup_connections(self):
        self.load_btn.clicked.connect(self.load_s1p_file)

    def load_s1p_file(self):
        # 打开文件对话框
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择 .s1p 文件", "", "S参数文件 (*.s1p)"
        )
        if not file_path:
            return

        try:
            # 读取S参数文件
            self.network = rf.Network(file_path)
            file_name = os.path.basename(file_path)
            self.info_label.setText(f"已加载: {file_name}")
            
            # 绘制史密斯圆图
            self.plot_smith_chart()
        except Exception as e:
            self.info_label.setText(f"加载失败: {str(e)}")
            self.network = None

    def plot_smith_chart(self):
        if self.network is None:
            return

        # 清除旧图表
        self.ax.clear()

        try:
            # 绘制史密斯圆图背景
            rf.plotting.smith(ax=self.ax, draw_labels=True, border=True)
            
            # 绘制S11参数曲线
            s11 = self.network.s[:, 0, 0]
            self.ax.plot(s11.real, s11.imag, 'r-', linewidth=2, label='S11')
            self.ax.legend(loc='upper right')
            self.ax.set_title("史密斯圆图 - S11")
            
            # 更新画布
            self.canvas.draw()
        except Exception as e:
            self.info_label.setText(f"绘图失败: {str(e)}")