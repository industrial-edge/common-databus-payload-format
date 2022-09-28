# Custom Connector Application

# This file is part of the common databus payload format repository.
# https://github.com/industrial-edge/common-databus-payload-format
#
# Copyright (c) 2022 Siemens Aktiengesellschaft
#
# This file is subject to the terms and conditions of the MIT License.  
# See LICENSE file in the top-level directory

import paho.mqtt.client as mqtt     # mqtt client for interacting with the databus
import os                           # interaction with operating system (e.g. read file)
import json                         # storing and exchanging data via JSON file
import datetime

APP_NAME = "Custom Connector"
CONFIG_FILE = '/cfg-data/config.json'
MQTT_BROKER = 'ie-databus'

global MQTT_USER
global MQTT_PASSWORD
global MQTT_METADATA_TOPIC
global MQTT_DATA_READ_TOPIC
global MQTT_DATA_WRITE_TOPIC
global MQTT_STATUS_TOPIC
global METADATA_JSON
global STATUS_JSON

MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_METADATA_TOPIC = ""
MQTT_DATA_READ_TOPIC = ""
MQTT_DATA_WRITE_TOPIC = ""
MQTT_STATUS_TOPIC = ""

#============================
# Reading Configuration
#============================

def read_parameter(jsonfile):
    
    print(f'> Read params from {jsonfile}')
    
    with open(jsonfile) as params:
        data = json.load(params)
        return data

def publish_metadata(client):
        meta_json_string = json.dumps(METADATA_JSON)
        pub = client.publish(MQTT_METADATA_TOPIC, meta_json_string)
        #print(f"> Published metadata on topic = {MQTT_METADATA_TOPIC} with result = {pub}")

def publish_statusdata(client):
        status_json_string = json.dumps(STATUS_JSON)
        pub = client.publish(MQTT_STATUS_TOPIC, status_json_string)
        #print(f"> Published status data on topic = {MQTT_STATUS_TOPIC} with result = {pub}")
#============================
# Callback functions
#============================

#as soon as the client connects successfully, it listens if new data is coming in the custom connector
def on_connect(client, userdata, flags, rc):       
    if rc == 0: # 0 = connection successful 
        print(f"> {APP_NAME} connected successfully")
        client.connected_flag = True
        
        # Publish Metadata
        publish_metadata(client)
        
        # Publish status data
        publish_statusdata(client)
        
    else:
        print("Connection failed!1")
        return

def on_disconnect(client, userdata, rc):
    print(f"{APP_NAME} is disconnected")
    client.connected_flag = False
    
    print("END of LOOP")
    client.loop_stop() 

def on_message(client, userdata, message):
    print(f"Recieved message = {message.payload} on topic = {message.topic}")
 
    # If data is coming in on write topic, write this data on output topic (data read topic)
    if message.topic == MQTT_DATA_WRITE_TOPIC: 
    
        # write input data on dedicated topic (data read topic)
        client.publish(MQTT_DATA_READ_TOPIC, message.payload)
        print("Data is written")
    
    # ignore all other topics
    else:
        return
    
    
#============================
# Main function
#============================

print("\n\nStarting custom connector application")
print("-------------------------------------")

# Read config file if existing
try:
    print("\n\n1. Read configuration file")
    params = read_parameter(CONFIG_FILE)
    MQTT_USER = params['MQTT_USER']
    MQTT_PASSWORD = params['MQTT_PASSWORD']
    MQTT_METADATA_TOPIC = params['MQTT_METADATA_TOPIC']
    MQTT_DATA_READ_TOPIC = params['MQTT_DATA_READ_TOPIC']
    MQTT_DATA_WRITE_TOPIC = params['MQTT_DATA_WRITE_TOPIC']
    MQTT_STATUS_TOPIC = params['MQTT_STATUS_TOPIC']

