# -*- coding: utf-8 -*-
# @Time    : 2025/7/24 19:26
# @Author  : LeurDeLis
# @File    : mqtt_client.py
# @Software: PyCharm

import paho.mqtt.client as mqtt

# 连接回调
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("连接成功")
        client.subscribe("recv")  # 连接成功后订阅 recv 主题
    else:
        print("连接失败，返回码：", rc)

# 消息接收回调
def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"[接收] Topic: {msg.topic}, Message: {payload}")

    # 响应性发布到 send 主题
    response = f"已收到消息：+++++{payload}"
    client.publish("send", response)
    print(f"[发送] Topic: send, Message: {response}")

# 初始化客户端
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# 连接到本地 broker
client.connect("127.0.0.1", 21883)

# 启动后台线程处理网络事件
client.loop_start()

# 保持主线程运行
try:
    while True:
        pass  # 或者使用 time.sleep(1)
except KeyboardInterrupt:
    print("断开连接")
    client.loop_stop()
    client.disconnect()

