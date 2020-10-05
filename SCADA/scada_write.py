import paho.mqtt.client as mqtt
from colorama import Fore, Back, Style
from os import system
import datetime
import time

def on_publish(client, userdata, mid):
    print('Data Published Successfully.')

def validate_agv(agv_no=0):
    while agv_no == 0:
        try:
            agv_no = int(input('Enter an integer for the AGV number:\n'))
        except ValueError:
            print(Fore.BLACK + Back.RED + 'Input must be a number from 1 - 3')
            print(Style.RESET_ALL,'\n')
            agv_no = 0
        if agv_no < 1 or agv_no > 3:
            print(Fore.BLACK + Back.RED + 'Input must be a number from 1 - 3')
            print(Style.RESET_ALL, '\n')
            agv_no = 0
    return agv_no

def validate_node_list(node_list=0):
    while node_list == 0:
        node_list = eval(input('Enter a list of locations. Each location '+\
        'must be a tuple of 3 dimensions x, y, and 0-2 for\n "Pick", "Place'+\
        ', or "Charge" e.g.: "[(45, 12, 0), (60, 10, 1), (50, -15, 2), (30, 15, 0)]"'\
        +'\n\n'))
        if type(node_list) is not list:
            print(Fore.BLACK + Back.RED +\
            'Input must be a list of tuples with length of 3 each')
            print(Style.RESET_ALL, '\n')
            node_list = 0
        else:
            for tup in node_list:
                if type(tup) is not tuple or len(tup) != 3:
                    print(Fore.BLACK + Back.RED\
                    + 'Input must be a list of tuples with length of 3 each')
                    print(Style.RESET_ALL, '\n')
                    node_list = 0
                elif tup[2] < 0 or tup[2] > 2:
                    print(Fore.BLACK + Back.RED +\
                    'Tuple 3rd element Must be from 0 - 2')
                    print(Style.RESET_ALL, '\n')
                    node_list = 0
    return node_list

if __name__ == '__main__':
    broker_address = '192.168.1.115'
    port = 1883
    client = mqtt.Client()
    client.on_publish = on_publish
    client.connect(broker_address, port)
    system('clear')

    print(Fore.BLACK + Back.GREEN + \
    '{:^100s}'.format('ICS REALTIME CONTROL SYSTEM -- version 1.0'))
    print(Style.RESET_ALL)
    print(datetime.datetime.now(), end ='\n\n')
   
    while True:
        try:
            response = int(input('Please select a number from the following list:\n \
                                    (1) Emergency stop\n \
                                    (2) Manual Override\n \
                                    (3) Restore Autonomy\n \
                                    (4) Assign node list\n \
                                    (5) Quit\n'))
        except ValueError:
            response = 0
        except KeyboardInterrupt:
            client.disconnect()
            break
        if response < 1 or response > 5:
            print(Fore.BLACK + Back.RED + 'Input must be a number from 1 - 5')
            print(Style.RESET_ALL, '\n')
        elif response == 1:
            agv_no = validate_agv()
            client.publish('AGVs/AGV_'+str(agv_no)+'/emergency', payload=1,\
                            qos=1, retain=False)
            # send an Emergency stop signal to the corresponding topic
        elif response == 2:
            agv_no = validate_agv()
            client.publish('AGVs/AGV_'+str(agv_no)+'/emergency', payload=2,\
                            qos=1, retain=False)
            # send a Manual Override signal to the corresponding topic
        elif response == 3:
            agv_no = validate_agv()
            client.publish('AGVs/AGV_'+str(agv_no)+'/emergency', payload=0,\
                            qos=1, retain=False)
            # clear the Manual Override from the corresponding topic
        elif response == 4:
            agv_no = validate_agv()
            node_list = validate_node_list()
            res = client.publish('AGVs/AGV_'+str(agv_no)+'/node_list', payload=str(node_list),\
                            qos=1, retain=False)   # str used since Payload CANNOT be a list.             
        elif response == 5:
            client.disconnect()
            break
