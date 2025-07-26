# -*- coding: utf-8 -*-
# @Time    : 2025/7/25 22:06
# @Author  : LeurDeLis
# @File    : other_function.py
# @Software: PyCharm
import socket
import subprocess
import sys
import webbrowser
import requests
from PyQt5 import QtCore, QtWidgets, QtGui
import UI.settings_dialog as settings_dialog
import UI.about as about

def add_shadow_to_widget(widget, blur_radius=10, x_offset=0, y_offset=0, color=None):
    """
    为QWidget控件添加阴影效果（通用版本）

    参数:
        widget: QWidget控件实例（QFrame、QPushButton、QGroupBox等）
        blur_radius: 阴影模糊半径 (默认: 10)
        x_offset: 水平偏移量 (默认: 0)
        y_offset: 垂直偏移量 (默认: 0)
        color: 阴影颜色 (默认: 根据控件类型自动设置)
    """
    # 类型检查
    if not isinstance(widget, QtWidgets.QWidget):
        print(f"警告: 传入的控件不是QWidget类型，实际类型: {type(widget)}")
        return

    # 根据不同控件类型设置默认颜色
    if color is None:
        if isinstance(widget, QtWidgets.QPushButton):
            color = QtGui.QColor(0, 0, 0, 60)  # 按钮使用较浅阴影
            blur_radius = 8 if blur_radius == 10 else blur_radius  # 按钮默认模糊半径
        else:
            color = QtGui.QColor(0, 0, 0, 80)  # 其他控件使用默认阴影

    # 创建并应用阴影效果
    shadow_effect = QtWidgets.QGraphicsDropShadowEffect(widget)
    shadow_effect.setBlurRadius(blur_radius)
    shadow_effect.setXOffset(x_offset)
    shadow_effect.setYOffset(y_offset)
    shadow_effect.setColor(color)
    widget.setGraphicsEffect(shadow_effect)

class MySetDialog(QtWidgets.QDialog, settings_dialog.Ui_Dialog):
    # 设置自定义配置文件路径的信号
    signal_set_config_file = QtCore.pyqtSignal(str)
    def __init__(self):
        super(MySetDialog, self).__init__()
        self.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 为frame安装事件过滤器
        self.setupFrameDragging()

        for i in [self.frame, self.set_theme1_btn, self.set_theme2_btn,
                  self.set_theme3_btn, self.groupBox, self.save_conf_btn,
                  self.default_conf_btn, self.path_lineEdit]:
            add_shadow_to_widget(
                i,
                blur_radius=30,
                color=QtGui.QColor(0, 0, 0, 100)
            )

    def close_dialog(self):
        """关闭对话框"""
        self.close()

    def min_dialog(self):
        """最小化对话框"""
        self.showMinimized()

    def set_theme_one(self):
        """设置主题为1"""
        print("设置主题为1")
        # self.setStyleSheet("")

    def set_theme_two(self):
        """设置主题为2"""
        print("设置主题为2")
        # self.setStyleSheet("")

    def set_theme_three(self):
        """设置主题为3"""
        print("设置主题为3")
        # self.setStyleSheet("")

    def file_path(self):
        """配置文件操作"""
        print("打开配置文件")
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "选择配置文件", "", "配置文件 (*.json *.ini *.conf)"
        )
        print(type(file_path), file_path)
        self.path_lineEdit.setText(file_path)

    def save_conf(self):
        """保存配置文件"""
        print("保存配置文件")
        file_path = self.path_lineEdit.text()
        if file_path:
            self.signal_set_config_file.emit(file_path)
        else:
            QtWidgets.QMessageBox.warning(self, "错误", "请选择有效的配置文件")

    def default_conf(self):
        """恢复默认配置"""
        print("恢复默认配置")
        self.signal_set_config_file.emit("null")

    def setupFrameDragging(self):
        """为frame控件设置拖动功能"""
        if hasattr(self, 'frame'):
            self.frame.installEventFilter(self)
            self.frame.setCursor(QtCore.Qt.PointingHandCursor)  # 可选：显示手型光标

    def eventFilter(self, obj, event):
        """事件过滤器处理frame的鼠标事件"""
        if obj == self.frame:
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
                    self.isDragging = True
                    return True

            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.LeftButton and self.isDragging:
                    self.move(event.globalPos() - self.dragPosition)
                    return True

            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    self.isDragging = False
                    return True

        return super().eventFilter(obj, event)


