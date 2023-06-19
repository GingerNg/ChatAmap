#!/bin/sh
suffix='.js'
echo "脚本名称 $1$suffix"
if [ "$1" == '' ]
then
    echo "请输入脚本名称"
    exit
else
    echo "restarting"
    # ps aux|grep $1.py |awk '{print $2}'
    ps aux|grep $1$suffix|awk '{print $2}'|xargs kill -9

    nohup node $1$suffix &

    ps aux|grep $1$suffix|head -3
fi