#!/bin/sh
suffix='.py'
echo "脚本名称 $1$suffix"
# ps aux|grep $1.py |awk '{print $2}'
ps aux|grep $1$suffix|awk '{print $2}'|xargs kill -9

nohup python3 $1$suffix &

ps aux|grep $1$suffix|head -3
