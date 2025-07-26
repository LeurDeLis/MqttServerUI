# -*- coding: utf-8 -*-
# @Time    : 2025/7/24 23:57
# @Author  : LeurDeLis
# @File    : main.py
# @Software: PyCharm
import json
import os
import sys
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
from PyQt5 import QtCore, QtWidgets, QtGui
from UI.MqttServer import Ui_MainWindow
from other_function import MySetDialog, MyAboutDialog, add_shadow_to_widget, is_internet_connected
from MQTT.mqtt_server import MQTTBrokerManager


class MyMqtt(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MyMqtt, self).__init__()
        self.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.settings_dialog = MySetDialog()
        self.msg_box = MyAboutDialog()

        # 配置文件内容
        self.config_content = None
        # MQTT 服务端
        self.broker = MQTTBrokerManager(
            mosquitto_path="./mosquitto/mosquitto.exe",
            config_file=None,
        )
        self.mqtt_server_conf_set()

        self.add_shadow()

        # 为frame安装事件过滤器
        self.setupFrameDragging()

        if is_internet_connected():
            self.wifi_lab.setStyleSheet("QLabel{\n"
                                        "    border:none;\n"
                                        "    background-color: rgba(255, 255, 255, 0);\n"
                                        "    image: url(:/img/icons/with_network.png);\n"
                                        "}")

        self.settings_dialog.signal_set_config_file.connect(self.set_config_file)

    def mqtt_server_conf_set(self):
        # 读取文件内容
        with open('./MQTT/app_conf', 'r') as file:
            self.config_content = json.loads(file.read())
        # 使用get方法安全获取配置值
        custom_config = self.config_content.get("custom")
        default_config = self.config_content.get("default")

        # 检查配置文件路径并加载
        if custom_config and os.path.exists(custom_config):
            self.broker.config_file = custom_config
            self.logs_text.append("已加载自定义配置文件！")
        elif default_config and os.path.exists(default_config):
            self.broker.config_file = default_config
            self.logs_text.append("已加载默认配置文件！")
        else:
            self.logs_text.append("错误：未找到有效的配置文件！")

    def add_shadow(self):
        for i in [self.ip_text, self.port_text, self.logs_text, self.frame, self.open_server_btn, self.state_bar, self.close_server_btn]:
            add_shadow_to_widget(
                i,
                blur_radius=20,
                color=QtGui.QColor(0, 0, 0, 100)
            )

    def setupFrameDragging(self):
        """为frame控件设置拖动功能"""
        if hasattr(self, 'state_bar'):
            self.state_bar.installEventFilter(self)
            self.state_bar.setCursor(QtCore.Qt.PointingHandCursor)  # 可选：显示手型光标

    def eventFilter(self, obj, event):
        """事件过滤器处理frame的鼠标事件"""
        if obj == self.state_bar:
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

    def close_app(self):
        """关闭应用程序"""
        if self.broker.is_running():
            self.broker.stop()
        self.close()

    def min_app(self):
        """最小化应用程序"""
        self.showMinimized()

    def connect_btn(self):
        """连接MQTT服务器"""
        print("连接MQTT服务器")
        ip = self.ip_text.text()
        port = self.port_text.text()
        if ip and port:
            self.broker.host = ip
            self.broker.port = int(port)
        custom_config = self.config_content.get("custom")
        # 检查配置文件路径并加载
        if custom_config and os.path.exists(custom_config):
            self.broker.config_file = custom_config
        self.logs_text.append("正在启动服务器...")
        self.broker.start()
        if self.broker.is_running():
            self.logs_text.append("服务器已启动")
            self.connect_lab.setStyleSheet("QLabel{\n"
                                           "    border:none;\n"
                                           "    background-color: rgba(255, 255, 255, 0);\n"
                                           "    image: url(:/img/icons/connect01.png);\n"
                                           "}")
        else:
            self.logs_text.append("服务器启动失败")
        self.logs_text.moveCursor(QtGui.QTextCursor.End)

    def disconnect_btn(self):
        """断开MQTT服务器连接"""
        print("断开MQTT服务器连接")
        # 在这里添加断开连接的逻辑
        self.logs_text.append("正在停止服务器...")
        self.broker.stop()
        if not self.broker.is_running():
            self.logs_text.append("服务器已停止")
            self.connect_lab.setStyleSheet("QLabel{\n"
                                           "    border:none;\n"
                                           "    background-color: rgba(255, 255, 255, 0);\n"
                                           "    image: url(:/img/icons/disconnect01.png);\n"
                                           "}")
        else:
            self.logs_text.append("服务器停止失败")
        self.logs_text.moveCursor(QtGui.QTextCursor.End)

    def set_config_file(self, path: str):
        print("设置配置文件", path)
        if path == "null":
            self.config_content["custom"] = None
        else:
            self.config_content["custom"] = path
        # 重新写入文件
        with open('./MQTT/app_conf', 'w') as file:
            json.dump(self.config_content, file, indent=4, ensure_ascii=False)

    def setting(self):
        """设置操作"""
        print("打开设置")
        self.settings_dialog.exec_()

    def about_app(self):
        """关于应用程序"""
        print("显示关于信息")
        self.msg_box.exec_()

if __name__ == "__main__":
    # 解决屏幕分辨率不适配的问题
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    window = MyMqtt()
    window.show()
    sys.exit(app.exec_())
