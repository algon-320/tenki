#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import datetime
import pickle
import lxml.html
import urllib.request, urllib.error
import re
from modules.weather import Weather
from modules.print_util import String


class WeatherForecastManager:
    PICKLE_DUMP_FILE = 'tenki.dump'

    XPATH_UPDATED_TIME = r'//*[@id="main-column"]/section/h2/time/text()'
    XPATH_POINT_INFO = r'//*[@id="main-column"]/section/h2/text()'
    XPATH_UPDATED_TIME_DETAIL_COMMENT = r'//*[@id="main-column"]/section/h2/time/comment()'
    XPATH_WEATHER_DATES = r'//*[@id="main-column"]/section/table[%d]/tr[1]/td/div/p/text()'
    XPATH_WEATHER_TD = r'//*[@id="main-column"]/section/table[%d]/tr[4]/td'
    XPATH_TEMPERATURE_TD = r'//*[@id="main-column"]/section/table[%d]/tr[6]/td'
    XPATH_PROB_RAIN_TD = r'//*[@id="main-column"]/section/table[%d]/tr[7]/td'
    XPATH_AMOUNT_RAIN_TD = r'//*[@id="main-column"]/section/table[%d]/tr[9]/td'
    XPATH_HUMIDITY_TD = r'//*[@id="main-column"]/section/table[%d]/tr[10]/td'

    SHOW_OPTS = (
        SHOW_WEATHER,
        SHOW_TEMPERATURE,
        SHOW_PROBABILITY_OF_RAIN,
        SHOW_AMOUNT_OF_RAIN,
        SHOW_HUMIDITY,
        SHOW_WITHOUT_COLORS,
    ) = map(lambda x: 1 << x, range(6))
    SHOW_ALL = SHOW_WEATHER | SHOW_TEMPERATURE | SHOW_PROBABILITY_OF_RAIN | SHOW_AMOUNT_OF_RAIN | SHOW_HUMIDITY


    def __init__(self, spot_url):
        self.url = spot_url
        self.weathers = []
        self.updated_time = None
        self.point_name = ''

        if os.path.exists(WeatherForecastManager.PICKLE_DUMP_FILE):
            self.unpickle()
            if self.updated_time + datetime.timedelta(hours=1) > datetime.datetime.now() and self.url == spot_url:
                return
        self.update_weather(spot_url)

    def update_weather(self, url):
        # print('[debug] checking for updates ...')
        try:
            html = urllib.request.urlopen(url).read()
        except:
            print('[error] cannot open URL')
            sys.exit(1)

        dom = lxml.html.fromstring(html.decode('utf-8'))
        updated_time_str = dom.xpath(WeatherForecastManager.XPATH_UPDATED_TIME)[0]
        point_info = dom.xpath(WeatherForecastManager.XPATH_POINT_INFO)[0]
        self.point_name = re.match(r'(.+)の天気', point_info).group(1)

        # 更新日時を設定
        comment = dom.xpath(WeatherForecastManager.XPATH_UPDATED_TIME_DETAIL_COMMENT)[0]
        comment = lxml.html.tostring(comment, method='html', encoding='unicode')
        mat = re.match(r'.*generate at (\d{4})\-(\d{2})\-\d{2} \d{2}\:\d{2}\:\d{2}', comment)
        year = int(mat.group(1))
        month = int(mat.group(2))
        mat = re.match(r'(\d+)日(\d+):(\d+)発表', updated_time_str)
        day = int(mat.group(1))
        hour = int(mat.group(2))
        minute = int(mat.group(3))
        self.updated_time = datetime.datetime(year, month, day, hour, minute)

        self.weathers = []

        for k in range(3):
            w = Weather()
            w.date = dom.xpath(WeatherForecastManager.XPATH_WEATHER_DATES % (k + 1))[0][:-1]
            tds_weather = dom.xpath(WeatherForecastManager.XPATH_WEATHER_TD % (k + 1))
            tds_temperature = dom.xpath(WeatherForecastManager.XPATH_TEMPERATURE_TD % (k + 1))
            tds_probability_of_rain = dom.xpath(WeatherForecastManager.XPATH_PROB_RAIN_TD % (k + 1))
            tds_amount_of_rain = dom.xpath(WeatherForecastManager.XPATH_AMOUNT_RAIN_TD % (k + 1))
            tds_humidity = dom.xpath(WeatherForecastManager.XPATH_HUMIDITY_TD % (k + 1))

            w.weathers = list(map(lambda td: td[1].text, tds_weather))
            w.is_past = list(map(lambda td: ('past' in td[0].attrib['src']), tds_weather))
            w.temperatures = list(map(lambda td: float(td[0].text), tds_temperature))
            w.probability_of_rains = list(map(lambda td: int(td[0].text), tds_probability_of_rain))
            w.amount_of_rains = list(map(lambda td: float(td[0].text), tds_amount_of_rain))
            w.humidities = list(map(lambda td: int(td[0].text), tds_humidity))

            self.weathers.append(w)

        self.pickle_data()

    def pickle_data(self):
        with open(WeatherForecastManager.PICKLE_DUMP_FILE, 'wb') as f:
            tmp = (self.url, self.weathers, self.updated_time, self.point_name)
            pickle.dump(tmp, f)

    def unpickle(self):
        with open(WeatherForecastManager.PICKLE_DUMP_FILE, 'rb') as f:
            tmp = pickle.load(f)
            self.url = tmp[0]
            self.weathers = tmp[1]
            self.updated_time = tmp[2]
            self.point_name = tmp[3]


    def print_weather(self, show_opts=None, conky=False, days=2):
        if show_opts == None:
            show_opts = WeatherForecastManager.SHOW_ALL

        max_width = 0
        for w in self.weathers:
            max_width = max(max_width, String.get_string_width(w.date))
        max_width += 6

        max_unit_width = 0
        for i in range(days):
            w = self.weathers[i]
            for tmp in w.weathers:
                max_unit_width = max(max_unit_width, String.get_string_width(tmp))

        print('-' * (max_width + (max_unit_width + 1) * 8))
        print('{p}の天気 ({M}月{D}日 {h:02d}:{m:02d} 発表)'.format(p=self.point_name,
          M=self.updated_time.month, D=self.updated_time.day,
          h=self.updated_time.hour, m=self.updated_time.minute))
        
        time_labels = ['03時', '06時', '09時', '12時', '15時', '18時', '21時', '24時']
        sys.stdout.write((' ' * max_width))
        for l in time_labels:
            sys.stdout.write(String.center(l, max_unit_width + 1))
        sys.stdout.write('\n')

        print('=' * (max_width + (max_unit_width + 1) * 8))
        for i in range(days):
            w = self.weathers[i]
            col = bool(show_opts & WeatherForecastManager.SHOW_WITHOUT_COLORS)
            if show_opts & WeatherForecastManager.SHOW_WEATHER:
                w.print_weather(max_width, max_unit_width, no_color=col, conky=conky)
            if show_opts & WeatherForecastManager.SHOW_TEMPERATURE:
                w.print_temperature(max_width, max_unit_width, no_color=col, conky=conky)
            if show_opts & WeatherForecastManager.SHOW_PROBABILITY_OF_RAIN:
                w.print_probability_of_rain(max_width, max_unit_width, no_color=col, conky=conky)
            if show_opts & WeatherForecastManager.SHOW_AMOUNT_OF_RAIN:
                w.print_amount_of_rain(max_width, max_unit_width, no_color=col, conky=conky)
            if show_opts & WeatherForecastManager.SHOW_HUMIDITY:
                w.print_humidity(max_width, max_unit_width, no_color=col, conky=conky)
            print('=' * (max_width + (max_unit_width + 1) * 8))
