
# Custom Connector Application

# This file is part of the common databus payload format repository.
# https://github.com/industrial-edge/common-databus-payload-format
#
# Copyright (c) Siemens 2023
#
# This file is subject to the terms and conditions of the MIT License.  
# See LICENSE file in the top-level directory

import paho.mqtt.client as mqtt     # mqtt client for interacting with the databus
import json                         # storing and exchanging data via JSON file
import datetime                     # for current timestamp
import time                         # for sleep function

APP_NAME = "Custom Connector"
CONFIG_FILE = '/cfg-data/config.json'
MQTT_BROKER = 'ie-databus'

global MQTT_USER
global MQTT_PASSWORD
global APP_INSTANCE_ID
global CONNECTION
global COLLECTION
global MQTT_METADATA_TOPIC
global MQTT_DATA_READ_TOPIC
global MQTT_DATA_WRITE_TOPIC
global MQTT_STATUS_TOPIC
global METADATA_JSON
global CONNECTED_FLAG               # create flag for tracking connection state
global CONNECTOR_STATUS
global CONNECTION_STATUS
global STATUS_JSON
global meta_json_string
global status_json_string

MQTT_USER = "edge"                  # default
MQTT_PASSWORD = "edge"              # default
APP_INSTANCE_ID = "custom1"         # default
CONNECTION = "Connection_1"         # default
COLLECTION = "Collection_1"         # default

MQTT_METADATA_TOPIC = ""
MQTT_DATA_READ_TOPIC = ""
MQTT_DATA_WRITE_TOPIC = ""
MQTT_STATUS_TOPIC = ""
METADATA_JSON = ""

CONNECTED_FLAG = False
CONNECTOR_STATUS = "available"          # Connector started up and just established connection to Databus. Status of underlying driver and connections is not yet known. This is the "birth" message
CONNECTION_STATUS = "bad"               # Connection to device is not working as expected, communication to device will not work.
STATUS_JSON = ""
meta_json_string = ""
status_json_string = ""

#============================
# Reading Configuration
#============================

def read_parameter(jsonfile):
    
    print(f'Start: Read params from {jsonfile}')
    
    with open(jsonfile) as params:
        data = json.load(params)
        return data

def publish_metadata(client):
    pub = client.publish(MQTT_METADATA_TOPIC, meta_json_string, retain=True)    # retain: the message will be set as the “last known good”/retained message for the topic
    print(f"Metadata: Published metadata topic ({MQTT_METADATA_TOPIC}) with result = {pub}")

def publish_statusdata(client):

    global STATUS_JSON
    global status_json_string

    # Metadata JSON
    STATUS_JSON = {
        "seq":1,
        "ts":str(datetime.datetime.now()),
        "connector":{"status": CONNECTOR_STATUS},
        "connections":
        [
            {"name": CONNECTION, "status": CONNECTION_STATUS}
        ]
    }

    status_json_string = json.dumps(STATUS_JSON)
    pub = client.publish(MQTT_STATUS_TOPIC, status_json_string, retain=True)    # retain: the message will be set as the “last known good”/retained message for the topic
    
    print(f"Status: Published status topic ({MQTT_STATUS_TOPIC}) with result = {pub}")
    print(f"Status: Status payload = {STATUS_JSON}")
    

#============================
# Callback functions
#============================

#as soon as the client connects successfully, it listens if new data is coming in the custom connector
def on_connect(client, userdata, flags, rc):

    global CONNECTED_FLAG
    global CONNECTOR_STATUS
    global CONNECTION_STATUS
        
    if rc == 0: # 0 = connection successful 
       
        print(f"Connect: {APP_NAME} connected successfully")
        
        # =======> HIER WEITER
        # Kennt die globalen Variablen in dieser Funktion nicht!!!
              
        CONNECTED_FLAG = True           # temp flag for tracking the connectin      
        CONNECTOR_STATUS = "good"       # Connector is running, connections to Databus and underlying driver are established
        CONNECTION_STATUS = "good"      # Connection to device is up. Device is in running state.
        
        # Publish Metadata
        publish_metadata(client)
                
    else:
        print("Connect: Connection failed!")
        CONNECTOR_STATUS = "bad"        # Connector is running, but not fully functional
        CONNECTION_STATUS = "bad"       # Connection to device is not working as expected, communication to device will not work.
        return
        
    # Publish status data
    publish_statusdata(client)

def on_disconnect(client, userdata, rc):

    global CONNECTED_FLAG
    global CONNECTOR_STATUS
    global CONNECTION_STATUS
        
    print(f"Disconnect: {APP_NAME} is disconnected")
    CONNECTED_FLAG = False
    CONNECTOR_STATUS = "unavailable"    # Connector lost connection to Databus. This is the "last will" message.
    CONNECTION_STATUS = "bad"           # Connection to device is not working as expected, communication to device will not work.
    
    # Publish status data
    publish_statusdata(client)
    
    print("Disconnect: END of LOOP") 
    client.loop.stop()

