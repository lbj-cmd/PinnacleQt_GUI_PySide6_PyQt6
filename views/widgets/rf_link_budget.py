# -*- coding: utf-8 -*-# Name:         rf_link_budget.py# Author:       小菜# Date:         2025/05/20 00:00# Description:  RF链路预算面板

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QLabel, QHeaderView
)
from PySide6.QtCore import Qt
import math
from math import log10

class RFLinkBudget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.setup_connections()
        self.update_calculations()

    def init_ui(self):
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)

        # 标题
        title_label = QLabel("RF 链路预算")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(title_label)

        # 按钮布局
        button_layout = QHBoxLayout()
        self.btn_add_stage = QPushButton("添加一级")
        self.btn_add_stage.setMinimumWidth(100)
        button_layout.addWidget(self.btn_add_stage)

        self.btn_remove_stage = QPushButton("删除一级")
        self.btn_remove_stage.setMinimumWidth(100)
        button_layout.addWidget(self.btn_remove_stage)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        # 表格
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["组件类型", "增益 (dB)", "噪声系数 (dB)"])
        self.table.setRowCount(0)

        # 设置表头自适应
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        # 设置表格编辑
        self.table.setEditTriggers(QTableWidget.DoubleClicked | QTableWidget.EditKeyPressed)
        main_layout.addWidget(self.table)

        # 结果显示
        result_layout = QVBoxLayout()

        self.lbl_total_gain = QLabel("总增益 (dB): 0.0")
        self.lbl_total_gain.setStyleSheet("font-size: 16px; font-weight: bold;")
        result_layout.addWidget(self.lbl_total_gain)

        self.lbl_total_nf = QLabel("总噪声系数 (dB): 0.0")
        self.lbl_total_nf.setStyleSheet("font-size: 16px; font-weight: bold;")
        result_layout.addWidget(self.lbl_total_nf)

        result_layout.addStretch()
        main_layout.addLayout(result_layout)

    def setup_connections(self):
        self.btn_add_stage.clicked.connect(self.add_stage)
        self.btn_remove_stage.clicked.connect(self.remove_stage)
        self.table.cellChanged.connect(self.update_calculations)

    def add_stage(self):
        row = self.table.rowCount()
        self.table.insertRow(row)

        # 默认组件类型
        type_item = QTableWidgetItem("放大器")
        # 保持可编辑状态
        self.table.setItem(row, 0, type_item)

        # 默认增益
        gain_item = QTableWidgetItem("10.0")
        gain_item.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row, 1, gain_item)

        # 默认噪声系数
        nf_item = QTableWidgetItem("1.5")
        nf_item.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row, 2, nf_item)

        self.update_calculations()

    def remove_stage(self):
        if self.table.rowCount() > 0:
            self.table.removeRow(self.table.rowCount() - 1)
            self.update_calculations()

    def update_calculations(self):
        try:
            # 暂时阻止表格的cellChanged信号，避免编辑时的重影问题
            self.table.blockSignals(True)
            total_gain_db = 0.0
            total_nf_linear = 0.0
            accumulated_gain_linear = 1.0  # 累积增益（线性）

            row_count = self.table.rowCount()
            if row_count == 0:
                total_gain_db = 0.0
                total_nf_db = 0.0
            else:
                for row in range(row_count):
                    # 获取增益值
                    gain_item = self.table.item(row, 1)
                    gain_db = float(gain_item.text()) if gain_item and gain_item.text() else 0.0
                    total_gain_db += gain_db
                    gain_linear = 10 ** (gain_db / 10.0)

                    # 获取噪声系数值
                    nf_item = self.table.item(row, 2)
                    nf_db = float(nf_item.text()) if nf_item and nf_item.text() else 0.0
                    nf_linear = 10 ** (nf_db / 10.0)

                    # 使用Friis公式计算总噪声系数 - 正确顺序：先计算当前级对噪声系数的贡献，再累积增益
                    if row == 0:
                        total_nf_linear = nf_linear
                    else:
                        total_nf_linear += (nf_linear - 1) / accumulated_gain_linear

                    # 累积增益必须在当前级噪声系数计算完成后再更新
                    accumulated_gain_linear *= gain_linear

                # 转换线性噪声系数为dB - 正确公式：10 * log10(total_nf_linear)
                total_nf_db = 10 * (log10(total_nf_linear)) if total_nf_linear > 0 else 0.0

            # 更新显示
            self.lbl_total_gain.setText(f"总增益 (dB): {total_gain_db:.2f}")
            self.lbl_total_nf.setText(f"总噪声系数 (dB): {total_nf_db:.2f}")
        except Exception as e:
            # 如果有错误，显示默认值
            self.lbl_total_gain.setText("总增益 (dB): 错误")
            self.lbl_total_nf.setText("总噪声系数 (dB): 错误")
        finally:
            # 恢复表格的信号
            self.table.blockSignals(False)