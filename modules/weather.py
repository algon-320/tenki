#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
from print_util import Color, Style, String, Print


class Weather():

    COLOR = {
      u'晴れ' : Color('#FFC235'),
      u'曇り' : Color('#BBBBBB'),
      u'小雨' : Color('#80C7E6'),
      u'弱雨' : Color('#77ABEA'),
      u'雨'   : Color('#437CE6'),
    }
    COLOR_UNK   = Color('#FF0A70')
    COLOR_RED   = Color('#F06060')
    COLOR_BLUE  = Color('#17ABEB')
    COLOR_WHITE = Color('#FFFFFF')


    def __init__(self):
        self.date = ''
        self.wathers = []
        self.temperatures = []
        self.is_past = []
        self.probability_of_rains = []
        self.amount_of_rains = []
        self.humidities = []


    def print_weather(self, width, unit_width=4, no_color=False):
        sys.stdout.write(String.rjust_unicode(u'[' + self.date + u'] | ', width))
        for (weather, past) in zip(self.weathers, self.is_past):
            style = Style.BOLD
            if past:
                style |= Style.WEAKEN
            if no_color == False:
                Print.change_color(Weather.COLOR.get(weather, Weather.COLOR_UNK), past)
            Print.change_style(style)
            sys.stdout.write(String.rjust_unicode(weather, unit_width))
            Print.change_style(Style.RESET)
            sys.stdout.write(' ')
        sys.stdout.write('\n')


    def print_temperature(self, width, unit_width=4, no_color=False):
        max_temperature = max(self.temperatures)
        min_temperature = min(self.temperatures)
        sys.stdout.write(String.rjust_unicode(u'気温(度) | ', width))
        for (temp, past) in zip(self.temperatures, self.is_past):
            if past:
                Print.change_style(Style.WEAKEN)
            if no_color == False:
                if temp == max_temperature:
                    Print.change_style(Style.BOLD)
                    Print.change_color(Weather.COLOR_RED, past)
                elif temp == min_temperature:
                    Print.change_style(Style.BOLD)
                    Print.change_color(Weather.COLOR_BLUE, past)
            sys.stdout.write(String.rjust_unicode(unicode(temp), unit_width))
            Print.change_style(Style.RESET)
            sys.stdout.write(' ')
        sys.stdout.write('\n')


    def print_probability_of_rain(self, width, unit_width=4, no_color=False):
        sys.stdout.write(String.rjust_unicode(u'降水確率(%) | ', width))
        for (prb_rain, past) in zip(self.probability_of_rains, self.is_past):
            if past:
                Print.change_style(Style.WEAKEN)
            sys.stdout.write(String.rjust_unicode(unicode(prb_rain), unit_width))
            Print.change_style(Style.RESET)
            sys.stdout.write(' ')
        sys.stdout.write('\n')


    def print_amount_of_rain(self, width, unit_width=4, no_color=False):
        sys.stdout.write(String.rjust_unicode(u'降水量(mm/h) | ', width))
        for (amo_rain, past) in zip(self.amount_of_rains, self.is_past):
            if past:
                Print.change_style(Style.WEAKEN)
            sys.stdout.write(String.rjust_unicode(unicode(amo_rain), unit_width))
            Print.change_style(Style.RESET)
            sys.stdout.write(' ')
        sys.stdout.write('\n')


    def print_humidity(self, width, unit_width=4, no_color=False):
        sys.stdout.write(String.rjust_unicode(u'湿度(%) | ', width))
        for (humid, past) in zip(self.humidities, self.is_past):
            if past:
                Print.change_style(Style.WEAKEN)
            sys.stdout.write(String.rjust_unicode(unicode(humid), unit_width))
            Print.change_style(Style.RESET)
            sys.stdout.write(' ')
        sys.stdout.write('\n')