def on_message(client, userdata, message):
    print(f"Message: Recieved message = {message.payload} on topic = {message.topic}")
 
    # If data is coming in on write topic, write this data on output topic (data read topic)
    if message.topic == MQTT_DATA_WRITE_TOPIC: 
    
        # write input data on dedicated topic (data read topic)
        client.publish(MQTT_DATA_READ_TOPIC, message.payload)
    
    # ignore all other topics
    else:
        return
    

#============================
# Main function
#============================

print("Start: >>> Starting custom connector application")

# Read config file if existing
try:
    print("Start: Read configuration file")
    params = read_parameter(CONFIG_FILE)
    
    MQTT_USER = params['MQTT_USER']
    MQTT_PASSWORD = params['MQTT_PASSWORD']
    APP_INSTANCE_ID = params['APP_INSTANCE_ID']
    CONNECTION = params['CONNECTION']
    COLLECTION = params['COLLECTION']
    
# If no config file exists, configure with default values
except:
    print("Start: Warning - no config file available! Using default values...")
  
    # MQTT_METADATA_TOPIC = 'ie/m/j/simatic/v1/custom1/dp'
    # MQTT_DATA_READ_TOPIC = 'ie/d/j/simatic/v1/custom1/dp/r/Connection_1/Collection_1'
    # MQTT_DATA_WRITE_TOPIC = 'ie/d/j/simatic/v1/custom1/dp/w/Connection_1/Collection_1'
    # MQTT_STATUS_TOPIC = 'ie/s/j/simatic/v1/custom1/status'
    

#create MQTT topics out of config file
MQTT_METADATA_TOPIC = 'ie/m/j/simatic/v1/' + APP_INSTANCE_ID + '/dp'
MQTT_DATA_READ_TOPIC = 'ie/d/j/simatic/v1/' + APP_INSTANCE_ID + '/dp/r/' + CONNECTION + '/' + COLLECTION
MQTT_DATA_WRITE_TOPIC = 'ie/d/j/simatic/v1/' + APP_INSTANCE_ID + '/dp/w/' + CONNECTION + '/' + COLLECTION
MQTT_STATUS_TOPIC = 'ie/s/j/simatic/v1/' + APP_INSTANCE_ID + '/status'

print(f"Start: MQTT_USER = {MQTT_USER}")
print(f"Start: MQTT_PASSWORD = {MQTT_PASSWORD}")
print(f"Start: APP_INSTANCE_ID = {APP_INSTANCE_ID}")
print(f"Start: CONNECTION = {CONNECTION}")
print(f"Start: COLLECTION = {COLLECTION}")
print(f"Start: MQTT_METADATA_TOPIC = {MQTT_METADATA_TOPIC}")
print(f"Start: MQTT_DATA_READ_TOPIC = {MQTT_DATA_READ_TOPIC}")
print(f"Start: MQTT_DATA_WRITE_TOPIC = {MQTT_DATA_WRITE_TOPIC}")
print(f"Start: MQTT_STATUS_TOPIC = {MQTT_STATUS_TOPIC}")


# Create metadata
# ----------------------------
print("Start: Create metadata")

# Metadata JSON (fix definition)
METADATA_JSON = {
    "seq":1,
    "hashVersion":123456789,
	"applicationName":"Custom Connector V2.0",
	"statustopic":MQTT_STATUS_TOPIC,
    "connections":
    [
        {
            "name":CONNECTION,
            "type":"simulated",
            "dataPoints":
            [
                {
                    "name":COLLECTION,
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

print(f"Start: Metadata payload = {METADATA_JSON}")

meta_json_string = json.dumps(METADATA_JSON)


# Configure MQTT client
# ---------------------

print("Start: Configure MQTT client")

client = mqtt.Client(client_id = APP_NAME)

#set username and password, must be created it databus configurator
client.username_pw_set(MQTT_USER,MQTT_PASSWORD)

#add callback functions
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# Start client
# ------------
print("Start: Start MQTT client")
client.connect(MQTT_BROKER)

# subscribe to write data topic and listen, if data is written
ret = client.subscribe(MQTT_DATA_WRITE_TOPIC)
print(f"Start: Subscribed to write topic ({MQTT_DATA_WRITE_TOPIC}) with result = {ret}")

# MQTT loop
# ---------
# clients always waits for messages
# loop_forever() method blocks the program, and is useful when the program must run indefinitely
client.loop_forever()
