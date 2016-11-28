#!/usr/bin/env python
import os, json, StringIO, threading
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import paho.mqtt.client as mosquitto
import settings

import rpyc
import os
import time
import sys

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
    c.root.print_string(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_subscribe(client, userdata, flags, rc):
    print("Subscribed: " + str(flags) + " " + str(rc))



c = rpyc.connect("localhost", 18861)

client = mosquitto.Client() 
client.on_subscribe = on_subscribe
client.on_connect = on_connect
client.on_message = on_message

client.connect(settings.MQTT_HOST,settings.MQTT_PORT, 60)
client.subscribe(settings.MQTT_TOPIC)
print "Subscriber:", settings
#client.loop_forever()
client.loop_start()

# Wait - if parent dies, exit gracefully
while os.getppid() != 1 :
    time.sleep(1)

# Clean up
time.sleep(1)
# Send a string to the display service to unblock it and allow it to terminate gracefully too
c.root.print_string("Parent process exited") 
time.sleep(1)
client.loop_stop()
print os.path.basename(__file__),": Parent exited"
sys.exit(1)


