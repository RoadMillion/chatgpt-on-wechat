import datetime

import requests

from cmd.cmd import ICmd
from tool.geo_weather import city_matcher

gaode_api_url = 'https://restapi.amap.com/v3/weather/weatherInfo?key=035a0a19feb20a64b3c9d6d8c8c032cf&city={}' \
                '&extensions=all'


def date_format(date_str):
    datetime_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    return datetime_obj.strftime('%Y年%m月%d日')


class WeatherCmd(ICmd):

    def try_intercept(self, text, context=None):
        city_code = city_matcher.match(text)
        if city_code:
            return get_weather(city_code)
        pass


def get_weather(city_code):
    request_url = gaode_api_url.format(city_code)
    try:
        response = requests.get(request_url)
        if response.status_code == 200:
            response = response.json()
            if response['status'] == '1' and response['count'] == '1':
                messages = []
                response = response['forecasts'][0]
                city = response['city']
                casts = response['casts']
                for index, cast in enumerate(casts):
                    date_str = '今天' if index == 0 else date_format(cast["date"])
                    messages.append('{} 白天{}，夜晚{}，白天温度 {}°，夜间温度 {}°，白天{}风 {} 级'
                                    .format(date_str,
                                            cast['dayweather'], cast['nightweather'], cast['daytemp'],
                                            cast['nighttemp'], cast['daywind'], cast['daypower']))
                response = city + '\n'.join(messages)
            else:
                response = None
        return response
    except Exception as e:
        print(e)
        return None


# %Y-%m-%d格式转换为%Y年%m月%d日


weather_cmd = WeatherCmd()

if __name__ == '__main__':
    print(weather_cmd.try_intercept('北京天气'))
