from datetime import date, datetime,timedelta
import math
from sqlite3 import Date
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import time

# 当前日期
now_date = time.strftime("%Y-%m-%d", time.localtime())

# 当前时间的年月日
year = datetime.now().year
month = datetime.now().month
day = datetime.now().day

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']
birthday_m = os.environ['BIRTHDAY_M']


app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  weather_two = res['data']['list'][1]
  weather_three = res['data']['list'][2]
  return weather['weather'], math.floor(weather['temp']), weather['wind'], weather['humidity'], weather_two['weather'], weather_three['weather']

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_birthday_m():
  next_m = datetime.strptime(str(date.today().year) + "-" + birthday_m, "%Y-%m-%d")
  if next_m < datetime.now():
    next_m = next_m.replace(year=next_m.year + 1)
  return (next_m - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature, wind_speed, humidity, tomorrow, after_tomorrow = get_weather()
data = {"year":{"value":year, "color": "#2177b8"},"month":{"value":month, "color": "#2177b8"},"day":{"value":day, "color": "#2177b8"}, "city":{"value":city, "color": "#2177b8"},"weather":{"value":wea, "color":"#a61b29"},"temperature":{"value":temperature, "color":"#12aa9c"},"wind_speed":{"value":wind_speed, "color":"#12aa9c"},"humidity":{"value":humidity, "color":"#12aa9c"},"tomorrow":{"value": tomorrow, "color":"#feba07"},"after_tomorrow":{"value": after_tomorrow, "color":"#feba07"},"love_days":{"value":get_count(), "color":"#f03752"},"birthday_left":{"value":get_birthday(), "color":"#eba0b3"},"birthday_right":{"value":get_birthday_m(), "color":"#eba0b3"}}
res = wm.send_template(user_id, template_id, data)
print(res)
