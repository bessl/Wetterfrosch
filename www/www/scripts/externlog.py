# -*- coding: utf-8 -*-
import os
import sys
import transaction
from openweathermap_requests import OpenWeatherMapRequests
import re
import requests
import numpy as np
import logging
from paste.deploy.loadwsgi import appconfig

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models import (
    DBSession,
    Log,
    Base,
    )

logger = logging.getLogger(__name__)
config = appconfig('config:development.ini', 'main', relative_to='.')
debug = False


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    get_data()


def get_data():
    data = {}

    # yahoo
    try:
        ya = requests.get("http://weather.yahooapis.com/forecastrss?w=550505&u=c")
        ya_humidity = re.findall(r'humidity="(\d+)"', ya.text)[0]
        ya_wind = re.findall(r'speed="([\.\d]+)"', ya.text)[0]
        ya_temp = re.findall(r'temp="(\d+)"', ya.text)[0]
        data["ya"] = {
            "humidity": ya_humidity,
            "temperature": ya_temp,
            "wind": ya_wind
        }
        logger.info("yahoo done")
    except:
        logger.error("Yahoo failed")

    # http://home.openweathermap.org/
    try:
        ow = OpenWeatherMapRequests(api_key=config["api_openweather"], cache_name='cache-openweathermap', expire_after=5*60)
        ow_data = ow.get_weather(lon=config["cords_lon"], lat=config["cords_lat"])
        data["ow"] = {
            "humidity": ow_data["main"]["humidity"],
            "temperature": ow_data["main"]["temp"],
            "wind": ow_data["wind"]["speed"]
        }
        logger.info("openweathermap.org done")
    except:
        logger.error("openweathermap.org failed")

    h = []
    t = []
    w = []
    for k in data.keys():
        h.append(float(data[k]["humidity"]))
        t.append(float(data[k]["temperature"]))
        w.append(float(data[k]["wind"]))

    internet_data_h_mean = np.mean(h)
    internet_data_t_mean = np.mean(t)
    internet_data_w_mean = np.mean(w)

    wa = requests.get("http://www.wetter.at/wetter/oesterreich/tirol/brixlegg")
    wa_temp = re.findall(r'"maxTemp">\s+(\d{1,2})', wa.text, re.MULTILINE)[0]
    wa_wind = re.findall(r'class="d">([\.\d]+)', wa.text)[0]
    wa_windrichtung = re.findall(r'class="d">.*km/h ([\w]{1,4})', wa.text)[0]
    wa_text = re.findall(r'class="s">(.*)</div>', wa.text)[0].capitalize()
    wa_niederschlag = re.findall(r'(\d+) mm/h', wa.text)[0]
    wa_sunup = re.findall(r'sunUp">(\d{1,2}:\d{1})', wa.text)[0] + "0"
    wa_sundown = re.findall(r'sunDown">(\d{1,2}:\d{1})', wa.text)[0] + "0"

    out_h = int(internet_data_h_mean)
    out_w = round(np.mean([internet_data_w_mean, float(wa_wind)]), 1)
    out_t = round(np.mean([float(wa_temp), internet_data_t_mean]), 1)

    if debug:
        print("====== wetter.at ====")
        print("Temperatur: %s" % wa_temp)
        print("Windstaekre: %s" % wa_wind)
        print("######## gelogte dateien  #############")
        print("Temperatur: %s°" % out_t)
        print("Windstaekre: %s km/h" % out_w)
        print("Windrichtung: %s" % wa_windrichtung)
        print("Humidity: %s%%" % out_h)
        print("Text: %s" % wa_text)
        print("Niederschlag: %s mm/h" % wa_niederschlag)
        print("Sonnenaufgang: %s" % wa_sunup)
        print("Sonnenuntergang: %s" % wa_sundown)
    else:
        with transaction.manager:
            log = Log(temperature=out_t, humidity=out_h, wind_speed=out_w, wind_direction=wa_windrichtung, description=wa_text, rainfall=wa_niederschlag, sun_up=wa_sunup, sun_down=wa_sundown)
            DBSession.add(log)