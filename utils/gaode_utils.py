import requests
from . import env
from .logger_utils import logging

key = env.gaode_key

class GaoDe(object):
    def __init__(self) -> None:
        """
        """
        pass

    @staticmethod
    def direction(origin, destination, city1, city2):
        url = 'https://restapi.amap.com/v5/direction/transit/integrated'
        params = {
            'key': key,
            'origin': origin,
            'destination': destination,
            'city1': city1,
            'city2': city2
        }
        response = requests.get(url, params=params)
        result = response.json()
        # print(result)
        routes = []
        for seg in result['route']['transits'][0]['segments']:
            for k,v in seg.items():
                # print(k,v)
                if k == "walking":
                    line = f"步行, {v['distance']}米"
                    routes.append(line)
                    logging.debug(line)
                elif k == "bus":
                    line = f"公交, {v['buslines'][0]['name']},{v['buslines'][0]['departure_stop']['name']}上车, {v['buslines'][0]['arrival_stop']['name']}下车"
                    routes.append(line)
                    logging.debug(line)
        logging.debug("---------------")
        return routes
                # print(k, v)

    @staticmethod
    def geocode(address, city=None):
        address = address.strip('\'')
        if city: city = city.strip('\'')
        logging.debug(f"geocode input: {address}, {city}")
        """
        address --> location(Lat Lng)
        [{'formatted_address': 'XXXXXX',
        'country': '中国',
        'province': '上海市',
        'citycode': '021',
        'city': '上海市',
        'district': '静安区',
        'township': [],
        'neighborhood': {'name': [], 'type': []},
        'building': {'name': [], 'type': []},
        'adcode': '310106',
        'street': [],
        'number': [],
        'location': '121.457689,31.275837',
        'level': '兴趣点'}]
        """

        url = 'https://restapi.amap.com/v3/geocode/geo'
        params = {
            'key': key,
            'address': address,
        }
        if city is not None: params["city"] = city
        response = requests.get(url, params=params)
        result = response.json()
        logging.debug(result)
        return result['geocodes'][0]['location']


if __name__ == "__main__":
    gaode = GaoDe()
    start_loc = '121.392456,31.315883'
    end_loc = '121.452284,31.274056'
    gaode.direction(origin=start_loc, destination=end_loc, city1="021", city2="021")