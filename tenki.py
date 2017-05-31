#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import click
from modules.weather_forecast_manager import WeatherForecastManager


@click.command()

def tenki():
    # つくば市の天気
    wfm = WeatherForecastManager('http://www.tenki.jp/forecast/3/11/4020/8220.html')
    wfm.print_weather(WeatherForecastManager.SHOW_ALL, conky=True)

if __name__ == '__main__':
    tenki()
