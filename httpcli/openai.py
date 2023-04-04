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


def remove_punctuation(text):
    import string
    for i in range(len(text)):
        if text[i] not in string.punctuation:
            return text[i:]
    return ""


def OpenaiServer(msg=None, preset_map={}, old_chat={}, senderid=None,user_chat=[]):
    arr = []
    preset =""
    try:
        try:
            if old_chat[senderid]:
                arr = old_chat[senderid]
        except Exception as e:
            pass
        try:
            if preset_map[senderid]:
                preset = preset_map[senderid]
        except Exception as e:
            pass
        if msg is None:
            output(f'ERROR：msg is None')
            msg = ""
        else:
            system = [
                {"role": "system", "content": preset}
            ]
            prompt = {"role": "user", "content": msg}
            arr.append(prompt)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=system + arr,
                max_tokens=500,
                top_p=1,
            )
            # msg = "来自openai回复结果：\n"
            msg = remove_punctuation(response.choices[0].message.content.strip().replace('\n\n', '\n'))
            arr.append({"role": "assistant", "content": msg})
            print(arr)
            if senderid in user_chat:
                old_chat[senderid] = arr
    except Exception as e:
        output(f"ERROR：{e}")
        msg = "AI请求超时"
    return msg
