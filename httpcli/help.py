"""
@Project ：WechatBot 
@File    ：openai.py
@IDE     ：PyCharm 
@Author  ：Xciny
@Date    ：2023/2/1 16:03 
"""
import configparser
import os

import openai

from httpcli.output import *

current_path = os.path.dirname(__file__)
config_path = os.path.join(current_path, "../config/config.ini")
config = configparser.ConfigParser()  # 类实例化
config.read(config_path, encoding="utf-8")
openai_key = config.get("apiService", "openai_key")
openai.api_key = openai_key


def gethelp():
    try:
        msg = "智障机器人使用说明：\n"
        msg += "智能机器人问答：@chatgpt {问题}\n"
        msg += "查看机器人状态（管理员权限）：test\n"
        msg += "获取一篇舔狗日记：舔狗日记\n"
        msg += "获取今日新闻（管理员权限）：今日新闻\n"
        msg += "查询城市天气：查询{城市名}天气\n"
        msg += "查询星座运势：查询{星座名}运势\n"
        msg += "获取当天摸鱼日历：摸鱼日历\n"
        msg += "获取安全资讯：安全资讯\n"
        msg += "查询ip归属地：查询ip {ip地址}\n"
        msg += "网络资产端口探测：端口扫描{域名/ip}\n"
        msg += "设置人格对话：设置人格 {AI助手} {助手乐于助人、富有创意、聪明而且非常友好。}\n"
        msg += "重置人格：重置人格\n"
        msg += "开启对话聊天：对话模式\n"
        msg += "结束对话聊天：结束对话\n"
        msg += "设置闹钟提醒（管理员权限）：提醒{微信名}{时间}{事件}\n"
        msg += "清空闹钟所有闹钟（管理员权限）：清空闹钟"
    except Exception as e:
        output(f"ERROR：{e.message}")
        msg = e
    return msg
