#!/bin/bash
#
#Step 3 (Broker) - Kick off broker
#Retrieve broker IP address
#sudo /sbin/ifconfig
sudo mosquitto -c /etc/mosquitto/mosquitto.conf
#
#
#Step 3 (Subscriber) - Subscribe to topic on selected broker
#$ sudo /sbin/ldconfig
#$ mosquitto_sub -h [broker IP address] -t [topic]
#
#
#Step 3 (Publisher) - Publish topic on selected broker
#$ sudo /sbin/ldconfig
#$ mosquitto_pub -h [broker IP address] -t [topic] -m [“message”]
#
#
#Step 4 Tweepy - Install Tweepy API to access real time twitter feed
#$ git clone git://github.com/tweepy/tweepy.git
#$ cd tweepy
#$ python setup.py install
#
#
#Step 5 paho MQTT python bindings
#$ git clone git://git.eclipse.org/gitroot/paho/org.eclipse.paho.mqtt.python.git
#$ cd org.eclipse.paho.mqtt.python
#$ python setup.py install
#
#
#
#
#Step 6 Demo
#* Start MQTT broker
#   * sudo mosquitto -c /etc/mosquitto/mosquitto.conf
#* Find out broker device IP address to be used below
#* Start MQTT standard client subscriber
#   * mosquitto_sub -h [broker IP address] -t twitter/96Boards
#* Start customised Client (please note for remote client, configure the host IP address in settings.py)
#   * Python subscriber.py
#* To print out to LCD display, modify subscriber.py, on_message method
#* Start twitter streaming service and publisher
#   * Python streamingmqtt.py
