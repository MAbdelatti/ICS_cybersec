import paho.mqtt.client as mqtt
from colorama import Fore, Back, Style
from os import system
import datetime
import time

class AGV(object):
    def __init__(self, location=(0.0,0.0,0.0), status=('OFF')):
        self.battery  = 100
        self.location = location
        self.status   =   status

def assign_values(msg):
    ID = msg.topic[9]
    received_top = msg.topic[11:]

    if ID == '1' and received_top == 'location':
        agv1.location = eval(msg.payload.decode("utf-8"))
    elif ID == '1' and received_top == 'status':
        agv1.status = msg.payload.decode("utf-8")
    elif ID == '1' and received_top == 'battery':
        agv1.battery = int(msg.payload.decode("utf-8"))
    elif ID == '2' and received_top == 'location':
        agv2.location = eval(msg.payload.decode("utf-8"))
    elif ID == '2' and received_top == 'status':
        agv2.status = msg.payload.decode("utf-8")
    elif ID == '2' and received_top == 'battery':
        agv2.battery = int(msg.payload.decode("utf-8"))   
    if ID == '3' and received_top == 'location':
        agv3.location = eval(msg.payload.decode("utf-8"))
    elif ID == '3' and received_top == 'status':
        agv3.status = msg.payload.decode("utf-8")
    elif ID == '3' and received_top == 'battery':
        agv3.battery = int(msg.payload.decode("utf-8"))

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    global conn_status
    conn_status = 'connected.'
    system('clear')
    print(Fore.BLACK + Back.GREEN + '{:^100s}'.format('ICS REALTIME MONITORING SYSTEM -- version 1.0'))
    print(Style.RESET_ALL)
    print(datetime.datetime.now())
    print('Status: ', Fore.BLACK + Back.GREEN + '{}'.format(conn_status))
    print(Style.RESET_ALL)
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe([('AGVs/+/location', 0), ('AGVs/+/status', 0), ('AGVs/+/battery', 0)])

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    assign_values(msg)
    system('clear')
    print(Fore.BLACK + Back.GREEN + '{:^100s}'.format('ICS REALTIME MONITORING SYSTEM -- version 1.0'))
    print(Style.RESET_ALL)
    print(datetime.datetime.now())
    print('Status: ', Fore.BLACK + Back.GREEN + '{}'.format(conn_status))
    print(Style.RESET_ALL)

    print('+============+=============+=============+============+')
    print('|            |    AGV#1    |    AGV#2    |    AGV#3   |')
    print('+============+=============+=============+============+')
    print('| Status     |','{:^11s}'.format(str(agv1.status)),\
                       '|','{:^11s}'.format(str(agv2.status)),\
                       '|','{:^10s}'.format(str(agv3.status)),'|')

    print('| Battery    |','{:^11s}'.format(str(agv1.battery)),\
                       '|','{:^11s}'.format(str(agv2.battery)),\
                       '|','{:^10s}'.format(str(agv3.battery)),'|')
    
    print('| Location X |','{:^11s}'.format(str(agv1.location[0])),\
                       '|','{:^11s}'.format(str(agv2.location[0])),\
                       '|','{:^10s}'.format(str(agv3.location[0])),'|')

    print('| Location Y |','{:^11s}'.format(str(agv1.location[1])),\
                       '|','{:^11s}'.format(str(agv2.location[1])),\
                       '|','{:^10s}'.format(str(agv3.location[1])),'|')

    print('| Task       |','{:^11s}'.format(str(agv1.location[2])),\
                       '|','{:^11s}'.format(str(agv2.location[2])),\
                       '|','{:^10s}'.format(str(agv3.location[2])),'|')
    print('+============+=============+=============+============+')


if __name__ == '__main__':
    broker_address = '192.168.1.115'
    agv1 = AGV()
    agv2 = AGV((100, 70, 1), 'ON')
    agv3 = AGV((-90, 15, 2), 'ON')    
    
    try:
        conn_status = 'disconnected.'
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect(broker_address, 1883, 60)
        client.loop_forever()
    except KeyboardInterrupt:
        client.disconnect
        conn_status = 'disconnected.'
        print('\nStatus:', Fore.BLACK + Back.RED + '{}'.format(conn_status))
        print(Style.RESET_ALL)
        print('Keyboard Interrupted')
