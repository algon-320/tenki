#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import click
from modules.weather_forecast_manager import WeatherForecastManager


@click.command()
@click.option('--url', type=str, default='http://www.tenki.jp/forecast/3/11/4020/8220.html',
              help=u'ピンポイント天気(3時間天気)のページのURL') # つくば市の天気
@click.option('--conky', is_flag=True, help=u'Conkyに表示させるときに指定してください')
def tenki(url, conky):
    wfm = WeatherForecastManager(url)
    wfm.print_weather(WeatherForecastManager.SHOW_ALL, conky=conky)

if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    print os.getcwd()
    tenki()
