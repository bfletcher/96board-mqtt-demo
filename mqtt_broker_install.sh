#!/bin/bash
#Broker install
#Step 1 and 2 are needed on both client and broker
#
#
#Step 1 - Preparing the build system
sudo apt-get update
sudo apt-get install build-essential python quilt devscripts python-setuptools python3
sudo apt-get install libssl-dev
sudo apt-get install cmake
sudo apt-get install libc-ares-dev
sudo apt-get install uuid-dev
sudo apt-get install daemon
#
#
#Step 2 - Getting mosquitto source package
wget http://mosquitto.org/files/source/mosquitto-1.4.3.tar.gz
tar zxvf mosquitto-1.4.3.tar.gz
cd mosquitto-1.4.3
make
sudo make install
sudo cp mosquitto.conf /etc/mosquitto

