__author__ = "Tulio Dias"
__copyright__ = "Copyright 2019, Inatel Competence Center"
__credits__ = "Inatel"
__license__ = "MIT"
__maintainer__ = "Tulio Dias"
__email__ = "tuliodias@inatel.br"

import paho.mqtt.client as mqtt
import time
import datetime
import json
import requests
import os
import logging
from pymongo import MongoClient

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logging.warning('MQTT Client-Python started')
time.sleep(3)
mongo_client = MongoClient('mongodb://mongo:27017/')

BD = mongo_client['db']
messages_collection = BD['messages']

def on_connect(client, userdata, flags, rc):
    client.subscribe("#")
    logging.warning("Topic # - Connected" )

def on_message(client, userdata, msg):
    global messages_collection
    topico = str(msg.topic)
    mensagem = str(msg.payload)
    logging.warning(topico + ":" + mensagem)
    message_data = {"topic":topico,"message":mensagem,"datetime":datetime.datetime.now()}
    logging.warning( messages_collection.insert_one(message_data).inserted_id )

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

for i in range(20):
    try:
        client.connect("mosca", 1883, 60)
        break
    except:
        logging.warning('Connection failed.. Trying again')
        time.sleep(5)

logging.warning('MQTT Connected!')
client.loop_forever()

