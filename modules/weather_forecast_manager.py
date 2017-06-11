#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
import os
import datetime
import pickle
import lxml.html
import urllib2
import re
from weather import Weather
from print_util import String


class WeatherForecastManager:
    PICKLE_DUMP_FILE = 'tenki.dump'

    SHOW_OPTS = (
        SHOW_WEATHER,
        SHOW_TEMPERATURE,
        SHOW_PROBABILITY_OF_RAIN,
        SHOW_AMOUNT_OF_RAIN,
        SHOW_HUMIDITY,
        SHOW_WITHOUT_COLORS,
    ) = map(lambda x: 1 << x, range(6))
    SHOW_ALL = SHOW_WEATHER | SHOW_TEMPERATURE | SHOW_PROBABILITY_OF_RAIN | SHOW_AMOUNT_OF_RAIN | SHOW_HUMIDITY


    def __init__(self, url, days=2):
        self.url = url
        self.weathers = []
        self.updated_time = None
        self.point_name = ''

        if os.path.exists(WeatherForecastManager.PICKLE_DUMP_FILE):
            self.unpickle()
            def parse_date(timestr):
                mat = re.match(ur'(\d+)年(\d+)月(\d+)日(\d+):(\d+)発表', timestr)
                year = int(mat.group(1))
                month = int(mat.group(2))
                day = int(mat.group(3))
                hour = int(mat.group(4))
                minute = int(mat.group(5))
                return datetime.datetime(year, month, day, hour, minute)

            last_update = parse_date(self.updated_time)
            if last_update + datetime.timedelta(hours=2) <= datetime.datetime.now():
                self.weathers = []
                self.update_weather(days)
        else:
            self.update_weather(days)



    def update_weather(self, days=2):
        # print '[info] checking for update ...'
        try:
            html = urllib2.urlopen(self.url)
        except:
            print '[error] cannot open URL'
            sys.exit(1)

        dom = lxml.html.parse(html)
        self.updated_time = dom.xpath(r'//*[@id="point_announce_datetime"]')[0].text
        point_info = dom.xpath(r'//*[@id="pinpoint_weather_name"]')[0].text
        self.point_name = re.match(ur'(.+)のピンポイント天気', point_info).group(1)

        for k in range(days):
            w = Weather()
            w.date = dom.xpath(r'//*[@id="bd-main"]/div[1]/table[%d]/thead/tr/td/div/p' % (k + 1))[0].text
            tds_weather = dom.xpath(r'//*[@id="bd-main"]/div[1]/table[%d]/tbody/tr[3]/td' % (k + 1))
            tds_temperature = dom.xpath(r'//*[@id="bd-main"]/div[1]/table[%d]/tbody/tr[5]/td' % (k + 1))
            tds_probability_of_rain = dom.xpath(r'//*[@id="bd-main"]/div[1]/table[%d]/tbody/tr[6]/td' % (k + 1))
            tds_amount_of_rain = dom.xpath(r'//*[@id="bd-main"]/div[1]/table[%d]/tbody/tr[8]/td' % (k + 1))
            tds_humidity = dom.xpath(r'//*[@id="bd-main"]/div[1]/table[%d]/tbody/tr[9]/td' % (k + 1))

            w.weathers = map(lambda td: td[1].text, tds_weather)
            w.is_past = map(lambda td: ('past' in td[0].attrib['src']), tds_weather)
            w.temperatures = map(lambda td: float(td[0].text), tds_temperature)
            w.probability_of_rains = map(lambda td: int(td[0].text), tds_probability_of_rain)
            w.amount_of_rains = map(lambda td: float(td[0].text), tds_amount_of_rain)
            w.humidities = map(lambda td: int(td[0].text), tds_humidity)

            self.weathers.append(w)

        self.pickle()


    def pickle(self):
        with open(WeatherForecastManager.PICKLE_DUMP_FILE, 'w') as f:
            pickle.dump((self.url, self.weathers, self.updated_time, self.point_name), f)

    def unpickle(self):
        with open(WeatherForecastManager.PICKLE_DUMP_FILE, 'r') as f:
            tmp = pickle.load(f)
            self.url = tmp[0]
            self.weathers = tmp[1]
            self.updated_time = tmp[2]
            self.point_name = tmp[3]


    def print_weather(self, show_opts=None, conky=False):
        if show_opts == None:
            show_opts = WeatherForecastManager.SHOW_ALL

        print '----------------------------------------------------------------'
        print (self.point_name + u'の天気  (' + self.updated_time + ')').encode('utf-8')
        max_width = 0
        for w in self.weathers:
            if max_width < String.get_string_width(w.date):
                max_width = String.get_string_width(w.date)

        max_width += 6

        sys.stdout.write((u' ' * max_width + u'03時 06時 09時 12時 15時 18時 21時 24時\n').encode('utf-8'))
        print '================================================================'
        for w in self.weathers:
            col = bool(show_opts & WeatherForecastManager.SHOW_WITHOUT_COLORS)
            if show_opts & WeatherForecastManager.SHOW_WEATHER:
                w.print_weather(max_width, no_color=col, conky=conky)
            if show_opts & WeatherForecastManager.SHOW_TEMPERATURE:
                w.print_temperature(max_width, no_color=col, conky=conky)
            if show_opts & WeatherForecastManager.SHOW_PROBABILITY_OF_RAIN:
                w.print_probability_of_rain(max_width, no_color=col, conky=conky)
            if show_opts & WeatherForecastManager.SHOW_AMOUNT_OF_RAIN:
                w.print_amount_of_rain(max_width, no_color=col, conky=conky)
            if show_opts & WeatherForecastManager.SHOW_HUMIDITY:
                w.print_humidity(max_width, no_color=col, conky=conky)
            print '================================================================'