class MyAboutDialog(QtWidgets.QDialog, about.Ui_Dialog):
    def __init__(self):
        super(MyAboutDialog, self).__init__()
        self.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 为frame安装事件过滤器
        self.setupFrameDragging()

        if hasattr(self, 'frame'):
            add_shadow_to_widget(
                self.frame,
                blur_radius=30,
                color=QtGui.QColor(0, 0, 0, 100)
            )

    def close_dialog(self):
        """关闭对话框"""
        self.close()

    def min_dialog(self):
        """最小化对话框"""
        self.showMinimized()

    def open_github(self):
        """处理链接点击"""
        print(f"[示例] 尝试打开链接: https://github.com/LeurDeLis/MqttServerUI")
        try:
            webbrowser.open("https://github.com/LeurDeLis/MqttServerUI")
        except Exception as e:
            error_message = f"无法打开链接 https://github.com/LeurDeLis/MqttServerUI:\n{str(e)}"
            print(error_message)
            QtWidgets.QMessageBox.warning(self, "打开链接失败", error_message)

    def open_csdn(self):
        """处理链接点击"""
        print(f"[示例] 尝试打开链接: https://blog.csdn.net/weixin_46973942")
        try:
            webbrowser.open("https://blog.csdn.net/weixin_46973942")
        except Exception as e:
            error_message = f"无法打开链接 https://blog.csdn.net/weixin_46973942:\n{str(e)}"
            print(error_message)
            QtWidgets.QMessageBox.warning(self, "打开链接失败", error_message)

    def setupFrameDragging(self):
        """为frame控件设置拖动功能"""
        if hasattr(self, 'frame'):
            self.frame.installEventFilter(self)
            self.frame.setCursor(QtCore.Qt.PointingHandCursor)  # 可选：显示手型光标

    def eventFilter(self, obj, event):
        """事件过滤器处理frame的鼠标事件"""
        if obj == self.frame:
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
                    self.isDragging = True
                    return True

            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.LeftButton and self.isDragging:
                    self.move(event.globalPos() - self.dragPosition)
                    return True

            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    self.isDragging = False
                    return True

        return super().eventFilter(obj, event)


def is_internet_connected(timeout=5):
    """
    检测网络是否可以上网

    Args:
        timeout (int): 超时时间（秒），默认5秒

    Returns:
        bool: True表示可以上网，False表示无法上网
    """

    # 方法1: 使用requests访问百度
    def check_http():
        try:
            response = requests.get('https://www.baidu.com', timeout=timeout)
            return response.status_code == 200
        except:
            return False

    # 方法2: 使用socket连接DNS服务器
    def check_dns():
        try:
            socket.create_connection(('8.8.8.8', 53), timeout=timeout)
            return True
        except:
            return False

    # 方法3: 使用ping检测
    def check_ping():
        try:
            if sys.platform.startswith('win'):
                # Windows
                result = subprocess.run(['ping', '-n', '1', 'www.baidu.com'],
                                        capture_output=True, timeout=timeout)
            else:
                # Linux/Mac
                result = subprocess.run(['ping', '-c', '1', 'www.baidu.com'],
                                        capture_output=True, timeout=timeout)
            return result.returncode == 0
        except:
            return False

    # 尝试三种方法，任一成功即认为可以上网
    return check_http() or check_dns() or check_ping()
