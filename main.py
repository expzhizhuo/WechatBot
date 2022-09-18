from servercli.server import *
from httpcli.output import *
from httpcli.everyday_news import *
from servercli.server import *
import configparser
import schedule
from multiprocessing import Process


# 读取本地的配置文件
current_path = os.path.dirname(__file__)
config_path = os.path.join(current_path, "./config/config.ini")
config = configparser.ConfigParser()  # 类实例化
config.read(config_path, encoding="utf-8")
admin_id = config.get("server", "admin_id")
room_id = config.get("server", "room_id")
set_time_am = config.get("server", "set_time_am")
set_time_pm = config.get("server", "set_time_pm")


def morning_paper_push():
    output("每日早报推送")
    msg = "每日早报推送测试,没有写呢，过几天完成"
    auto_send_message_room(msg, room_id)


def evening_paper_push():
    output("每日晚间安全资讯推送")
    msg = get_safety_news()
    auto_send_message_room(msg, room_id)


# 创建定时任务
def auto_push():
    output("每日定时任务 Strat")
    # 早报自动推送
    schedule.every().day.at(set_time_am).do(morning_paper_push)
    # 晚报自动推送
    schedule.every().day.at(set_time_pm).do(evening_paper_push)
    while True:
        schedule.run_pending()


def main():
    output("WechatBot Test")
    get_personal_info()
    processed = Process(target=evening_paper_push, name="Auto push")
    # 进程守护，主进程结束子进程也要结束
    processed.daemon = True
    processed.start()
    bot()


if __name__ == "__main__":
    main()
