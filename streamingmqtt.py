#!/usr/bin/env python
import os, json, StringIO, threading
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import paho.mqtt.client as mosquitto
import settings

import json
import os
import sys
import time

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        print(data)
        return(True)

    def on_error(self, status):
        print(status)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("$SYS/#")

class MQTTListener(StreamListener):
    def __init__(self, client):
        self.client = client
	self.buffer =""
	print "Listener constructed"

    def on_data(self, data):
	# print "Received data"
	decoded = json.loads(data)
        self.buffer += decoded['text']
        if data.endswith("\r\n") and self.buffer.strip():
           self.client.publish(settings.MQTT_TOPIC,self.buffer)
        self.buffer = ""
        return(True)

    def on_error(self, status):
        print status


client = mosquitto.Mosquitto() 
client.on_connect = on_connect
client.connect(settings.MQTT_HOST,settings.MQTT_PORT, 60)
l = MQTTListener(client)
#l = StdOutListener()
auth = OAuthHandler(settings.key, settings.secret)
auth.set_access_token(settings.access_token, settings.access_token_secret)
stream = Stream(auth, l)
stream.filter(track=['Linux'], async=True)
print "Streaming Started"

# Wait - if parent dies, exit gracefully
while os.getppid() != 1 :
    time.sleep(1)

stream.disconnect()
print os.path.basename(__file__),": Parent exited"
sys.exit(1)

