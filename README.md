# WechatBot
一个基于PC版的微信机器人，采用hook的形式进行消息拦截，内存信息读取的形式获取通讯录，用户信息等

感谢@cixingguangming55555开发的server端以及集成化的hook利用程序，本项目是基于@cixingguangming55555大佬的开源项目进行的二开（玩法很多我慢慢开发吧，就这样吧）

这里需要使用的微信版本是3.2.0.121版本，历史版本下载地址

- https://github.com/tom-snow/wechat-windows-versions

## 部署教程

安装微信3.2.0.121版本，然后再打开ServerMain/server中的微信DLL注入器V1.0.3.exe工具进行dll注入

![image-20220915181623688](images/image-20220915181623688.png) 

点击注入即可，然后接下来就是项目的config目录下面的config.ini的配置

config.ini详解

```
[server]
# 微信机器人服务端的配置文件
ip = 127.0.0.1
port = 5555
admin_id = wxid_kb0e7h9icqqv22

[apiService]
# MD5解密接口
md5_url = 
# 舔狗日记接口
dog_url = http://api.tianapi.com/
# 彩虹屁接口
fart_url = http://api.tianapi.com/
# 历史上的今天
history_url = https://api.qqsuu.cn/api/60s
# 当日安全新闻
secwiki_url = https://www.sec-wiki.com/news/rss
freebuf_url = https://www.freebuf.com/feed
qax_url = https://forum.butian.net/Rss
anquanke_url = https://www.anquanke.com/knowledge
```

**admin_id是管理员ID，在程序跑起来之后你给机器人发送一个消息即可看见**

![image-20220915181940797](images/image-20220915181940797.png) 

这个就是你的管理身份账号

**舔狗日记和彩虹屁接口信息可以到https://www.tianapi.com进行注册获取**

## 项目启动

首先使用命令安装依赖

```bash
pip3 install -r requirements.txt
```

如果出现WebSocketApp no modle的报错，使用命令安装此依赖即可

```bash
pip3 install websocket-client-py3
```

然后使用命令即可启动项目

```bash
python3 main.py
```

***建议使用python3.8以上**

## 后续开发计划

- 实现每日咨询自动定时推送（暂时只可以管理员指定获取）
- 实现GitHub实时监控
- 实现第三方工具实时推送
- 待定，有需求可以提交lessus

## 最后

代码写的烂，轻点喷，毕竟我这么菜，后续项目迭代看心情吧，就这样

## 参考资料

- https://github.com/Le0nsec/SecCrawler
- https://github.com/tom-snow/wechat-windows-versions
