import paho.mqtt.client as mqtt
from colorama import Fore, Back, Style
from os import system
import datetime
import time

#borker_address = "mqtt.eclipse.org" # Just for now
borker_address = '192.168.1.115' 

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    global conn_status
    conn_status = 'connected.'
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe([('AGVs/+/location', 0), ('AGVs/+/status', 0)])

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

    system('clear')
    print(Fore.BLACK + Back.GREEN + '{:^100s}'.format('ICS REALTIME MONITORING SYSTEM -- version 1.0'))
    print(Style.RESET_ALL)
    print(datetime.datetime.now())
    print('Status', conn_status)
    print('+============+=============+=============+============+')
    print('|            |    AGV#1    |    AGV#2    |    AGV#3   |')
    print('+============+=============+=============+============+')
    print('| Status     |','{:^11s}'.format('ON'),'|','{:^11s}'.format('OFF'),'|','{:^10s}'.format('ON'),'|')
    print('| Location X |','{:^11s}'.format('ON'),'|','{:^11s}'.format('OFF'),'|','{:^10s}'.format('ON'),'|')
    print('| Location Y |','{:^11s}'.format('ON'),'|','{:^11s}'.format('OFF'),'|','{:^10s}'.format('ON'),'|')
    #time.sleep(1)


if __name__ == '__main__':
    try:
        conn_status = 'disconnected.'
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect(borker_address, 1883, 60)
        client.loop_start()
    except KeyboardInterrupt:
        client.disconnect
        conn_status = 'disconnected.'
        print('\nStatus:', Fore.BLACK + Back.RED + '{}'.format(conn_status))
        print(Style.RESET_ALL)
        client.loop_stop()
        print('Keyboard Interrupted')