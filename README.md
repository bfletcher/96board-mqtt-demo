# 96board-mqtt-demo
MQTT publisher/subscriber demo using tweepy on a CE-edition 96board

Introduction:

Demonstrates the use of mosquitto as a broker and paho as a client for MQTT
messages. MQTT messages are published (using a twitter feed as content). A
subscriber client subscribes to these MQTT messages and displays them on an
emulated lcd display.

A twitter stream is used as a source of MQTT messages streamingmqtt.py. Using
the paho mosquitto bindings, this python script sets up a client that publishes
MQTT messages.

lcdsubscriber.py, also using paho bindings, sets up an MQTT subscriber client.
For added sparkle, lcdsubscriber emulates an lcd matrix display. If you want
to see messages on stdout, set Debug in lcdsubscriber.py to True.

Setup:

Based on Debian. Tested on a DB410c with build #144 installed from SD card.

# install the relevant packages
$ ./mqtt_broker_install.sh
$ ./mqtt_client_install.sh

# As configured, the broker and client are on the same host

# add your user name to /etc/mosquitto/mosquitto.conf (e.g. user linaro)
$ sudo vi /etc/mosquitto/mosquitto.conf

# script to start the demo after installation
$ ./mqtt_demo_start.sh

# Creates the lcd display window and shows the tweets from the tweepy
# filter received from subscribing to MQTT

Files:

mqtt_broker_install.sh - script that installs the MQTT broker
mqtt_client_install.sh - script that installs the MQTT client
mqtt_demo.readme - this file
mqtt_demo_start.sh - script to start the demo after installation
settings.py - settings, including OAuth token for tweepy to access twitter apis
streamingmqtt.py - sets up a tweepy stream that publishes filter results to MQTT
lcdsubscriber.py - an MQTT subscriber that outputs to the lcd over rpyc
subscriber.py - a simple subscriber without the lcd emulation
lcd_chars.txt - defines the character set for the lcd matrix display
lcd_client.py - a simple test client for the lcd display (not used in the demo)
lcd_service.py - a service accessed by rpyc that emulates an lcd display in gtk

(c) Linaro 2016

