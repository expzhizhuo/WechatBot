import os
import requests
from httpcli.output import *
import configparser

# 读取本地的配置文件
current_path = os.path.dirname(__file__)
config_path = os.path.join(current_path, "../config/config.ini")
config = configparser.ConfigParser()  # 类实例化
config.read(config_path, encoding="utf-8")
History_url = config.get("apiService", "history_url")
md5_url = config.get("apiService", "md5_url")
dog_url = config.get("apiService", "dog_url")
fart_url = config.get("apiService", "fart_url")


# 获取历史的今天事件
def get_history_event():
    output("Get History Today event")
    try:
        resp = requests.get(
            History_url,
            timeout=5,
            verify=False,
        )
        print(resp.text)
        if resp.status_code == 200 and resp.json()["code"] == 200:
            msg = resp.text
        else:
            msg = "历史上的今天接口调用超时"
    except Exception as e:
        msg = "历史上的今天接口调用出错，错误信息：{}".format(e)
    return msg


# 获取舔狗日记
def get_lick_the_dog_diary():
    output("Get Lick the dog diary")
    try:
        resp = requests.get(
            dog_url,
            timeout=5,
            verify=False,
        )
        if resp.status_code == 200 and resp.json()["code"] == 200:
            msg = resp.json()["newslist"][0]["content"]
        else:
            msg = "舔狗日记接口调用超时"
    except Exception as e:
        msg = "舔狗日记接口调用出错，错误信息：{}".format(e)
    return msg


# 获取今天的天气
def get_today_weather(self):
    output("Get Today Weather")
    if self:
        city = self
    else:
        city = ""


# 获取彩虹屁
def get_rainbow_fart():
    output("Get Rainbow fart")
    try:
        resp = requests.get(
            fart_url,
            timeout=4,
            verify=False,
        )
        if resp.status_code == 200 and resp.json()["code"] == 200:
            msg = resp.json()["newslist"][-1]["content"]
        else:
            msg = "彩虹屁接口调用超时"
    except Exception as e:
        msg = "彩虹屁接口调用出错，错误信息：{}".format(e)
    return msg


# 获取鸡汤
def get_chicken_soup():
    output("Get Chicken soup")
    try:
        resp = requests.get(
            "https://api.oick.cn/dutang/api.php", timeout=5, verify=False
        )
        if resp.status_code == 200:
            msg = resp.text.replace('"', "")
        else:
            msg = "鸡汤接口请求超时"
    except Exception as e:
        msg = "鸡汤接口调用出错，错误信息：{}".format(e)
    return msg


# md5解密接口
def get_md5(self):
    output("Get MD5 Clear")
    try:
        md5_list = self.split(":")
        md5_list = self.split("：")
        md5_list = self.split(" ")
        if len(md5_list) > 1 and len(md5_list[1]) > 5:
            pmd5_url = str(md5_url) + str(md5_list[1])
            resp = requests.get(pmd5_url, timeout=5, verify=False)
            if resp.status_code == 200 and len(resp.json()["result"]) > 0:
                msg = "\n密文：{}\nMD5解密结果为：{}".format(
                    str(md5_list[1]),
                    resp.json()["result"]["{}".format(str(md5_list[1]))],
                )
            elif resp.status_code != 200:
                msg = "MD5解密接口调用超时"
            else:
                msg = "MD5解密失败"
        else:
            msg = None
            pass
    except Exception as e:
        msg = "PMD5解密接口调用出错，错误信息：{}".format(e)
    return msg
