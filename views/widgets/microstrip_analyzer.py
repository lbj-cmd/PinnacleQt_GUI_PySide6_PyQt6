# -*- coding: utf-8 -*-
# Name:         microstrip_analyzer.py
# Author:       小菜
# Date:         2024/4/01 00:00
# Description:  微带线阻抗分析功能

import math
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPainter, QPen, QFont
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSizePolicy
)


class MicrostripCrossSection(QWidget):
    """微带线横截面绘图控件"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(400, 300)
        self.w: float = 50.0  # 微带线宽度
        self.h: float = 100.0  # 介质基板厚度

    def set_dimensions(self, w: float, h: float):
        """设置微带线尺寸"""
        self.w = max(1.0, w)  # 确保不为0
        self.h = max(1.0, h)
        self.update()  # 触发重绘

    def paintEvent(self, event):
        """重写绘图事件"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), Qt.white)

        # 计算缩放比例，确保图形在控件内合理显示
        scale = min(self.width() * 0.8 / self.w, self.height() * 0.8 / self.h)
        scaled_w = self.w * scale
        scaled_h = self.h * scale

        # 计算中心位置
        center_x = self.width() / 2
        center_y = self.height() / 2

        # 绘制介质基板（灰色）
        painter.setBrush(Qt.lightGray)
        painter.drawRect(int(center_x - scaled_w / 2), int(center_y - scaled_h / 2),
                         int(scaled_w), int(scaled_h))

        # 绘制微带线（黑色）
        painter.setBrush(Qt.black)
        strip_h = scaled_h * 0.1  # 微带线厚度占基板厚度的10%
        painter.drawRect(int(center_x - scaled_w / 2), int(center_y - scaled_h / 2 - strip_h),
                         int(scaled_w), int(strip_h))

        # 绘制坐标轴
        pen = QPen(Qt.black, 1, Qt.DashLine)
        painter.setPen(pen)
        # 水平轴（W）
        painter.drawLine(int(center_x - scaled_w / 2 - 20), int(center_y),
                         int(center_x + scaled_w / 2 + 20), int(center_y))
        # 垂直轴（H）
        painter.drawLine(int(center_x), int(center_y - scaled_h / 2 - strip_h - 20),
                         int(center_x), int(center_y + scaled_h / 2 + 20))

        # 标注尺寸
        pen = QPen(Qt.red, 1)
        painter.setPen(pen)
        font = QFont("Arial", 10)
        painter.setFont(font)

        # 标注W
        painter.drawText(int(center_x), int(center_y + 20), f"W = {self.w:.2f}mm")
        # 标注H
        painter.drawText(int(center_x + 20), int(center_y - strip_h / 2), f"H = {self.h:.2f}mm")


class MicrostripAnalyzer(QWidget):
    """微带线阻抗分析主控件"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.setup_connections()
        self.calculate_z0()  # 初始计算

    def init_ui(self):
        """初始化UI布局"""
        # 主布局：左右分栏
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        self.setLayout(main_layout)

        # 左侧布局：输入参数
        left_layout = QVBoxLayout()
        left_layout.setSpacing(15)

        # 输入参数控件
        self.er_input = self.create_input_field("介电常数 Er:", "4.4")
        self.h_input = self.create_input_field("基板厚度 H (mm):", "1.0")
        self.w_input = self.create_input_field("微带线宽度 W (mm):", "1.0")
        self.t_input = self.create_input_field("微带线厚度 T (mm):", "0.035")

        # 添加到左侧布局
        left_layout.addWidget(self.er_input)
        left_layout.addWidget(self.h_input)
        left_layout.addWidget(self.w_input)
        left_layout.addWidget(self.t_input)
        left_layout.addStretch()

        # 右侧布局：绘图区域
        right_layout = QVBoxLayout()
        right_layout.setSpacing(15)

        self.drawing_area = MicrostripCrossSection()
        right_layout.addWidget(self.drawing_area)

        # 底部布局：结果显示
        self.result_label = QLabel("特性阻抗 Z0: --- Ω")
        font = self.result_label.font()
        font.setPointSize(12)
        font.setBold(True)
        self.result_label.setFont(font)
        self.result_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.result_label)

        # 添加到主布局
        main_layout.addLayout(left_layout, 1)  # 左侧占1份宽度
        main_layout.addLayout(right_layout, 3)  # 右侧占3份宽度

    def create_input_field(self, label_text: str, default_value: str) -> QWidget:
        """创建带标签的输入字段"""
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(layout)

        label = QLabel(label_text)
        label.setMinimumWidth(120)
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        input_line = QLineEdit(default_value)
        input_line.setMaximumWidth(100)
        input_line.setObjectName(label_text.split()[0])  # 设置对象名以便识别

        layout.addWidget(label)
        layout.addWidget(input_line)

        return widget

    def setup_connections(self):
        """建立信号与槽的连接"""
        # 为所有输入字段添加文本变化事件监听
        for child in self.findChildren(QLineEdit):
            child.textChanged.connect(self.on_input_changed)

    def on_input_changed(self):
        """输入变化时的处理"""
        try:
            # 获取输入值
            w = float(self.w_input.findChild(QLineEdit).text())
            h = float(self.h_input.findChild(QLineEdit).text())

            # 更新绘图区域尺寸
            self.drawing_area.set_dimensions(w, h)
            # 计算并更新结果
            self.calculate_z0()
        except ValueError:
            # 输入无效时不更新
            pass

    def calculate_z0(self):
        """计算微带线特性阻抗Z0
        采用近似公式：Z0 = (60 / sqrt(Er_eff)) * ln(8H/W + W/(4H))
        其中Er_eff = (Er + 1)/2 + (Er - 1)/2 * 1/sqrt(1 + 12H/W)
        """
        try:
            # 获取输入值
            er = float(self.er_input.findChild(QLineEdit).text())
            h = float(self.h_input.findChild(QLineEdit).text())
            w = float(self.w_input.findChild(QLineEdit).text())
            t = float(self.t_input.findChild(QLineEdit).text())  # 暂时未使用厚度修正

            # 计算有效介电常数
            er_eff = (er + 1) / 2 + (er - 1) / 2 * math.sqrt(1 + 12 * h / w)

            # 计算特性阻抗
            z0 = (60 / math.sqrt(er_eff)) * math.log(8 * h / w + w / (4 * h))

            # 显示结果
            self.result_label.setText(f"特性阻抗 Z0: {z0:.2f} Ω")
        except ValueError:
            # 输入无效时显示错误
            self.result_label.setText("特性阻抗 Z0: 输入无效")


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MicrostripAnalyzer()
    window.setWindowTitle("微带线阻抗分析")
    window.show()
    sys.exit(app.exec())