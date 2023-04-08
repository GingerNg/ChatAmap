from utils.openai_utils import Openai
from utils import gaode_utils
from utils.logger_utils import logging
gaode = gaode_utils.GaoDe()
def get_location(text):
    logging.debug(f"openai input: {text}")
    messages =[
            {"role": "system", "content": "你是一个路径规划机器人"},
            {"role": "user", "content": f"识别以下句子中我的起点，终点和经过的地点，以及所在城市\
                                            返回格式：|'起点'|'终点'|'经过的地点'|'城市'|， \
                                          如果无法识别起点和终点，则追问，\
                                          句子：{text}"}
        ]
    openai_obj = Openai()
    result = []
    resp = openai_obj.chat_complete(messages)
    for r in resp:
        one = r.choices[0].delta.content if 'content' in r.choices[0].delta else ''
        result.append(one)
    res = "".join(result)
    logging.debug(f"openai output: {res}")
    return res

import re
def parse(text):
    text = text.replace('\'','')
    items = text.split("|")
    start = items[1]
    end = items[2]
    vias = re.split('[,，、]', items[3])
    city = items[4]
    return [start, end, vias, city]

def plan_route(text):
    """plan route"""
    loc_str = get_location(text)
    if loc_str.startswith("|"):
        start, end, vias, city = parse(loc_str)
        logging.debug(start, end, vias, city)
    # locations = loc_str.split("｜")
    # print(locations)
    start_lng_lat = gaode.geocode(start, city=city)
    end_lng_lat = gaode.geocode(end, city=city)
    via_lng_lats = [gaode.geocode(location, city=city) for location in vias]
    routes = {}
    routes[f"{start}->{vias[0]}"] = gaode.direction(origin=start_lng_lat, destination=via_lng_lats[0], city1="021", city2="021")
    for i in range(1, len(via_lng_lats)):
        routes[f"{vias[i-1]}->{vias[i]}"] = gaode.direction(origin=via_lng_lats[i-1], destination=via_lng_lats[i], city1="021", city2="021")
    routes[f"{vias[-1]}->{end}"] = gaode.direction(origin=via_lng_lats[-1], destination=end_lng_lat, city1="021", city2="021")
    return routes