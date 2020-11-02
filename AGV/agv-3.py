import paho.mqtt.client as mqtt
from os import system
import multiprocessing
import keyring as kr
import datetime
import logging
import random
import time

class AGV(object):
    def __init__(self, location=(0.0,0.0,0), status=('ON')):
        mqtt.Client.__init__(self)
        self.battery   = 100
        self.location  = location
        self.node_list = [(1,1,1)]
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

    def subscribe_to_topics(self, client, broker_address, port):
        try:
            client.connect(broker_address, port)
            client.subscribe([('AGVs/AGV3/node_list', 1),\
                          ('AGVs/AGV3/emergency', 1)])
            # self.subscribe([('AGVs/+/node_list', 1),\
            # ('AGVs/+/emergency', 1)]) # To test Authorization
        except Exception as e:
            self.logger.warning(e)

    def publish_to_topics(self, client, broker_address, port):
        try:
            topic_list = ['AGVs/AGV3/location', 'AGVs/AGV3/status', 'AGVs/AGV3/battery']
            random_topic = random.choice(topic_list)

            if random_topic == 'AGVs/AGV3/location':
                self.location = random.choice(self.node_list)
                random_value  = self.location 
            elif random_topic == 'AGVs/AGV3/status':
                random_value  = random.choice(['Online','Offline','Stopped','Manual']) 
            elif random_topic == 'AGVs/AGV3/battery':
                random_value  = random.randint(0, 100) 

            client.publish(random_topic, str(random_value), qos=0)
        except Exception as e:
            self.logger.warning(e)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        userdata['myobject'].logger.info('CONNECTED TO BROKER.')
    elif rc == 5:
        userdata['myobject'].logger.error('AUTHENTICATION FAILED.')
    
def on_subscribe(client, userdata, mid, granted_qos):
    userdata['myobject'].logger.info('SUBSCRIBED SUCCESSFULLY')

def on_message(client, userdata, msg):
    userdata['myobject'].logger.info('RECEIVED MESSAGE FROM '+ msg.topic)
    received_top = msg.topic[11:]

    if received_top == 'node_list':
        userdata['myobject'].node_list = eval(msg.payload.decode("utf-8"))
    elif received_top == 'emergency':
        userdata['myobject'].emergency = eval(msg.payload.decode("utf-8"))

def on_publish(client, userdata, mid):
    userdata['myobject'].logger.info('DATA PUBLISHED SUCCESSFULLY')

def on_disconnect(client, userdata, rc):
    userdata['myobject'].logger.info('DISCONNECTED FROM BROKER.')
    client.loop_stop()

if __name__ == '__main__':
    broker_address = '192.168.1.115'
    port  = 1883
    user = 'AGV3'
    try:
        passwd = kr.get_password('ICS', user)
    except ValueError:
        print('INCORRECT PASSWORD...EXITTING...')
        exit()

    agv_3 = AGV()
    agv_3.initiate_logger()

    client_sub_userdata = {'myobject':agv_3}
    client_pub_userdata = {'myobject':agv_3}
    client_sub = mqtt.Client(userdata=client_sub_userdata)
    client_pub = mqtt.Client(userdata=client_pub_userdata)
    
    client_sub.on_connect   = on_connect
    client_pub.on_connect   = on_connect
    client_sub.on_subscribe = on_subscribe
    client_pub.on_subscribe = on_subscribe
    client_sub.on_message   = on_message
    client_pub.on_message   = on_message
    client_sub.on_publish   = on_publish
    client_pub.on_publish   = on_publish

    client_sub.username_pw_set(username=user, password=passwd)
    client_pub.username_pw_set(username=user, password=passwd)
    
    try:
        agv_3.subscribe_to_topics(client_sub, broker_address, port)
        client_pub.connect(broker_address, port)

        while True:
            agv_3.publish_to_topics(client_pub, broker_address, port)
            client_sub.loop_start()
            client_pub.loop_start()
            time.sleep(3)

    except KeyboardInterrupt:
        client_sub.disconnect()
        client_pub.disconnect()
