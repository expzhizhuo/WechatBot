import configparser
import os
import re
import warnings

import feedparser
import requests

from httpcli.output import *

warnings.filterwarnings('ignore')

# 读取本地的配置文件
current_path = os.path.dirname(__file__)
config_path = os.path.join(current_path, "../config/config.ini")
config = configparser.ConfigParser()  # 类实例化
config.read(config_path, encoding="utf-8")
xz_url = config.get("apiService", "xz_url")
freebuf_url = config.get("apiService", "freebuf_url")
qax_url = config.get("apiService", "qax_url")
anquanke_url = config.get("apiService", "anquanke_url")
y4tacker_url = config.get("apiService", "y4tacker_url")

news_list = ""
# 全局header头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    # 'Connection':'keep-alive',#默认时链接一次，多次爬取之后不能产生新的链接就会产生报错Max retries exceeded with url
    "Upgrade-Insecure-Requests": "1",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Connection": "close",  # 解决Max retries exceeded with url报错
}


# 先知社区
def get_xz_news():
    global news_list
    str_list = ""
    news_list += "#先知社区"
    try:
        rs1 = feedparser.parse(xz_url)
        length = len(rs1.entries)
        for buf in range(length):
            try:
                if str(time.strftime("%Y-%m-%d")) in str(rs1.entries[buf]["published"]):
                    url_f = rs1.entries[buf]["link"]
                    title_f = rs1.entries[buf]["title_detail"]["value"]
                    link4 = "\n" + title_f + "\n" + url_f + "\n"
                    str_list += link4
                else:
                    pass
            except Exception as e:
                output("ERROR：{}".format(e))
                break
        if len(str_list) > 0:
            news_list += str_list
        else:
            link6 = "\n今日暂无文章"
            news_list += link6
    except Exception as e:
        link6 = "\n今日暂无文章"
        news_list += link6
        output("ERROR：先知社区 {}".format(e))
        return "xz is no ok"


# freebuf 源
def get_freebuf_news():
    # global news_list
    str_list = ""
    str_list += "#FreeBuf早报\n"
    try:
        rs1 = feedparser.parse(freebuf_url)
        length = len(rs1.entries)
        for buf in range(length):
            try:
                if (
                        f'tm_year={int(time.strftime("%Y"))}'
                        in str(rs1.entries[buf]["published_parsed"])
                        and f'tm_mon={int(time.strftime("%m"))}'
                        in str(rs1.entries[buf]["published_parsed"])
                        and f'tm_mday={str(int(time.strftime("%d")) - 1)}'
                        in str(rs1.entries[buf]["published_parsed"])
                ):
                    url_f = rs1.entries[buf]["link"]
                    title_f = (
                        rs1.entries[buf]["title_detail"]["value"]
                        .replace("FreeBuf早报 |", "")
                        .replace(" ", "")
                    )
                    link4 = "\n" + title_f + "\n" + url_f + "\n"
                    str_list += link4
                else:
                    pass
            except Exception as e:
                output("ERROR：{}".format(e))
                break
        if len(str_list) == 0:
            link6 = "\n今日暂无文章"
            str_list += link6
        else:
            pass
    except Exception as e:
        link6 = "\n今日暂无文章"
        str_list += link6
        output("ERROR：freebuf {}".format(e))
    str_list += "\nCreated by zhizhuo \n{}".format(time.strftime("%Y-%m-%d %X"))
    return str_list


# 奇安信攻防社区
def get_qax_news():
    global news_list
    str_list = ""
    news_list += "\n#奇安信攻防社区"
    try:
        rs1 = feedparser.parse(qax_url)
        length = len(rs1.entries)
        for buf in range(length):
            try:
                if str(time.strftime("%Y-%m-%d")) in str(rs1.entries[buf]["published"]):
                    url_f = rs1.entries[buf]["link"]
                    title_f = rs1.entries[buf]["title_detail"]["value"]
                    link4 = "\n" + title_f + "\n" + url_f + "\n"
                    str_list += link4
                else:
                    pass
            except Exception as e:
                output("ERROR：{}".format(e))
                break
        if len(str_list) > 0:
            news_list += str_list
        else:
            link6 = "\n今日暂无文章"
            news_list += link6
    except Exception as e:
        link6 = "\n今日暂无文章"
        news_list += link6
        output("ERROR：奇安信攻防社区 {}".format(e))
        return "qax is no ok"


