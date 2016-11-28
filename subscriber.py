#!/usr/bin/env python
import os, json, StringIO, threading
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import paho.mqtt.client as mosquitto
import settings

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

def on_message(client, userdata, msg):
    print("AA" + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_subscribe(client, userdata, flags, rc):
    print("Subscribed: " + str(flags) + " " + str(rc))

client = mosquitto.Client() 
client.on_subscribe = on_subscribe
client.on_connect = on_connect
client.on_message = on_message

client.connect(settings.MQTT_HOST,settings.MQTT_PORT, 60)
client.subscribe(settings.MQTT_TOPIC)
print "Subscriber:", settings
client.loop_forever()
