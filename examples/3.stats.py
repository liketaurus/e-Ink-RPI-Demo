#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import time
import datetime
import subprocess
import requests 
from datetime import datetime
from datetime import date
from urllib.request import urlopen
from io import BytesIO


picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("Local Weather/Device Stats Demo")
    
    epd = epd2in13_V2.EPD()
    logging.info("1. Init and Clear...")
    epd.init(epd.FULL_UPDATE)
    
    
    # Fonts
    font12 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12)
    font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)    
    
    # unicode font
    font=ImageFont.truetype("/usr/share/fonts/truetype/lato/Lato-Medium.ttf",14)
    
    # Stats
    logging.info("2. Start gathereing stats...")    
    IP = subprocess.check_output(['hostname', '-I']).decode('ascii')
    cpu = subprocess.check_output("cat /proc/loadavg", shell = True).decode('ascii')
    cpu_n=subprocess.check_output("nproc", shell = True).decode('ascii')
    CPU = '{:.0f}%'.format( float(cpu.split()[0]) / float(cpu_n)*100 ) # subprocess.check_output(cmd, shell = True).decode('ascii')
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB, %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell = True ).decode('ascii')
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk usage: %d/%dGB, %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell = True ).decode('ascii')
    
    # Date and time
    today = date.today()
    now = datetime.now()
    d1 = today.strftime("%A, %B %d, %Y")
    d2=now.strftime("%H:%M:%S")
    Date=d1+", "+d2
    
    # Weather
    logging.info("3. Getting local weather...") 
    response = requests.get("http://api.weatherstack.com/current?access_key=19c7d0285e94d11603416456eb292d64&query=Poltava")    
    data = response.json()
    desc = data["current"]["weather_descriptions"][0]
    temp = data["current"]["temperature"]
    picWeather = data["current"]["weather_icons"][0]   
    celcius = chr(176)+ "C"
        
    Picresponse = requests.get(picWeather)
    img = Image.open(BytesIO(Picresponse.content))
    
    
    logging.info("4. Show stats/weather...")
    image = Image.new('1', (epd.height, epd.width), 255)  
    draw = ImageDraw.Draw(image)
          
    draw.text((0, 1), Date, font = font)
    draw.text((0, 20), "Weather: "+desc+", "+str(temp)+celcius,font = font)
    draw.text((0, 50), "IP: " + str(IP),font=font)
    draw.text((0, 65), "CPU load: "+str(CPU) ,font = font12, fill = 0)
    draw.text((0, 80), str(MemUsage),font = font12, fill = 0)
    draw.text((0, 95), str(Disk),font = font12, fill = 0)
    
    image.paste(img, (180, 50)) 
    
    epd.display(epd.getbuffer(image))
    time.sleep(2)    
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()
