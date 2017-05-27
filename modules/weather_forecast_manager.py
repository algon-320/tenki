#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
import pickle
import lxml.html
import urllib2
import re
from weather import Weather
from print_util import String


class WeatherForecastManager:

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
        self.update_weather(days)


    def update_weather(self, days=2):
        try:
            html = urllib2.urlopen(self.url)
        except:
            print '[error] cannot open URL'
            sys.exit(1)

        dom = lxml.html.parse(html)
        announce_datetime = dom.xpath(r'//*[@id="point_announce_datetime"]')[0].text
        self.updated_time = announce_datetime
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
            w.is_past = map(lambda td: bool(re.match('.*past.*', td[0].attrib['src'])), tds_weather)
            w.temperatures = map(lambda td: float(td[0].text), tds_temperature)
            w.probability_of_rains = map(lambda td: int(td[0].text), tds_probability_of_rain)
            w.amount_of_rains = map(lambda td: float(td[0].text), tds_amount_of_rain)
            w.humidities = map(lambda td: int(td[0].text), tds_humidity)

            self.weathers.append(w)


    # 現状使っていない TODO
    def pickle(self):
        with open('tenki' + '.dump', 'w') as f:
            pickle.dump((self.url, self.weather, self.updated_time), f)
    def unpickle(self):
        with open('tenki.dump', 'r') as f:
            tmp = pickle.load(f)
            self.url = tmp[0]
            self.weather = tmp[1]
            self.updated_time = tmp[2]


    def print_weather(self, show_opts=None):
        if show_opts == None:
            show_opts = WeatherForecastManager.SHOW_ALL

        print '----------------------------------------------------------------'
        print (self.point_name + u'の天気  (' + self.updated_time + ')')
        max_width = 0
        for w in self.weathers:
            if max_width < String.get_string_width(w.date):
                max_width = String.get_string_width(w.date)

        max_width += 6

        sys.stdout.write(' ' * max_width + '03時 06時 09時 12時 15時 18時 21時 24時\n')
        print '================================================================'
        for w in self.weathers:
            col = bool(show_opts & WeatherForecastManager.SHOW_WITHOUT_COLORS)
            if show_opts & WeatherForecastManager.SHOW_WEATHER:
                w.print_weather(max_width, no_color=col)
            if show_opts & WeatherForecastManager.SHOW_TEMPERATURE:
                w.print_temperature(max_width, no_color=col)
            if show_opts & WeatherForecastManager.SHOW_PROBABILITY_OF_RAIN:
                w.print_probability_of_rain(max_width, no_color=col)
            if show_opts & WeatherForecastManager.SHOW_AMOUNT_OF_RAIN:
                w.print_amount_of_rain(max_width, no_color=col)
            if show_opts & WeatherForecastManager.SHOW_HUMIDITY:
                w.print_humidity(max_width, no_color=col)
            print '================================================================'


    # def debug_print(self):
    #     w = Weather()
    #     w.date = u'X月Y日(Z)'
    #     w.weathers = [u'晴れ', u'曇り', u'小雨', u'弱雨', u'雨', u'HOGE', u'FUGA', u'PIYO']
    #     w.is_past = [False, False, False, False, False, False, False, False]
    #     w.temperatures = [-20, -10, 0, 10, 20, 30, 40, 50]
    #     w.probability_of_rains = [0, 10, 20, 30, 40, 50, 60, 70]
    #     w.amount_of_rains = [0, 10, 20, 30, 40, 50, 60, 70]
    #     w.humidities = [0, 10, 20, 30, 40, 50, 60, 70]
    #
    #     width = 15
    #
    #     print '=======[ COLOR / FUTURE ]========================================\n'
    #     w.print_weather(width)
    #     w.print_temperature(width)
    #     w.print_probability_of_rain(width)
    #     w.print_amount_of_rain(width)
    #     w.print_humidity(width)
    #     print '\n========[ WITHOUT COLOR / FUTURE ]===============================\n'
    #     w.print_weather(width, no_color=True)
    #     w.print_temperature(width, no_color=True)
    #     w.print_probability_of_rain(width, no_color=True)
    #     w.print_amount_of_rain(width, no_color=True)
    #     w.print_humidity(width, no_color=True)
    #
    #     w.is_past = [True, True, True, True, True, True, True, True]
    #
    #     print '\n========[ COLOR / PAST ]=========================================\n'
    #     w.print_weather(width)
    #     w.print_temperature(width)
    #     w.print_probability_of_rain(width)
    #     w.print_amount_of_rain(width)
    #     w.print_humidity(width)
    #     print '\n========[ WITHOUT COLOR / PAST ]=================================\n'
    #     w.print_weather(width, no_color=True)
    #     w.print_temperature(width, no_color=True)
    #     w.print_probability_of_rain(width, no_color=True)
    #     w.print_amount_of_rain(width, no_color=True)
    #     w.print_humidity(width, no_color=True)
    #     print '\n================================================================='
