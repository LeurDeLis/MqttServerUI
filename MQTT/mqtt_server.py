# -*- coding: utf-8 -*-
# @Time    : 2025/7/24 18:01
# @Author  : LeurDeLis
# @File    : mqtt_server.py
# @Software: PyCharm

import subprocess
import threading
import os
import tempfile


class MQTTBrokerManager:
    """
    Mosquitto MQTT Broker 管理类
    """

    def __init__(self, mosquitto_path: str, config_file: str = None, host: str = None, port: int = None):
        """
        初始化 MQTT Broker 管理器。
        :param mosquitto_path: Mosquitto 可执行文件路径
        :param config_file: 配置文件路径（如果不提供则使用 host + port 动态生成）
        :param host: 监听地址（与 port 一起使用时生效）
        :param port: 监听端口（与 host 一起使用时生效）
        """
        self.mosquitto_path = mosquitto_path
        self.config_file = os.path.abspath(config_file) if config_file else None
        self.host = host
        self.port = port
        self.proc = None
        self._log_thread = None
        self._temp_conf_path = None  # 存储动态生成的配置文件路径

    def _log_reader(self, proc):
        """
        后台线程读取 Mosquitto 日志
        """
        for line in proc.stdout:
            print("[Broker]", line.strip())

    def _generate_temp_config(self):
        """
        动态生成监听配置文件
        """
        config_content = f"""
listener {self.port} {self.host}
allow_anonymous true
log_dest stdout
"""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".conf", mode="w", encoding="utf-8")
        temp_file.write(config_content)
        temp_file.close()
        self._temp_conf_path = temp_file.name
        return self._temp_conf_path

    def start(self):
        """
        启动 MQTT Broker 服务
        """
        # 判断使用配置文件还是动态 IP + 端口
        if self.host and self.port:
            config_path = self._generate_temp_config()
            print(f"使用动态配置文件启动: {config_path}")
        elif self.config_file and os.path.exists(self.config_file):
            config_path = self.config_file
            print(f"使用默认配置文件启动: {config_path}")
        else:
            raise ValueError("未提供有效的配置文件，且缺少 host 和 port 参数。")

        self.proc = subprocess.Popen(
            [self.mosquitto_path, "-c", config_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        self._log_thread = threading.Thread(target=self._log_reader, args=(self.proc,), daemon=True)
        self._log_thread.start()
        print(f"Mosquitto 启动成功，监听：{self.host or 'config file 中指定的地址'}:{self.port or 'config file 中指定的端口'}")

    def stop(self):
        """
        停止 MQTT Broker 服务
        """
        if self.proc is not None:
            print("正在关闭 Mosquitto...")
            self.proc.terminate()
            try:
                self.proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.proc.kill()
            print("Mosquitto 已关闭")
            self.proc = None

        if self._temp_conf_path and os.path.exists(self._temp_conf_path):
            os.remove(self._temp_conf_path)
            self._temp_conf_path = None

    def is_running(self):
        """
        检查 Broker 是否正在运行
        """
        return self.proc is not None and self.proc.poll() is None

# # 使用 IP+端口 启动
# broker = MQTTBrokerManager(
#     mosquitto_path=r"D:\APP\mosquitto\mosquitto.exe",
#     host="127.0.0.1",
#     port=21883
# )
# broker.start()
#
# # 使用已有配置文件启动
# broker = MQTTBrokerManager(
#     mosquitto_path=r"D:\APP\mosquitto\mosquitto.exe",
#     config_file="./mosquitto_local.conf"
# )
# broker.start()
