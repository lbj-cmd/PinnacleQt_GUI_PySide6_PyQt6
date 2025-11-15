# -*- coding: utf-8 -*-
# Name:         main_window.py
# Author:       小菜
# Date:         2024/4/01 00:00
# Description:

import sys
from typing import (Tuple, Union)

from PySide6.QtCore import (Qt, QTimer, QEvent, QPoint, QRect, QPropertyAnimation, QParallelAnimationGroup, QCoreApplication, QSize)
from PySide6.QtGui import (QIcon, QCursor)
from PySide6.QtWidgets import (QMainWindow, QApplication, QSizeGrip, QPushButton, QSizePolicy, QWidget, QTextEdit, QLabel)

from config import (DarkConfig, LightConfig)
from views.ui_components import (create_width_animation, create_animation_group, apply_shadow_effect)
from views.ui_designs import Ui_MainWindow
from views.widgets import CustomGrip


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #
        self.is_maximum_size: bool = bool(0)
        self.left_grip: CustomGrip = None
        self.right_grip: CustomGrip = None
        self.top_grip: CustomGrip = None
        self.bottom_grip: CustomGrip = None
        self.sizegrip: QSizeGrip = None
        self.animation: QPropertyAnimation = None
        self.animation_group: QParallelAnimationGroup = None
        self.move_position: QPoint = QPoint(0, 0)
        #
        self.dark_theme: bool = bool(1)
        self.current_selected_btn: str = 'btn_home'
        self.config = DarkConfig
        #
        self.timer = QTimer()
        self.initialize_new_panels()
        self.initialize_view()
        self.setup_connections()

    # noinspection PyTypeChecker
    def set_theme(self):
        """在应用程序中切换浅色和深色主题。
        此方法清除当前样式，应用全局主题样式，并根据所选主题调整特定小部件的样式。"""
        # 清空显性的样式，两个设置按钮 和 菜单选中的按钮
        self.toggle_setting_btn_style()
        self.toggle_selected_btn_style(is_add=False)

        # 切换主题
        self.config = LightConfig if self.dark_theme else DarkConfig
        self.dark_theme = not self.dark_theme
        theme_name = "浅色" if self.dark_theme else "深色"
        
        # 设置全局的新样式，新主题
        with open(self.config.QSS_FILE, mode='r', encoding='utf-8') as f:
            self.styleSheet.setStyleSheet(f.read())
        # 设置部件的样式
        for widget_name, style in self.config.MANUAL_STYLES.items():
            widget = getattr(self, widget_name, None)
            widget.setStyleSheet(style)

        # 设置当前选中的按钮的颜色
        btn: QPushButton = self.findChild(QPushButton, self.current_selected_btn)
        self.toggle_selected_btn_style(btn)

        # 添加两个设置按钮的颜色，如果有展开的话
        self.toggle_setting_btn_style(add_default_style=True)
        
        # 记录主题切换日志
        import logging
        logging.info(f"主题已切换为 {theme_name} 主题")

        # 添加主题切换日志
        import logging
        theme_name = "浅色" if self.dark_theme else "深色"
        logging.info(f"主题切换为: {theme_name}主题")

    def initialize_view(self):
        """初始化视图"""
        self.initialize_title()
        #
        self.initialize_border_effects()
        #
        self.initialize_window_resizing()
        #
        self.toggle_selected_btn_style(self.btn_home)
        # 无边框
        self.setWindowFlag(Qt.FramelessWindowHint)
        # 半透明
        self.setAttribute(Qt.WA_TranslucentBackground)

    def initialize_new_panels(self):
        """初始化新面板"""
        # 添加日志查看器按钮
        self.btn_logs = QPushButton(self.topMenu)
        self.btn_logs.setObjectName("btn_logs")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(self.btn_logs.sizePolicy().hasHeightForWidth())
        self.btn_logs.setSizePolicy(sizePolicy)
        self.btn_logs.setMinimumSize(QSize(0, 45))
        self.btn_logs.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_logs.setLayoutDirection(Qt.LeftToRight)
        self.btn_logs.setStyleSheet(u"background-image: url(:/icons/icons/cil-notes.png);")
        self.btn_logs.setText(QCoreApplication.translate("MainWindow", u"Logs", None))
        self.verticalLayout_8.addWidget(self.btn_logs)

        # 添加系统监控按钮
        self.btn_monitor = QPushButton(self.topMenu)
        self.btn_monitor.setObjectName("btn_monitor")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(self.btn_monitor.sizePolicy().hasHeightForWidth())
        self.btn_monitor.setSizePolicy(sizePolicy)
        self.btn_monitor.setMinimumSize(QSize(0, 45))
        self.btn_monitor.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_monitor.setLayoutDirection(Qt.LeftToRight)
        self.btn_monitor.setStyleSheet(u"background-image: url(:/icons/icons/cil-chart.png);")
        self.btn_monitor.setText(QCoreApplication.translate("MainWindow", u"Monitor", None))
        self.verticalLayout_8.addWidget(self.btn_monitor)

        # 添加日志查看器页面
        self.logs_page = QWidget()
        self.logs_page.setObjectName("logs_page")
        self.text_edit_logs = QTextEdit(self.logs_page)
        self.text_edit_logs.setGeometry(QRect(10, 10, 800, 600))
        self.text_edit_logs.setStyleSheet("background-color: #1e1e1e; color: #cccccc;")
        self.stackedWidget.addWidget(self.logs_page)

        # 添加系统监控页面
        self.monitor_page = QWidget()
        self.monitor_page.setObjectName("monitor_page")
        self.label_cpu = QLabel(self.monitor_page)
        self.label_cpu.setGeometry(QRect(10, 10, 200, 30))
        self.label_cpu.setStyleSheet("font-size: 16px;")
        self.label_memory = QLabel(self.monitor_page)
        self.label_memory.setGeometry(QRect(10, 50, 200, 30))
        self.label_memory.setStyleSheet("font-size: 16px;")
        self.stackedWidget.addWidget(self.monitor_page)

        # 设置日志捕获器
        import logging
        # 创建日志捕获器
        self.log_handler = logging.StreamHandler(self)
        self.log_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.log_handler.setFormatter(formatter)
        # 移除所有已存在的处理器
        for handler in logging.getLogger('').handlers[:]:
            logging.getLogger('').removeHandler(handler)
        # 添加我们的日志捕获器
        logging.getLogger('').addHandler(self.log_handler)
        # 设置root logger的级别为INFO
        logging.getLogger('').setLevel(logging.INFO)
        # 测试日志
        logging.info("日志查看器已初始化")

    def setup_connections(self):
        """事件绑定"""
        # 标题栏事件
        self.titleRightInfo.mouseMoveEvent = self.move_window
        self.titleRightInfo.mouseDoubleClickEvent = self.double_click_maximize_restore

        # 设置按钮点击事件
        self.settingsTopBtn.clicked.connect(self.linkage_animation)
        self.toggleLeftBox.clicked.connect(self.linkage_animation)
        self.extraCloseColumnBtn.clicked.connect(self.linkage_animation)

        # 菜单按钮点击事件
        self.toggleButton.clicked.connect(self.toggle_menu)
        self.btn_home.clicked.connect(self.switch_page)
        self.btn_widgets.clicked.connect(self.switch_page)
        self.btn_new.clicked.connect(self.switch_page)
        self.btn_save.clicked.connect(self.switch_page)
        self.btn_logs.clicked.connect(self.switch_page)
        self.btn_monitor.clicked.connect(self.switch_page)
        self.toggleTheme.clicked.connect(self.set_theme)

        # 最大最小化点击事件
        self.minimizeAppBtn.clicked.connect(self.showMinimized)
        self.maximizeRestoreAppBtn.clicked.connect(self.maximize_restore)
        self.closeAppBtn.clicked.connect(self.close)

        # 系统监控定时器
        self.timer.timeout.connect(self.update_system_info)
        self.timer.start(2000)

    def initialize_title(self):
        """设置title"""
        # 设置标题
        title = "PyDracula - Modern GUI"
        description = "PyDracula APP - Theme with colors based on Dracula for Python."
        self.setWindowTitle(title)
        self.titleRightInfo.setText(description)

    def initialize_window_resizing(self):
        """可调整窗口尺寸"""
        self.sizegrip = QSizeGrip(self.frame_size_grip)
        self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")

    def initialize_border_effects(self):
        """初始化自定义边框并为窗口应用阴影效果。"""
        # 添加窗口阴影和边框
        self.left_grip = CustomGrip(self, Qt.LeftEdge, True)
        self.right_grip = CustomGrip(self, Qt.RightEdge, True)
        self.top_grip = CustomGrip(self, Qt.TopEdge, True)
        self.bottom_grip = CustomGrip(self, Qt.BottomEdge, True)

        # 阴影效果
        apply_shadow_effect(self.bgApp)

    def maximize_restore(self):
        """最大化窗口和还原"""
        if not self.is_maximum_size:
            self.showMaximized()
            self.appMargins.setContentsMargins(0, 0, 0, 0)
            self.maximizeRestoreAppBtn.setToolTip("Restore")
            self.maximizeRestoreAppBtn.setIcon(QIcon(u":/icons/icons/icon_restore.png"))
            self.frame_size_grip.hide()
            self.left_grip.hide()
            self.right_grip.hide()
            self.top_grip.hide()
            self.bottom_grip.hide()
        else:
            self.showNormal()
            self.resize(self.width() + 1, self.height() + 1)
            self.appMargins.setContentsMargins(10, 10, 10, 10)
            self.maximizeRestoreAppBtn.setToolTip("Maximize")
            self.maximizeRestoreAppBtn.setIcon(QIcon(u":/icons/icons/icon_maximize.png"))
            self.frame_size_grip.show()
            self.left_grip.show()
            self.right_grip.show()
            self.top_grip.show()
            self.bottom_grip.show()
        self.is_maximum_size = not self.is_maximum_size

    def toggle_menu(self):
        """切换菜单"""
        # GET TARGET WIDTH
        target_width = self.config.MENU_WIDTH if self.leftMenuBg.width() == 60 else 60

        # ANIMATION
        self.animation = create_width_animation(self.leftMenuBg, target_width)
        self.animation.start()

    # noinspection PyTypeChecker
    def toggle_selected_btn_style(self, widget=None, is_add=True):
        """清空菜单栏已选择按钮的样式

        Args:
            widget:
            is_add(bool): 是否为添加样式

        Returns:

        """
        if not widget:
            widget: QPushButton = self.findChild(QPushButton, self.current_selected_btn)

        if is_add:
            widget.setStyleSheet(widget.styleSheet() + self.config.MENU_SELECTED_STYLESHEET)
        else:
            widget.setStyleSheet(widget.styleSheet().replace(self.config.MENU_SELECTED_STYLESHEET, ''))
        # print(widget.objectName(), widget.styleSheet())

    def toggle_setting_btn_style(self, add_default_style=False) -> Union[Tuple[int, int], None]:
        """根据方向和是否添加的标志，切换给定控件的样式。

        Args:
            add_default_style(bool): 是否为两个设置按钮添加默认的样式

        Returns:
            关于动画组移动的元组 或 None
        """
        color_map = {
            'left': self.config.BTN_LEFT_BOX_COLOR,
            'right': self.config.BTN_RIGHT_BOX_COLOR,
        }

        direction_map = {
            'toggleLeftBox': 'left',
            'extraCloseColumnBtn': 'left',
            'settingsTopBtn': 'right'
        }

        # 获取触发当前动画的按钮 和 动画触发方向
        btn = self.sender()
        direction = direction_map.get(btn.objectName())
        left_style = self.toggleLeftBox.styleSheet()
        right_style = self.settingsTopBtn.styleSheet()

        # 计算左右侧面板应该展开或收起的目标宽度
        left_width = self.extraLeftBox.width()
        right_width = self.extraRightBox.width()
        target_left_width = self.config.LEFT_BOX_WIDTH if (left_width == 0 and direction == "left") else 0
        target_right_width = self.config.RIGHT_BOX_WIDTH if (right_width == 0 and direction == "right") else 0

        # 先判断是否为添加默认样式
        if add_default_style:
            self.toggleLeftBox.setStyleSheet(left_style + color_map.get('left')) if left_width else None
            self.settingsTopBtn.setStyleSheet(right_style + color_map.get('right')) if right_width else None
            return

        # 根据当前面板的宽度和方向，调整按钮样式
        if target_left_width and not target_right_width:
            # 展开左侧面板，应用左侧按钮样式，并移除右侧按钮样式
            self.toggleLeftBox.setStyleSheet(left_style + color_map.get('left'))
            self.settingsTopBtn.setStyleSheet(right_style.replace(color_map.get('right'), ''))
        elif not target_left_width and target_right_width:
            # 展开右侧面板，应用右侧按钮样式，并移除左侧按钮样式
            self.toggleLeftBox.setStyleSheet(left_style.replace(color_map.get('left'), ''))
            self.settingsTopBtn.setStyleSheet(right_style + color_map.get('right'))
        else:
            # 如果没有特定方向，移除触发按钮的样式
            self.toggleLeftBox.setStyleSheet(left_style.replace(color_map.get('left'), ''))
            self.settingsTopBtn.setStyleSheet(right_style.replace(color_map.get('right'), ''))

        return target_left_width, target_right_width

    def linkage_animation(self):
        """根据触发动画的按钮，计算并执行侧边面板的展开或收起动画。

        根据触发器（按钮）的objectName映射到对应的动画方向，计算出左右侧面板的目标宽度，并对相应的按钮样式进行添加或移除。最后，创建并启动包含两个动画的并行动画组。
        """
        # 获取需要移动的目标距离
        target_left_width, target_right_width = self.toggle_setting_btn_style()

        # 对左右面板执行展开或收起的动画
        left_box = create_width_animation(self.extraLeftBox, target_left_width)
        right_box = create_width_animation(self.extraRightBox, target_right_width)

        # GROUP ANIMATION
        self.animation_group = create_animation_group([left_box, right_box])
        self.animation_group.start()

    def switch_page(self):
        """
        切换页面
        """
        page_map = {
            'btn_home': 0,
            'btn_widgets': 1,
            'btn_new': 2,
            'btn_logs': 3,
            'btn_monitor': 4,
        }
        selected_btn = self.sender()
        selected_btn_name: str = selected_btn.objectName()
        if selected_btn_name in page_map:
            index = page_map[selected_btn_name]
            if index == self.stackedWidget.currentIndex():
                return
            # 切换页面
            QTimer.singleShot(150, lambda: self.stackedWidget.setCurrentIndex(index))
            # 设置未被选中按钮样式
            self.toggle_selected_btn_style(is_add=False)
            # 设置选中的按钮样式
            self.toggle_selected_btn_style(selected_btn)
            # 记录当前选中的按钮
            self.current_selected_btn = selected_btn_name
        print(f'Button "{selected_btn_name}" pressed!')

    def update_system_info(self):
        """更新系统信息"""
        import psutil
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        self.label_cpu.setText(f"CPU 使用率: {cpu_percent}%")
        self.label_memory.setText(f"内存 使用率: {memory_percent}%")

    def emit(self, record):
        """日志捕获器的emit方法"""
        log_entry = self.log_handler.formatter.format(record)
        self.text_edit_logs.append(log_entry)

    def write(self, message):
        """日志捕获器的write方法"""
        if message.strip():
            self.text_edit_logs.append(message.strip())

    def flush(self):
        """日志捕获器的flush方法"""
        pass

    def double_click_maximize_restore(self, event):
        """双击标题控件事件"""
        # IF DOUBLE CLICK CHANGE STATUS
        if event.type() == QEvent.MouseButtonDblClick:
            QTimer.singleShot(250, self.maximize_restore)

    def move_window(self, event=None):
        """窗口拖动"""
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.move_position)
            event.accept()

    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() == Qt.LeftButton:
            self.move_position = event.globalPosition().toPoint() - self.pos()
            event.accept()

    def resizeEvent(self, event):
        """处理窗口大小调整事件"""
        self.left_grip.setGeometry(0, 10, 10, self.height())
        self.right_grip.setGeometry(self.width() - 10, 10, 10, self.height())
        self.top_grip.setGeometry(0, 0, self.width(), 10)
        self.bottom_grip.setGeometry(0, self.height() - 10, self.width(), 10)


if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    sys.exit(app.exec())
