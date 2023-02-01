"""
@Project ：WechatBot 
@File    ：openai.py
@IDE     ：PyCharm 
@Author  ：zhizhuo
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


def OpenaiServer(msg=None):
    try:
        if msg is None:
            output(f'ERROR：msg is None')
        else:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=msg,
                temperature=0.6,
            )
            print(response.choices[0].text)
            msg = response.choices[0].text
            return msg
    except Exception as e:
        output(f"ERROR：{e.message}")
        msg = e.message
        return msg
