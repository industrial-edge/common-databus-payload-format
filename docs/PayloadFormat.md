# Format of Common Databus Payload

- [Format of Common Databus Payload](#format-of-common-databus-payload)
  - [Overview](#overview)
  - [Databus broker](#databus-broker)
  - [Topics](#topics)
  - [Operations](#operations)
    - [Get metadata (subscription)](get-metadata-subsription)
    - [Read datapoint values (subscription)](read-datapoint-values-subscription)
  - [Messages](#messages)
    - [Simatic Metadata](#simatic-metadata)
  
## Overview

This page describes the Common Databus Payload Format, which implementation is mandatory for all Edge apps to communicate with the IE Databus. The data exchange is based on MQTT, where we have a broker (server) and one or more clients. The communication between the clients works via topics, where clients can publish data or subscribe to receive data. Besides the topic, each MQTT message also contains a payload, where the message text is stored.

The official documentation can be found here under chapter "General Common Payload Format":

[Industrial Edge Common Databus Payload Format](https://industrial-edge.io/developer/systemapps/data-processing/databus/reference/index.html)

![mqtt](/docs/graphics/mqtt.png)

## Databus broker

The IE Databus acts as MQTT broker within the Edge Ecosystem. The broker filters all incoming messages and distributes data to certain topics. Therefore, if you want to implement an own app that uses the Common Databus Payload Format, you also need to implement a MQTT client inside your app.

DNS name of the IE Databus broker:

**`mqtt://ie-databus:1883`**

## Topics

Topics are a form of defined addresses that allow MQTT clients to share information. They are structured in a hierarchy, using a *'/'* as delimiter. Edge apps can publish and subscribe to topics.

Within the Edge Ecosystem we have a fixed structure of topics:

**`ie/m/j/simatic/v1/...`**

- ***ie***      = industrial edge
- ***m***       = metadata / *d* = data / *s* = status
- ***j***       = JSON format
- ***simatic*** = SIMATIC schema
- ***v1***      = major version of the SIMATIC payload

## Operations

### Get metadata (subscription)

This operation gets the Metadata of a connector.

Topic: **`ie/m/j/simatic/v1/{providerAppInstanceId}/dp`**

*{providerAppInstanceId}* is the instance id of an app, like it is already defined for available Edge apps (e.g. *s7c1* for the S7 Connector or *eip1* for the Ethernet IP Connector)

Example for S7 Connector: `ie/m/j/simatic/v1/s7c1/dp`

The dedicated message payload in JSON format is described [here](#simatic-metadata).

### Read datapoint values (subscription)

This operation reads Simatic datapoint values of a connector in JSON format.

Topic: `ie/d/j/simatic/v1/{providerAppInstanceId}/dp/r{dpConnectionNamePath}{dpCollectionNamePath}`

Parameter 'providerAppInstanceId' = the instance id of an app, like it is already defined for available Edge apps (e.g. "s7c1" for the S7 Connector or "eip1" for the Ethernet IP Connector)

Parameter 'dpConnectionNamePath' = the connection name including '/'

Parameter 'dpCollectionNamePath' = the collection name including '/'1, e.g. "/default"

Example for S7 Connector: `ie/d/j/simatic/v1/s7c1/dp/r/Plc/default`

The dedicated message payload in JSON format is described [here](#simatic-metadata).

## Messages

Each Operation responds with a dedicated message. Below the payload formats are described.

### Simatic Metadata

This payload contains the Simatic Metadata (dpMetadataSimaticV1).

```json
{"seq":1,"hashVersion":3776821982,"connections":
    [{"name":"Plc","type":"OPCUA","dataPoints":
        [{"name":"default","topic":"ie/d/j/simatic/v1/s7c1/dp/r/Plc/default","publishType":"bulk","dataPointDefinitions":
            [{"name":"GDB.operate.machineState","id":"101","dataType":"Int","accessMode":"r","acquisitionCycleInMs":100,"acquisitionMode":"CyclicOnChange"},
             {"name":"GDB.signals.energySignals.energyConsumptionFillingTank","id":"102","dataType":"Real","accessMode":"r","acquisitionCycleInMs":100,"acquisitionMode":"CyclicOnChange"}
            ]
        }]
    }]
}

```

subDpValueSimaticV1Msg
