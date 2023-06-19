import requests

from utils.env_utils import gaode_key
key = gaode_key
class GaoDe(object):
    def __init__(self) -> None:
        """
        https://restapi.amap.com/v5/direction/driving?parameters
        https://restapi.amap.com/v5/direction/walking?parameters
        https://restapi.amap.com/v5/direction/bicycling?parameters
        https://restapi.amap.com/v5/direction/electrobike?parameters
        https://restapi.amap.com/v5/direction/transit/integrated
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
        for step in result['route']['transits'][0]['segments']:
            print(step)

    @staticmethod
    def geocode(address, city=None):
        print(f"geocode input: {address}")
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
        print(result)
        return result['geocodes'][0]['location']


if __name__ == "__main__":
    gaode = GaoDe()
    start_loc = '121.392456,31.315883'
    end_loc = '121.452284,31.274056'
    gaode.direction(origin=start_loc, destination=end_loc, city1="021", city2="021")