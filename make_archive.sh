#!/bin/bash 
# copy files into a command-line specified directory $1
mkdir $1
cp lcd_chars.txt $1
cp lcd_client.py $1
cp lcd_service.py $1
cp lcdsubscriber.py $1
cp make_archive.sh $1
cp mqtt_broker_install.sh $1
cp mqtt_broker_start.sh $1
cp mqtt_client_install.sh $1
cp mqtt_demo_start.sh $1
cp mqtt_install.sh $1
cp settings.py $1
cp streamingmqtt.py $1
cp subscriber.py $1
cp mqtt_demo.readme $1

tar cvfz archive.taz $1 
