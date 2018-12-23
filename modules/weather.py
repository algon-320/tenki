#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from modules.print_util import Color, Style, String, Print


class Weather():

    COLOR = {
      '晴れ' : Color('#FFC235'),
      '曇り' : Color('#BBBBBB'),
      '小雨' : Color('#80C7E6'),
      '弱雨' : Color('#77ABEA'),
      '雨'   : Color('#437CE6'),
    }
    COLOR_UNK   = Color('#FF0A70')
    COLOR_RED   = Color('#F06060')
    COLOR_BLUE  = Color('#17ABEB')
    COLOR_WHITE = Color('#FFFFFF')


    def __init__(self):
        self.date = ''
        self.weathers = []
        self.temperatures = []
        self.is_past = []
        self.probability_of_rains = []
        self.amount_of_rains = []
        self.humidities = []


    def print_weather(self, width, unit_width=4, no_color=False, conky=False):
        sys.stdout.write(String.rjust('[' + self.date + '] | ', width))
        for (weather, past) in zip(self.weathers, self.is_past):
            style = Style.BOLD
            if past:
                style |= Style.WEAKEN
            if no_color == False:
                Print.change_color(Weather.COLOR.get(weather, Weather.COLOR_UNK), weaken=past, conky=conky)
            Print.change_style(style, conky=conky)
            sys.stdout.write(String.rjust(weather, unit_width))
            Print.change_style(Style.RESET, conky=conky)
            sys.stdout.write(' ')
        sys.stdout.write('\n')


    def print_temperature(self, width, unit_width=4, no_color=False, conky=False):
        max_temperature = max(self.temperatures)
        min_temperature = min(self.temperatures)
        sys.stdout.write(String.rjust('気温(度) | ', width))
        for (temp, past) in zip(self.temperatures, self.is_past):
            Print.change_color(Weather.COLOR_WHITE, weaken=past, conky=conky)
            if past:
                Print.change_style(Style.WEAKEN, conky=conky)
            if no_color == False:
                if temp == max_temperature:
                    Print.change_style(Style.BOLD, conky=conky)
                    Print.change_color(Weather.COLOR_RED, weaken=past, conky=conky)
                elif temp == min_temperature:
                    Print.change_style(Style.BOLD, conky=conky)
                    Print.change_color(Weather.COLOR_BLUE, weaken=past, conky=conky)
            sys.stdout.write(String.rjust('%.1f' % temp, unit_width))
            Print.change_style(Style.RESET, conky=conky)
            sys.stdout.write(' ')
        sys.stdout.write('\n')


    def print_probability_of_rain(self, width, unit_width=4, no_color=False, conky=False):
        sys.stdout.write(String.rjust('降水確率(%) | ', width))
        for (prb_rain, past) in zip(self.probability_of_rains, self.is_past):
            Print.change_color(Weather.COLOR_WHITE, weaken=past, conky=conky)
            sys.stdout.write(String.rjust('%d' % prb_rain, unit_width))
            Print.change_style(Style.RESET, conky=conky)
            sys.stdout.write(' ')
        sys.stdout.write('\n')


    def print_amount_of_rain(self, width, unit_width=4, no_color=False, conky=False):
        sys.stdout.write(String.rjust('降水量(mm/h) | ', width))
        for (amo_rain, past) in zip(self.amount_of_rains, self.is_past):
            Print.change_color(Weather.COLOR_WHITE, weaken=past, conky=conky)
            sys.stdout.write(String.rjust('%.1f' % amo_rain, unit_width))
            Print.change_style(Style.RESET, conky=conky)
            sys.stdout.write(' ')
        sys.stdout.write('\n')


    def print_humidity(self, width, unit_width=4, no_color=False, conky=False):
        sys.stdout.write(String.rjust('湿度(%) | ', width))
        for (humid, past) in zip(self.humidities, self.is_past):
            Print.change_color(Weather.COLOR_WHITE, weaken=past, conky=conky)
            sys.stdout.write(String.rjust('%d' % humid, unit_width))
            Print.change_style(Style.RESET, conky=conky)
            sys.stdout.write(' ')
        sys.stdout.write('\n')
