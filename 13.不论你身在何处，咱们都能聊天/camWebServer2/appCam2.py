#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  	appCam.py
#  	based on tutorial ==> https://blog.miguelgrinberg.com/post/video-streaming-with-flask
# 	PiCam Local Web Server with Flask
# MJRoBot.org 19Jan18

from flask import Flask, render_template, Response
app = Flask(__name__)


import time
from sakshat import SAKSHAT
from sakspins import SAKSPins as PINS

#Declare the SAKS Board

# get data from DHT sensor
def getDHTdata():		
	#DHT22Sensor = Adafruit_DHT.DHT22
	#DHTpin = 16
	#hum, temp = Adafruit_DHT.read_retry(DHT22Sensor, DHTpin)
	
	hum = 1
	temp = SAKS.ds18b20.temperature
	if hum is not None and temp is not None:
		hum = round(hum)
		temp = round(temp, 1)
	return temp, hum


@app.route("/")
def index():
	timeNow = time.asctime( time.localtime(time.time()) )
	temp, hum = getDHTdata()
	
	templateData = {
      'time': timeNow,
      'temp': temp,
      'hum'	: hum
	}
	return render_template('index.html', **templateData)

@app.route('/led_light')
def led_on():
	#点亮所有LED灯
	SAKS.ledrow.on()
	timeNow = time.asctime( time.localtime(time.time()) )
	temp, hum = getDHTdata()
	
	templateData = {
      'time': timeNow,
      'temp': temp,
      'hum'	: hum
	}
	return render_template('index.html', **templateData)

@app.route('/led_close')
def led_off():
	#点亮所有LED灯
	SAKS.ledrow.off()
	timeNow = time.asctime( time.localtime(time.time()) )
	temp, hum = getDHTdata()
	
	templateData = {
      'time': timeNow,
      'temp': temp,
      'hum'	: hum
	}
	return render_template('index.html', **templateData)

if __name__ == '__main__':
    SAKS = SAKSHAT()
    app.run(host='0.0.0.0', port =8080, debug=True, threaded=True)
