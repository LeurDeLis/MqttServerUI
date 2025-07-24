# -*- coding: utf-8 -*-
# @Time    : 2025/7/24 18:01
# @Author  : LeurDeLis
# @File    : mqtt_server.py
# @Software: PyCharm

# -*- coding: utf-8 -*-
# @Time    : 2025/7/24 18:01
# @Author  : LeurDeLis
# @File    : mqtt_server.py
# @Software: PyCharm

import subprocess
import threading
import os
import tempfile
import time

# Mosquitto 可执行文件路径（Windows 示例）
MOSQUITTO_PATH = r"D:\APP\mosquitto\mosquitto.exe"
# Broker 监听地址和端口
MQTT_HOST = "127.0.0.1"
MQTT_PORT = 21883

def create_temp_config():
    """
    使用当前目录下已有的配置文件。
    文件内容应包含监听设置，例如：
        listener 21883 127.0.0.1
        allow_anonymous true
        log_dest stdout
    """
    config_path = os.path.abspath("./mosquitto_local.conf")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"未找到配置文件: {config_path}")
    return config_path


def log_reader(proc):
    """
    后台线程实时读取 Mosquitto 日志。
    """
    for line in proc.stdout:
        print("[Broker]", line.strip())

def start_mosquitto():
    """
    启动 Mosquitto Broker 并返回进程句柄和配置文件路径。
    """
    config_path = create_temp_config()
    proc = subprocess.Popen(
        [MOSQUITTO_PATH, "-c", config_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    threading.Thread(target=log_reader, args=(proc,), daemon=True).start()
    print(f"Mosquitto 启动成功，监听：{MQTT_HOST}:{MQTT_PORT}")
    return proc, config_path

def stop_mosquitto(proc, config_path):
    """
    停止 Mosquitto 进程。
    """
    print("正在关闭 Mosquitto...")
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
    print("Mosquitto 已关闭")


if __name__ == "__main__":
    proc, config_file = start_mosquitto()
    try:
        input("按回车键停止 MQTT Broker ...\n")
    finally:
        stop_mosquitto(proc, config_file)