# If no config file exists, configure with default values
except:
    print("> Warning: no config file available! Using default values...")
    MQTT_USER = 'edge'
    MQTT_PASSWORD = 'edge'
    MQTT_METADATA_TOPIC = 'ie/m/j/simatic/v1/custom1/dp'
    MQTT_DATA_READ_TOPIC = 'ie/d/j/simatic/v1/custom1/dp/r/connection1/collection1'
    MQTT_DATA_WRITE_TOPIC = 'ie/d/j/simatic/v1/custom1/dp/w/connection1/collection1'
    MQTT_STATUS_TOPIC = 'ie/s/j/simatic/v1/custom1/status'

print(f"> MQTT_USER = {MQTT_USER}")
print(f"> MQTT_PASSWORD = {MQTT_PASSWORD}")
print(f"> MQTT_METADATA_TOPIC = {MQTT_METADATA_TOPIC}")
print(f"> MQTT_DATA_READ_TOPIC = {MQTT_DATA_READ_TOPIC}")
print(f"> MQTT_DATA_WRITE_TOPIC = {MQTT_DATA_WRITE_TOPIC}")
print(f"> MQTT_STATUS_TOPIC = {MQTT_STATUS_TOPIC}")


# Create metadata fix setting)
# ----------------------------
print("\n\n2. Create metadata")

# Metadata JSON (fix definition)
METADATA_JSON = {
    "seq":1,
    "hashVersion":123456789,
	"applicationName":"Custom Connector V1.0",
	"statustopic":MQTT_STATUS_TOPIC,
    "connections":
    [
        {
            "name":"Connection_1",
            "type":"simulated",
            "dataPoints":
            [
                {
                    "name":"Collection_1",
                    "topic":MQTT_DATA_READ_TOPIC,
                    "pubTopic":MQTT_DATA_WRITE_TOPIC,
                    "publishType":"bulk",
                    "dataPointDefinitions":
                    [
                        {
                            "name":"Datapoint_Bool",
                            "id":"101",
                            "dataType":"Bool"
                        },
                        {
                            "name":"Datapoint_Int",
                            "id":"102",
                            "dataType":"Int"
                        },
                        {
                            "name":"Datapoint_Real",
                            "id":"103",
                            "dataType":"Real"
                        }
                    ]
                }
            ]
        }
    ]
}

print(f"{METADATA_JSON}")

meta_json_string = json.dumps(METADATA_JSON)

# Create status data (fix setting)
# -------------------------------
print("\n\n3. Create status data")

# Metadata JSON (fix definition)
STATUS_JSON = {
    "seq":1,
    "ts":str(datetime.datetime.now()),
    "connector":{"status": "good"},
    "connections":
    [
        {"name": "Connection_1", "status": "good"}
    ]
}
    
print(f"{STATUS_JSON}")

# Configure MQTT client
# ---------------------

print("\n\n4. Configure MQTT client")

client = mqtt.Client(client_id = APP_NAME)

#set username and password, must be created it databus configurator
client.username_pw_set(MQTT_USER,MQTT_PASSWORD)

#add callback functions
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# Start client
# ------------
print("\n\n5. Start MQTT client")
client.connect(MQTT_BROKER)

# subscribe to write data topic and listen, if data is written
ret2 = client.subscribe(MQTT_DATA_WRITE_TOPIC)
print(f"Subscribed to write topic ({MQTT_DATA_WRITE_TOPIC}) with result = {ret2}")


# MQTT loop
# ---------

# starts a loop in another thread and lets the main thread continue to do other things
# loop_stop() is places in function "on_disconnect"
client.loop_start()

# MAIN thread
# -----------
print("Publish metadata and status every 5 seconds")
lastTime = datetime.datetime.now()
        
while True:
    
    if ((datetime.datetime.now() - lastTime) < datetime.timedelta(seconds=5)):
        # wait and do nothing
        wait = True
    
    else:
        lastTime = datetime.datetime.now()
        
        # Publish Metadata
        publish_metadata(client)
        
        # Publish Status Data
        publish_statusdata(client)
