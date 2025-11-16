# -*- coding: utf-8 -*-
# Name:         s_parameter_viewer.py
# Author:       小菜
# Date:         2024/11/15 00:00
# Description: S参数查看器面板

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
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QFileDialog,
    QLabel, QSizePolicy
)


class SParameterViewer(QWidget):
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
        self.load_btn = QPushButton("加载 .s2p 文件")
        self.load_btn.setCursor(Qt.PointingHandCursor)
        control_layout.addWidget(self.load_btn)

        # 参数选择下拉框
        self.param_combo = QComboBox()
        self.param_combo.addItems(["S11", "S12", "S21", "S22"])
        # 设置下拉框宽度自动调整
        self.param_combo.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        # 设置属性以解决文字重影问题
        # 设置白色框黑体样式
        self.param_combo.setStyleSheet('''QComboBox {
            background-color: white;
            color: black;
            border: 1px solid #ccc;
            padding: 5px;
            font-size: 12px;
            font-family: "Microsoft YaHei", SimHei, sans-serif;
            font-weight: bold;
            outline: none;
            min-width: 100px;
        }
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 25px;
            border-left: 1px solid #ccc;
        }
        QComboBox::down-arrow {
            image: url(:/icons/cil-caret-bottom.png);
        }
        QComboBox QAbstractItemView {
            background-color: white;
            color: black;
            border: 1px solid #ccc;
            selection-background-color: #e0e0e0;
            font-size: 12px;
            font-family: "Microsoft YaHei", SimHei, sans-serif;
            font-weight: bold;
        }''')
        control_layout.addWidget(self.param_combo)

        # 信息标签
        self.info_label = QLabel("请加载 .s2p 文件")
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

        # 初始化图表
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("S参数对数幅度")
        self.ax.set_xlabel("频率 (GHz)")
        self.ax.set_ylabel("幅度 (dB)")
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.canvas.draw()

    def setup_connections(self):
        self.load_btn.clicked.connect(self.load_s2p_file)
        self.param_combo.currentTextChanged.connect(self.plot_selected_param)

    def load_s2p_file(self):
        # 打开文件对话框
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择 .s2p 文件", "", "S参数文件 (*.s2p)"
        )
        if not file_path:
            return

        try:
            # 读取S参数文件
            self.network = rf.Network(file_path)
            file_name = os.path.basename(file_path)
            self.info_label.setText(f"已加载: {file_name}")
            
            # 绘制默认参数
            self.plot_selected_param(self.param_combo.currentText())
        except Exception as e:
            self.info_label.setText(f"加载失败: {str(e)}")
            self.network = None

    def plot_selected_param(self, param):
        if self.network is None:
            return

        # 清除旧图表
        self.ax.clear()

        # 设置标题和坐标轴
        self.ax.set_title(f"S参数对数幅度 - {param}")
        self.ax.set_xlabel("频率 (GHz)")
        self.ax.set_ylabel("幅度 (dB)")
        self.ax.grid(True, linestyle='--', alpha=0.7)

        try:
            # 解析参数
            port1 = int(param[1]) - 1
            port2 = int(param[2]) - 1

            # 获取频率和幅度数据
            freq_ghz = self.network.f / 1e9
            mag_db = rf.mag_2_db(self.network.s[:, port2, port1])

            # 绘制曲线
            self.ax.plot(freq_ghz, mag_db, linewidth=2, label=param)
            self.ax.legend(loc='upper right')

            # 自动调整坐标轴范围
            self.ax.relim()
            self.ax.autoscale_view()

            # 更新画布
            self.canvas.draw()
        except Exception as e:
            self.info_label.setText(f"绘图失败: {str(e)}")