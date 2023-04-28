#!/bin/sh
suffix='.js'
echo "脚本名称 $1$suffix"
# ps aux|grep $1.py |awk '{print $2}'
ps aux|grep $1$suffix|awk '{print $2}'|xargs kill -9
# rasa train  --config configs/config.yml --domain configs/domain.yml

nohup node $1$suffix &

ps aux|grep $1$suffix|head -3