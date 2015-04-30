#!/usr/bin/env pythondmport time
import plotly.plotly as py
import json
import time
import readadc
import datetime
import numpy as np
import RPi.GPIO as GPIO
#from array import array

with open('../conf/plotly.json') as config_file:
    plotly_user_config = json.load(config_file)

py.sign_in(plotly_user_config["username"], plotly_user_config["api_key"])

url = py.plot([
    {
        'x': [], 'y': [], 'type': 'scatter',
        'stream': {
            'token': plotly_user_config['stream_ids'][0],
            'maxpoints': 400
        }
    },
    {
        'x': [], 'y': [], 'type': 'scatter',
        'stream': {
            'token': plotly_user_config['stream_ids'][1],
            'maxpoints': 20
        }
    }
    ], filename='Raspberry Pi Streaming Example Values')

print "View your streaming graph here: ", url

# temperature sensor middle pin connected channel 0 of mcp3008
sensor_pin = 7
readadc.initialize()

stream = py.Stream(plotly_user_config['stream_ids'][0])
stream.open()
THRESH=512
bpmstream = py.Stream(plotly_user_config['stream_ids'][1])
bpmstream.open()
#pulse detection
pulse = False

bar = np.array([])
big = np.array([])
GPIO.setup(13, GPIO.OUT)

while True:
	sensor_data = readadc.readadc(sensor_pin,
                                  readadc.PINS.SPICLK,
                                  readadc.PINS.SPIMOSI,
                                  readadc.PINS.SPIMISO,
                                  readadc.PINS.SPICS)
	#print sensor_data	
#	draw the equivalent number of points in an attempt to draw a vertical pulse sensing graph
	for i in range(sensor_data / 100):
		print ".",
		#detect beats
	if (sensor_data > THRESH):
		if (pulse == False):
			pulse = True
			print "Beat"
			bar = np.append(bar,1)
		else:
			#print ""
			bar = np.append(bar,0)
	else:
		pulse = False
		#print ""
		bar = np.append(bar,0)
		#hang out and do nothing for a tenth of a second
	
    	stream.write({'x': datetime.datetime.now(), 'y': sensor_data/4})
	time.sleep(0.1)
	#every 3 seconds
	if (bar.shape[0] == 20):
		big = np.append(big, bar)
			
		if (big.shape[0] > 200):
			#foo = np.sum(big)*3
			#print "BEFORE========================================================"
			#print big.shape
 			big = np.delete(big,[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19])
			#print "AFTER========================================================"
			#print big.shape
			bpm = np.sum(big*3)
			print bpm
			#print "BPM <3 <3 <3 <3 <3" + bpm.to_s
    			bpmstream.write({'x': datetime.datetime.now(), 'y': bpm})
			if (bpm > 90):
				GPIO.output(13, True)
			else:
				GPIO.output(13, False)
	
		bar = [ ]
		




		


