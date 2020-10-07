import paho.mqtt.client as mqtt
from os import system
import datetime
import logging
import time

class AGV(mqtt.Client):
    def __init__(self, location=(0.0,0.0,0), status=('ON')):
        mqtt.Client.__init__(self)
        self.battery   = 100
        self.location  = location
        self.status    = status
        self.emergency = 0

    def initiate_logger(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        # create console handler and set level to debug

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter\
        ('%(asctime)s [%(levelname)s] %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        self.logger.addHandler(ch)

    def subscribe_to_topics(self):
        try:
            self.subscribe([('AGVs/AGV_3/node_list', 1),\
                          ('AGVs/AGV_3/emergency', 1)])
            # self.subscribe([('AGVs/+/node_list', 1),\
            # ('AGVs/+/emergency', 1)]) # To test Authorization
        except:
            pass

    def publish_to_topics(self):
        try:
            self.subscribe([('AGVs/AGV_3/node_list', 1),\
                          ('AGVs/AGV_3/emergency', 1)])
            # self.subscribe([('AGVs/+/node_list', 1),\
            # ('AGVs/+/emergency', 1)]) # To test Authorization
        except:
            pass

def on_connect(client, userdata, flags, rc):
    agv_3.logger.info('CONNECTED TO BROKER.')
    agv_3.subscribe_to_topics()

def on_subscribe(client, userdata, mid, granted_qos):
    agv_3.logger.info('SUBSCRIBED SUCCESSFULLY')

def on_message(client, userdata, msg):
    agv_3.logger.info('RECEIVED MESSAGE FROM '+ msg.topic)
    received_top = msg.topic[11:]

    if received_top == 'node_list':
        agv_3.node_list = eval(msg.payload.decode("utf-8"))
        print(agv_3.node_list)
    elif received_top == 'emergency':
        agv_3.emergency = eval(msg.payload.decode("utf-8"))
        print(agv_3.emergency)

def on_publish(client, userdata, mid):
    agv_3.logger.info('DATA PUBLISHED SUCCESSFULLY')

if __name__ == '__main__':
    broker_address = '192.168.1.115'
    port  = 1883
    agv_3 = AGV()
    agv_3.initiate_logger()
    
    agv_3.on_connect   = on_connect
    agv_3.on_subscribe = on_subscribe
    agv_3.on_message = on_message
    agv_3.on_publish = on_publish
    
    try:
        agv_3.connect(broker_address, port)
        agv_3.loop_forever()

        # Start publishing on parallel so navigation processes can run separately:
    except KeyboardInterrupt:
        agv_3.disconnect()
        agv_3.logger.info('DISCONNECTED FROM BROKER.')
