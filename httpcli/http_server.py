import os
import re
import requests
from httpcli.output import *
import configparser
import random

# 读取本地的配置文件
current_path = os.path.dirname(__file__)
config_path = os.path.join(current_path, "../config/config.ini")
config = configparser.ConfigParser()  # 类实例化
config.read(config_path, encoding="utf-8")
History_url = config.get("apiService", "history_url")
md5_url = config.get("apiService", "md5_url")
dog_url = config.get("apiService", "dog_url")
fart_url = config.get("apiService", "fart_url")
girl_videos_url = config.get("apiService", "girl_videos_url")
weather_url = config.get("apiService", "weather_url")
smile_url = config.get("apiService", "smile_url")
zodiac_url = config.get("apiService", "zodiac_url")
allow_token = config.get("apiService", "allow_token")


# 获取历史的今天事件
def get_history_event():
    output("Get History Today event")
    try:
        resp = requests.get(
            History_url,
            timeout=5,
            verify=False,
        )
        if resp.status_code == 200:
            path = os.path.abspath("./img")
            img_name = int(time.time() * 1000)
            # 以时间轴的形式给图片命名
            with open(f"{path}\\{img_name}.jpg", "wb+") as f:
                # 写入文件夹
                f.write(resp.content)  # 如果这句话一直报错，很有可能是你的网址url不对
                # 关闭文件夹
                f.close()
            video_path = os.path.abspath(f"{path}\\{img_name}.jpg")
            msg = video_path.replace("\\", "\\\\")
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
    try:
        city_list = re.findall("查询(.*?)天气", self)
        if len(city_list) > 0:
            city = city_list[0]
        else:
            city = ""
        resp = requests.get(str(weather_url) + str(city), timeout=5, verify=False)
        if resp.status_code == 200 and resp.json()["status"] == 1000:
            air_speed = resp.json()["data"]["forecast"][0]["fengli"]
            air_speed_msg = air_speed.replace("<![CDATA[", "").replace("]]>", "")
            weather_msg = f'今日{city}的天气\n日期：{resp.json()["data"]["forecast"][0]["date"]}\n最高气温：{resp.json()["data"]["forecast"][0]["high"]}\n最低气温：{resp.json()["data"]["forecast"][0]["low"]}\n风向：{resp.json()["data"]["forecast"][0]["fengxiang"]}\n风速：{air_speed_msg}\n天气：{resp.json()["data"]["forecast"][0]["type"]}\n\nBy zhizhuo\n{time.strftime("%Y-%m-%d %X")}'
            msg = weather_msg
        else:
            msg = f"天气查询接口出错，请稍后重试,接口状态{resp.status_code}"
    except Exception as e:
        output("ERROR: {0}".format(e))
        msg = "天气查询接口出错，ERROR:{}".format(e)
    return msg


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


def get_girl_videos():
    output("Get Girl Videos")
    try:
        resp = requests.get(girl_videos_url, timeout=5, verify=False)
        if resp.status_code == 200:
            videos_url = re.findall(
                '<video src="(.*?)" muted controls preload="auto"', resp.text, re.S
            )
            if len(videos_url) > 0:
                url = "http:" + str(videos_url[0])
                resp1 = requests.get(url, timeout=5, verify=False)
                path = os.path.abspath("./video")
                videos_name = int(time.time() * 1000)
                # 以时间轴的形式给图片命名
                with open(f"{path}\\{videos_name}.mp4", "wb+") as f:
                    # 写入文件夹
                    f.write(resp1.content)  # 如果这句话一直报错，很有可能是你的网址url不对
                    # 关闭文件夹
                    f.close()
                video_path = os.path.abspath(f"{path}\\{videos_name}.mp4")
                msg = video_path.replace("\\", "\\\\")
            else:
                msg = "ERROR：未识别到URL连接"
        else:
            msg = "站点状态异常，访问请求：{}".format(resp.status_code)
    except Exception as e:
        output("ERROR：{}".format(e))
        msg = "视频接口调用出错，错误信息：{}".format(e)
    return msg


# 获取搞笑段子
def get_Funny_jokes():
    output("GET Funny jokes")
    try:
        content_num = random.randint(0, 9)
        resp = requests.get(
            smile_url + str(random.randint(1, 8715)), timeout=5, verify=False
        )
        if resp.status_code == 200 and resp.json()["code"] == 1:
            msg = (
                resp.json()["data"]["list"][content_num]["content"]
                + "\n\n更新时间："
                + resp.json()["data"]["list"][content_num]["updateTime"]
            )
        else:
            msg = f"ERROR：接口请求请求异常，接口状态：{resp.status_code},错误信息：{resp.json()['msg']}"
            output(msg)
    except Exception as e:
        output(f"ERROR：{e}")
        msg = f"搞笑段子接口调用出错，ERROR：{e}"
    return msg


# 获取今日黄历
def get_today_zodiac():
    output("GET today zodiac")
    try:
        resp = requests.get(
            zodiac_url + str(time.strftime("%Y%m%d")) + str(allow_token),
            timeout=5,
            verify=False,
        )
        if resp.status_code == 200 and resp.json()["code"] == 1:
            msg = f'当前日期：{resp.json()["data"]["date"]}\n本周第{resp.json()["data"]["weekDay"]}天\n属相：{resp.json()["data"]["chineseZodiac"]}\n节气：{resp.json()["data"]["solarTerms"]}\n农历：{resp.json()["data"]["lunarCalendar"]}\n宜：{resp.json()["data"]["suit"]}\n忌：{resp.json()["data"]["avoid"]}\n今年第{resp.json()["data"]["dayOfYear"]}天\n今年第{resp.json()["data"]["weekOfYear"]}周\n星座：{resp.json()["data"]["constellation"]}\n本月第{resp.json()["data"]["indexWorkDayOfMonth"]}个工作日'
        else:
            msg = f"ERROR：接口请求请求异常，接口状态：{resp.status_code},错误信息：{resp.json()['msg']}"
            output(msg)
    except Exception as e:
        output(f"ERROR：{e}")
        msg = f"搞笑段子接口调用出错，ERROR：{e}"
    return msg
