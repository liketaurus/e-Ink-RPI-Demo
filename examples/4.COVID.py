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
    logging.info("COVID'19 Stats Demo")
    
    epd = epd2in13_V2.EPD()
    logging.info("1. Init and Clear...")
    epd.init(epd.FULL_UPDATE)
    
    # Fonts
    font13 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 13)
    font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)    
    # unicode font
    font=ImageFont.truetype("/usr/share/fonts/truetype/lato/Lato-Medium.ttf",16)
    
    logging.info("2. Start gathereing COVID data")   
    COVIDresponse = requests.get("https://api.covid19api.com/live/country/ukraine/status/confirmed")    
    COVIDdata = list(COVIDresponse.json())
    # print(COVIDdata)
    
    i = len(COVIDdata)-1
    Confirmed = COVIDdata[i]["Confirmed"]    
    Deaths = COVIDdata[i]["Deaths"]
    Recovered = COVIDdata[i]["Recovered"]
    Active = COVIDdata[i]["Active"]
    Date = COVIDdata[i]["Date"]
    
    logging.info("3. Show stats...")
    image = Image.new('1', (epd.height, epd.width), 255)  
    draw = ImageDraw.Draw(image)
          
    draw.text((0, 1), "COVID'19 in Ukraine: "+str(Date)[0:10], font = font)    
    draw.text((0, 23), "Confirmed: "+str(Confirmed),font = font)
    draw.text((0, 55), "Deaths: " + str(Deaths),font = font15, fill = 0)
    draw.text((0, 70), "Active: "+str(Active) ,font = font15, fill = 0)
    draw.text((0, 85), "Recovered: "+str(Recovered),font = font15, fill = 0)
    
    # read bmp file 
    logging.info("4. Read BMP file...")
    img = Image.open(os.path.join(picdir, 'COVID-icon.bmp'))
    image.paste(img, (145, 20)) 
    
    epd.display(epd.getbuffer(image))
    time.sleep(2)
            
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()