# 安全客
def get_anquanke_news():
    global news_list
    str_list = ""
    news_list += "\n#安全客"
    try:
        rs1 = requests.get(anquanke_url, timeout=5, verify=False)
        rs1.encoding = "utf-8"
        resp_text = (
            rs1.text.replace("\xa9", "")
            .replace("\n", "")
            .replace("&gt;", "")
            .replace(" ", "")
            .replace("                        ", "")
            .replace("                               ", "")
        )
        newlist = re.findall(
            '<divclass="info-content"><divclass="title"><atarget="_blank"rel="noopenernoreferrer"href="(.*?)">(.*?)</a></div><divclass="tagshide-in-mobile-device">',
            resp_text,
            re.S,
        )
        timelist = re.findall(
            '<istyle="margin-right:4px;"class="fafa-clock-o"></i>(.*?)</span></span>',
            resp_text,
            re.S,
        )
        for a in range(len(timelist)):
            try:
                if time.strftime("%Y-%m-%d") in timelist[a]:
                    link1 = str(newlist[a][1])
                    link2 = "https://www.anquanke.com" + str(newlist[a][0])
                    link3 = "\n" + str(link1) + "\n" + str(link2) + "\n"
                    str_list += link3
                else:
                    pass
            except Exception as e:
                output("ERROR：{}".format(e))
                break
        if len(str_list) > 0:
            news_list += str_list
        else:
            link6 = "\n今日暂无文章"
            news_list += link6
    except Exception as e:
        link6 = "\n今日暂无文章"
        news_list += link6
        output("ERROR：安全客 {}".format(e))
        return "安全客 is no ok"


# Y4tacker Blog
def get_y4tacker_news():
    global news_list
    str_list = ""
    news_list += "\n#Y4tacker Blog"
    # today = datetime.date.today()
    # yesterday = today - datetime.timedelta(days=1)
    # formatted_yesterday = yesterday.strftime("%Y-%m-%d")
    try:
        rs1 = feedparser.parse(y4tacker_url)
        length = len(rs1.entries)
        for buf in range(length):
            try:
                # print(time.strftime("%Y-%m-%d"))
                # print(formatted_yesterday)
                # print(time.strftime("%Y-%m-%d %H:%M:%S", rs1.entries[buf]["published_parsed"]))
                if str(time.strftime("%Y-%m-%d")) in str(
                        time.strftime("%Y-%m-%d %H:%M:%S", rs1.entries[buf]["updated_parsed"])):
                    url_f = rs1.entries[buf]['links'][0]['href']
                    title_f = rs1.entries[buf]["title"]
                    link4 = "\n" + title_f + "\n" + url_f + "\n"
                    str_list += link4
                else:
                    pass
            except Exception as e:
                output("ERROR：{}".format(e))
                break
        if len(str_list) > 0:
            news_list += str_list
        else:
            link6 = "\n今日暂无文章"
            news_list += link6
    except Exception as e:
        link6 = "\n今日暂无文章"
        news_list += link6
        output("ERROR：Y4tacker Blog {}".format(e))
        return "Y4tacker Blog is no ok"


def get_safety_news():
    output("GET safety News")
    global news_list
    news_list = ""
    get_xz_news()
    # get_freebuf_news()
    # get_qax_news()
    get_anquanke_news()
    get_y4tacker_news()
    output("获取成功")
    news_list += "\nCreated by zhizhuo \n{}".format(time.strftime("%Y-%m-%d %X"))
    return news_list


if __name__ == "__main__":
    news = get_safety_news()
    print(news)
