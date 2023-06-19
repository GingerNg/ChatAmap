#!/bin/sh
suffix='.py'
echo "脚本名称 $1$suffix"
if [ "$1" == '' ]
then
    echo "请输入脚本名称"
    exit
else
    echo "restarting"
    # ps aux|grep $1.py |awk '{print $2}'
    ps aux|grep $1$suffix|awk '{print $2}'|xargs kill -9

    nohup pipenv run python3 $1$suffix &

    ps aux|grep $1$suffix|head -3
fi


# echo "脚本全名 $1"
# name=${1%%.*}
# echo "脚本名称 $name"
# ps aux|grep $name|awk '{print $2}'|xargs kill -9
# # rasa train  --config configs/config.yml --domain configs/domain.yml

# if [[ $1 = *.js ]]
# then
#     # echo "$1 ends with .js"
#     nohup node $1 &
# elif [[ $1 = *.py ]]
# then
#     # echo "$1 ends with .py"
#     nohup python3 $1 &
# else
#     echo "$1 can be executed"
# fi

# ps aux|grep $1|head -3