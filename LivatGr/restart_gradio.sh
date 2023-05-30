#!/bin/sh
ps aux|grep main_gradio.py|awk '{print $2}'|xargs kill -9
# rasa train  --config configs/config.yml --domain configs/domain.yml

nohup python3 main_gradio.py &

ps aux|grep main_gradio:app|head -3