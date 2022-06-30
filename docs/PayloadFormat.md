# Format of Common Databus Payload

- [Format of Common Databus Payload](#format-of-common-databus-payload)
  - [Overview](#overview)
  - [Databus broker](#databus-broker)
  - [Topics](#topics)
  - [Operations](#operations)
    - [Get metadata (subDpMetadataSimaticV1)](#get-metadata-subDpMetadataSimaticV1)
    - [Read datapoint values (subDpValueSimaticV1)](#read-datapoint-values-subDpValueSimaticV1)
  - [Messages](#messages)
    - [Metadata (dpMetadataSimaticV1)](#metadata-dpMetadataSimaticV1)
    - [Datapoints (subDpValueSimaticV1Msg)](#datapoints-subDpValueSimaticV1Msg)
  
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

- **ie**      = industrial edge
- **m**       = metadata / **d** = data / **s** = status
- **j**       = JSON format
- **simatic** = SIMATIC schema
- **v1**      = major version of the SIMATIC payload

## Operations

### Get metadata (subDpMetadataSimaticV1)

This subscription gets the Metadata of a connector.

Topic: **`ie/m/j/simatic/v1/{providerAppInstanceId}/dp`**

- **{providerAppInstanceId}**      = the instance id of an app, like it is already defined for available Edge apps

Example for S7 Connector: `ie/m/j/simatic/v1/s7c1/dp`

The dedicated message payload in JSON format is described [here](#metadata-dpmetadatasimaticv1).

### Read datapoint values (subDpValueSimaticV1)

This subscription reads datapoint values of a connector.

Topic: **`ie/d/j/simatic/v1/{providerAppInstanceId}/dp/r{dpConnectionNamePath}{dpCollectionNamePath}`**

- **{providerAppInstanceId}**      = the instance id of an app, like it is already defined for available Edge apps
- **{dpConnectionNamePath}**      = the connection name including '/'
- **{dpCollectionNamePath}**      = the collection name including '/'1, e.g. "/default"

Example for S7 Connector: `ie/d/j/simatic/v1/s7c1/dp/r/Plc/default`

The dedicated message payload in JSON format is described [here](#datapoints-subdpvaluesimaticv1msg).

## Messages

Each Operation responds with a dedicated message. Below the payload formats are described.

### Metadata (dpMetadataSimaticV1)

This payload contains the metadata.

```json
{"seq":1,"hashVersion":767858540,"connections":
  [{"name":"Plc","type":"S7","dataPoints":
    [{"name":"default","topic":"ie/d/j/simatic/v1/s7c1/dp/r/Plc/default","publishType":"bulk","dataPointDefinitions":
      [
        {"name":"machineState","id":"101","dataType":"Int","accessMode":"rw","acquisitionCycleInMs":500,"acquisitionMode":"CyclicContinuous"},
        {"name":"numberProduced","id":"102","dataType":"DInt","accessMode":"rw","acquisitionCycleInMs":500,"acquisitionMode":"CyclicContinuous"}
      ]
    }]
  }]
}
```

### Datapoints (subDpValueSimaticV1Msg)

This payload contains the datapoint values.

```json
{"seq":4,"vals":
  [{"id":"107","qc":3,"ts":"2022-06-30T12:08:00.7318090Z","val":645.9671020507812},
  {"id":"108","qc":3,"ts":"2022-06-30T12:08:00.7318090Z","val":7.897408962249756},
  {"id":"110","qc":3,"ts":"2022-06-30T12:08:00.7318090Z","val":116.52999877929688},
  {"id":"111","qc":3,"ts":"2022-06-30T12:08:00.7318090Z","val":645.9671020507812}]
}
```
