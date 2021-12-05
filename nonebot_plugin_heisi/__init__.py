# python3
# -*- coding: utf-8 -*-
# @Time    : 2021/11/15 16:49
# @Author  : yzyyz
# @Email   :  youzyyz1384@qq.com
# @File    : __init__.py.py
# @Software: PyCharm
import nonebot
from nonebot import on_command,logger
from nonebot.adapters.cqhttp import Bot,Event,MessageEvent,MessageSegment,GroupMessageEvent
from nonebot.typing import T_State
import os
from os.path import dirname
import random
import requests
import datetime

heisi_group=nonebot.get_driver().config.heisi_group
heisi_cd=nonebot.get_driver().config.heisi_cd
path=dirname(__file__)+"/resources"
cddir=dirname(__file__)+"/cd"
his = on_command("his",aliases={".黑丝",".丝袜"})
@his.handle()
async def _(bot:Bot,event:GroupMessageEvent,state:T_State):
    # print(event.group_id,type(event.group_id),heisi_group,type(heisi_group))
    gid=str(event.group_id)
    if os.path.exists(path)==False:
        logger.info("创建资源路径")
        os.mkdir(path)
    if os.path.exists(path+"/heisi.txt")==False:
        where_heisi=requests.get("https://cdn.jsdelivr.net/gh/yzyyz1387/blogimages/nonebot/heisi.txt").text
        logger.info(f"从gayhub下载资源文件  {path}/heisi.txt")
        with open(path+"/heisi.txt","w",encoding="utf-8") as heisitxt:
            heisitxt.write(where_heisi)
            heisitxt.close()

    if gid in heisi_group:
        img_list=open(path+"/heisi.txt","r",encoding="utf-8").read().replace("\n","").split(".jpg")
        img = random.choice(img_list)+".jpg"
        cdtxt=cddir+"/"+gid+"cd.txt"
        if os.path.exists(cddir)==False:
            os.mkdir(cddir)
        if os.path.exists(cdtxt)==False:
            with open(cdtxt,"w") as cd:
                timenow = datetime.datetime.now()
                cd.write(str(timenow))
                cd.close()
                logger.info("初始化成功")
                await bot.send(
                    event=event,
                    message="初始化成功，当前群已开通此功能，请再发一次命令开始使用"
                )
        else:
            cdtime=open(cdtxt,"r").read()
            cdtime=datetime.datetime.strptime(cdtime,"%Y-%m-%d %H:%M:%S.%f")
            now=datetime.datetime.now()
            if int(str((now-cdtime).seconds))>int(heisi_cd):
                with open(cdtxt, "w") as cd:
                    timenow = datetime.datetime.now()
                    cd.write(str(timenow))
                    cd.close()
                await bot.send(
                    event=event,
                    message=MessageSegment.image(img)
                )
            else:
                left=int(heisi_cd)-int(str((now-cdtime).seconds))
                await bot.send(
                    event=event,
                    message="技能CD中，剩%d秒"%left
                )
    else:
        logger.info(f"群  {event.group_id} 未开通此功能，发送提示信息 ")
        await bot.send(
            event=event,
            message="当前群未开通此功能"
        )
