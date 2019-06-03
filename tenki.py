#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------- for speedup urllib.request.urlopen
import socket
def getAddrInfoWrapper(host, port, family=0, socktype=0, proto=0, flags=0):
    return origGetAddrInfo(host, port, socket.AF_INET, socktype, proto, flags)
origGetAddrInfo = socket.getaddrinfo
socket.getaddrinfo = getAddrInfoWrapper
# -------------------------------------------------

import os
import click
from modules.weather_forecast_manager import WeatherForecastManager

@click.command(help='天気予報を表示します。(tenki.jp)')
@click.option('--url', type=str, default='https://tenki.jp/forecast/3/11/4020/8220/3hours.html',
              help='3時間天気のページのURL') # つくば市の天気
@click.option('--days', type=int, default=2, help='表示させる日数[1~3] (デフォルト2)')
@click.option('--conky', is_flag=True, help='Conkyに表示させるときに指定してください')
@click.option('--slim', is_flag=True, help='湿度、風速を表示しない')
def tenki(url, days, conky, slim):
    wfm = WeatherForecastManager(url)
    if slim:
        show = \
            WeatherForecastManager.SHOW_WEATHER | \
            WeatherForecastManager.SHOW_TEMPERATURE | \
            WeatherForecastManager.SHOW_PROBABILITY_OF_RAIN
        wfm.print_weather(show, conky=conky, days=days)
    else:
        wfm.print_weather(WeatherForecastManager.SHOW_ALL, conky=conky, days=days)

if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    tenki()
