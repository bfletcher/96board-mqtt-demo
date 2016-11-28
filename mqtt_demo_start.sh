#!/bin/bash
# Demo start  
# this configuration assuming client and broker are local
#
#

#* Start Local LCD display service
#* emulates an LCD output in a gtk window
python lcd_service.py &

#* Start MQTT broker
echo "starting broker"
sudo mosquitto -c /etc/mosquitto/mosquitto.conf &

#* Start customised Subscriber (please note for remote client, configure the host IP address in settings.py)
#* Modified subscriber.py, on_message method to route output to emulated LCD display over rpyc
#* Wait for the LCD display to come on line (polling the socket would be cleaner ...)
sleep 5
echo "starting lcd subscriber"
python lcdsubscriber.py &

#* Start twitter streaming service and Publisher
echo "starting twitter service"
python streamingmqtt.py &

#* Child processes started above should check this parent is still alive
while true; do
    sleep 1
done



