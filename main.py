from servercli.server import *
from httpcli.output import *
from httpcli.everyday_news import *
from servercli.server import *
import configparser
from apscheduler.schedulers.blocking import BlockingScheduler
from multiprocessing import Process
import datetime
import time
from pyfiglet import Figlet

# 读取本地的配置文件
current_path = os.path.dirname(__file__)
config_path = os.path.join(current_path, "./config/config.ini")
config = configparser.ConfigParser()  # 类实例化
config.read(config_path, encoding="utf-8")
admin_id = config.get("server", "admin_id")
room_id = config.get("server", "room_id")
set_time_am = config.get("server", "set_time_am").replace("[", "").replace("]", "").split(r",")
set_time_pm = config.get("server", "set_time_pm").replace("[", "").replace("]", "").split(r",")
set_time_am_today = config.get("server", "set_time_am_today").replace("[", "").replace("]", "").split(r",")
set_fish_time = config.get("server", "set_fish_time").replace("[", "").replace("]", "").split(r",")
after_work_time = config.get("server", "after_work_time").replace("[", "").replace("]", "").split(r",")


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


# 考虑到下班群有影响选择单发
def everyday_after_work_push():
    output("下班通知推送")
    if (
            int(datetime.date.today().isoweekday()) == 6
            or int(datetime.date.today().isoweekday()) == 7
    ):
        msg = ""
    else:
        msg = "【智障机器人】提醒您：\n各部门请注意，下班时间已到！！！请快速撤离，不要浪费电费，记得发日报！"
    roomid = "19006375252@chatroom"
    auto_send_message_room(msg, roomid)


def cpy_after_work_push():
    output("小鹏有下班通知推送")
    msg = "【智障机器人】提醒您：\n小迷妹请注意，小鹏有下班时间已到！！！正火速回家，不要忘记给我准备碗筷哦！"
    roomid = "44374587412@chatroom"
    if int(datetime.date.today().isoweekday()) == 7:
        pass
    else:
        auto_send_message_room(msg, roomid)


def yx_after_work_push():
    output("小迷妹下班通知推送")
    msg = "【智障机器人】提醒您：\n请注意，小迷妹下班时间已到！！！不要忘记打卡，回家路上注意安全，不要走路玩手机！"
    roomid = "44374587412@chatroom"
    if int(datetime.date.today().isoweekday()) == 7:
        pass
    else:
        auto_send_message_room(msg, roomid)


# 重写定时任务
def auto_push():
    output("每日定时任务 Strat")
    sched = BlockingScheduler()
    # 早报自动推送
    sched.add_job(morning_paper_push, 'cron', hour=set_time_am[3], minute=set_time_am[4], id='task_morning_paper_push',misfire_grace_time=60)
    # 黄历自动推送
    sched.add_job(everyday_zodiac_push, 'cron', hour=set_time_am[3], minute=set_time_am[4], id='task_everyday_zodiac_push',misfire_grace_time=60)
    # 每日安全新闻早报推送
    sched.add_job(evening_paper_push, 'cron', hour=set_time_am[3], minute=set_time_am[4], id='task_evening_paper_push1',misfire_grace_time=60)
    # 摸鱼日历自动推送
    sched.add_job(everyday_fish_push, 'cron', hour=set_fish_time[3], minute=set_fish_time[4], id='task_everyday_fish_push',misfire_grace_time=60)
    # 晚报自动推送
    # sched.add_job(evening_paper_push, 'cron', hour=set_time_pm[3], minute=set_time_pm[4], id='task_evening_paper_push',misfire_grace_time=60)
    # 下班通知推送
    # sched.add_job(everyday_after_work_push, 'cron', hour=after_work_time[3], minute=after_work_time[4], id='task_everyday_after_work_push',misfire_grace_time=60)
    # 小杨鑫下班专属通知推送
    sched.add_job(yx_after_work_push, 'cron', hour='17', minute='45', id='task_yx_after_work_push',misfire_grace_time=60)
    # 小鹏有下班专属通知推送
    sched.add_job(cpy_after_work_push, 'cron', hour='18', minute='00', id='task_cpy_after_work_push',misfire_grace_time=60)
    sched.start()


def main():
    output("WechatBot Run ....")
    get_personal_info()
    processed = Process(target=auto_push, name="Auto push")
    # 进程守护，主进程结束子进程也要结束
    processed.daemon = True
    processed.start()
    bot()


if __name__ == "__main__":
    f = Figlet(font="slant", width=2000)
    cprint(f.renderText("WechatBot"), "green")
    cprint("\t\t\t\t\t\t--------By zhizhuo")
    main()
