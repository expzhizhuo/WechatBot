import colorama
import schedule
from pyfiglet import Figlet

from servercli.server import *

# 解决cmd样式问题
colorama.init(autoreset=True)

# 读取本地的配置文件
current_path = os.path.dirname(__file__)
config_path = os.path.join(current_path, "./config/config.ini")
config = configparser.ConfigParser()  # 类实例化
config.read(config_path, encoding="utf-8")
admin_id = config.get("server", "admin_id")
room_id = config.get("server", "room_id")
set_time_am = config.get("server", "set_time_am")
set_time_pm = config.get("server", "set_time_pm")
set_time_am_today = config.get("server", "set_time_am_today")
set_fish_time = config.get("server", "set_fish_time")
after_work_time = config.get("server", "after_work_time")


def morning_paper_push():
    output("每日早报推送")
    msg = get_history_event()
    room_id_list = room_id.split(",")
    for i in range(len(room_id_list)):
        send_img_room(msg, room_id_list[i])


def morning_paper_news_push():
    time.sleep(5)
    output("每日安全新闻早报推送")
    msg = get_freebuf_news()
    room_id_list = room_id.split(",")
    for i in range(len(room_id_list)):
        auto_send_message_room(msg, room_id_list[i])


def evening_paper_push():
    output("每日晚间安全资讯推送")
    msg = get_safety_news()
    room_id_list = room_id.split(",")
    for i in range(len(room_id_list)):
        auto_send_message_room(msg, room_id_list[i])


def everyday_zodiac_push():
    output("今日黄历推送")
    msg = get_today_zodiac()
    room_id_list = room_id.split(",")
    for i in range(len(room_id_list)):
        auto_send_message_room(msg, room_id_list[i])


def everyday_morning_push():
    output("今日早安寄语推送")
    time.sleep(1)
    msg = get_morning_info()
    room_id_list = room_id.split(",")
    for i in range(len(room_id_list)):
        auto_send_message_room(msg, room_id_list[i])


def everyday_fish_push():
    output("今日摸鱼日历推送")
    if (
            int(datetime.date.today().isoweekday()) == 6
            or int(datetime.date.today().isoweekday()) == 7
    ):
        pass
    else:
        msg = Touch_the_fish()
        room_id_list = room_id.split(",")
        for i in range(len(room_id_list)):
            auto_send_message_room(msg, room_id_list[i])


def everyday_after_work_push():
    output("下班通知推送")
    if (
            int(datetime.date.today().isoweekday()) == 6
            or int(datetime.date.today().isoweekday()) == 7
    ):
        msg = ""
    else:
        msg = "各部门请注意，下班时间已到！！！请滚，不要浪费电费，记得发日报！\n[Doge] over"
    room_id_list = room_id.split(",")
    for i in range(len(room_id_list)):
        auto_send_message_room(msg, room_id_list[i])


def tomato_after_work_push():
    output("番茄下班通知推送")
    msg = "各部门请注意，番茄下班时间已到！！！请火速回家，不要浪费电费，记得发日报！\n[Doge] over"
    roomid = "25348406777@chatroom"
    if int(datetime.date.today().isoweekday()) == 7:
        pass
    else:
        auto_send_message_room(msg, roomid)


# 创建定时任务
def auto_push():
    output("每日定时任务 Strat")
    # 今日黄历推送
    # schedule.every().day.at(set_time_am_today).do(everyday_zodiac_push)
    # 早安寄语
    # schedule.every().day.at(set_time_am_today).do(everyday_morning_push)
    # 早报自动推送
    schedule.every().day.at(set_time_am).do(morning_paper_push)
    # 每日安全新闻早报推送
    schedule.every().day.at(set_time_am).do(morning_paper_news_push)
    # 摸鱼日历自动推送
    # schedule.every().day.at(set_fish_time).do(everyday_fish_push)
    # 晚报自动推送
    schedule.every().day.at(set_time_pm).do(evening_paper_push)
    # 下班通知推送
    # schedule.every().day.at(after_work_time).do(everyday_after_work_push)
    # 番茄下班专属通知推送
    # schedule.every().day.at("21:00").do(tomato_after_work_push)
    while True:
        schedule.run_pending()


def main():
    output("WechatBot Run ....")
    get_personal_info()
    # processed = Process(target=auto_push, name="Auto push")
    # # 进程守护，主进程结束子进程也要结束
    # processed.daemon = True
    # processed.start()
    bot()


if __name__ == "__main__":
    f = Figlet(font="slant", width=2000)
    cprint(f.renderText("WechatBot"), "green")
    cprint("\t\t\t\t\t\t--------By zhizhuo")
    main()
