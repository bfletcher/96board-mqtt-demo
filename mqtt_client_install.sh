#!/bin/bash
# LOCAL Client install
#Step 1 and 2 are needed on both client and broker if they are different machines.
#
#
#Step 1 - Preparing the build system
#$ sudo apt-get update
#$ sudo apt-get install build-essential python quilt devscripts python-setuptools python3
#$ sudo apt-get install libssl-dev
#$ sudo apt-get install cmake
#$ sudo apt-get install libc-ares-dev
#$ sudo apt-get install uuid-dev
#$ sudo apt-get install daemon
#
#
#Step 2 - Getting mosquitto source package
#$ wget http://mosquitto.org/files/source/mosquitto-1.4.3.tar.gz
#$ tar zxvf mosquitto-1.4.3.tar.gz
#$ cd mosquitto-1.4.3
#$ make
#$ sudo make install
#$ sudo cp mosquitto.conf /etc/mosquitto
#
#
#Step 3 Tweepy - Install Tweepy API to access real time twitter feed
# because of problems reported with later verions, using 3.1.0
# Needs pip for the installation, and later version seems to have problems.
sudo easy_install pip==1.2.1
git clone https://github.com/tweepy/tweepy.git
cd tweepy
git checkout tags/v3.1.0
sudo python setup.py install
#
#
#Step 4 - paho MQTT python bindings
#
git clone https://github.com/eclipse/paho.mqtt.python.git
cd paho.mqtt.python
sudo python setup.py install
#
#Step 5 - Install some dependencies for the lcd display emulator
#
sudo pip install --upgrade rpyc
sudo apt-get install python-glade2

