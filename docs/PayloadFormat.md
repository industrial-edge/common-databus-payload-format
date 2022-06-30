# Format of Common Databus Payload

- [Format of Common Databus Payload](#format-of-common-databus-payload)
  - [Overview](#overview)
  - [Databus broker](#databus-broker)
  - [Topics](#topics)
  - [Operations](#operations)
    - [Get metadata (subDpMetadataSimaticV1)](#get-metadata-subdpmetadatasimaticv1)
    - [Read datapoint values (subDpValueSimaticV1)](#read-datapoint-values-subdpvaluesimaticv1)
    - [Write datapoint values (pubDpValueSimaticV1)](#write-datapoint-values-pubdpvaluesimaticv1)
  - [Messages](#messages)
    - [Metadata (dpMetadataSimaticV1)](#metadata-dpmetadatasimaticv1)
    - [Read datapoints (subDpValueSimaticV1Msg))](#read-datapoints-subdpvaluesimaticv1msg)
    - [Write datapoints (pubDpValueSimaticV1Msg))](#write-datapoints-pubdpvaluesimaticv1msg)
  
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

A client can **subscribe** to this topic to get the metadata.

Topic: **`ie/m/j/simatic/v1/{providerAppInstanceId}/dp`**

- **{providerAppInstanceId}**     = the instance id of an app, like it is already defined for available Edge apps

Example for S7 Connector: `ie/m/j/simatic/v1/s7c1/dp`

The dedicated message payload in JSON format is described [here](#metadata-dpmetadatasimaticv1).

### Read datapoint values (subDpValueSimaticV1)

A client can **subscribe** to this topic to read datapoint values.

Topic: **`ie/d/j/simatic/v1/{providerAppInstanceId}/dp/r{dpConnectionNamePath}{dpCollectionNamePath}`**

- **{providerAppInstanceId}**     = the instance id of an app, like it is already defined for available Edge apps
- **{dpConnectionNamePath}**      = the connection name including '/'
- **{dpCollectionNamePath}**      = the collection name including '/'1, e.g. "/default"

Example for S7 Connector: `ie/d/j/simatic/v1/s7c1/dp/r/Plc/default`

The dedicated message payload in JSON format is described [here](#datapoints-subdpvaluesimaticv1msg).

### Write datapoint values (pubDpValueSimaticV1)

A client can **publish** a message to this topic to write datapoint values.

Topic: **`ie/d/j/simatic/v1/{providerAppInstanceId}/dp/w{dpConnectionNamePath}{dpCollectionNamePath}`**

- **{providerAppInstanceId}**     = the instance id of an app, like it is already defined for available Edge apps
- **{dpConnectionNamePath}**      = the connection name including '/'
- **{dpCollectionNamePath}**      = the collection name including '/'1, e.g. "/default"

Example for S7 Connector: `ie/d/j/simatic/v1/s7c1/dp/w/Plc/default`

The dedicated message payload in JSON format is described [here](#write-datapoints-pubDpValueSimaticV1Msg).

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
        {"name":"numberProduced","id":"102","dataType":"DInt","accessMode":"rw","acquisitionCycleInMs":500,"acquisitionMode":"CyclicContinuous"},
        {"name":"numberFaulty","id":"103","dataType":"DInt","accessMode":"rw","acquisitionCycleInMs":500,"acquisitionMode":"CyclicContinuous"},
        {"name":"tankLevel","id":"104","dataType":"Real","accessMode":"rw","acquisitionCycleInMs":500,"acquisitionMode":"CyclicContinuous"}
      ]
    }]
  }]
}
```

### Read datapoints (subDpValueSimaticV1Msg)

This payload contains the datapoint values, that have been read.

```json
{"seq":12571,"vals":
  [
    {"id":"101","qc":3,"ts":"2022-06-30T13:52:52.0219440Z","val":3},
    {"id":"102","qc":3,"ts":"2022-06-30T13:52:52.0219440Z","val":1091},
    {"id":"103","qc":3,"ts":"2022-06-30T13:52:52.0219440Z","val":0},
    {"id":"104","qc":3,"ts":"2022-06-30T13:52:52.0219440Z","val":0.02729782462120056}]
}
```

### Write datapoints (pubDpValueSimaticV1Msg)

This payload contains the datapoint values, that shall be written.

```
{"seq":{seq},"vals":
  [
    {"id":"{id_1}","val":{val_1},"ts":"{ts_1}","qc":{qc_1},"qx":{qx_1}},
    {"id":"{id_2}","val":{val_2},"ts":"{ts_2}","qc":{qc_2},"qx":{qx_2}}
  ]
}
```

- **{seq}**     = [integer] the sequence number (optional)
- **{id}**    = [string] unique id (string) of one datapoint, as defined in metadata (**required**)
- **{val}**   = [integer/number/string/array] value of the tag, must fit to datapoint definition in metadata (**required**)
- **{ts}**      = [string] timestamp of the datapoint, e.g. "2020-11-23T16:35:41.1234567Z" (optional)
- **{qc}**      = [integer] quality of the value, see table below (optional)
- **{qx}**      = [integer] extended quality of the value (optional)

Quality values

qc    | description
----- | ------
0     | BAD - The dp value is not useful
1     | UNCERTAIN - The quality of the dp value is less than normal, but the value may still be useful
2     | GOOD (non-cascade) - The quality of the dp value is good
3     | GOOD (cascade) - The quality of the dp value is good and may be used in control

Example of payload:

```json
{"seq":1,"vals":
  [
    {"id":"101","val":1},
    {"id":"102","val":1000},
    {"id":"103","val":10},
    {"id":"104","val":10.10}
  ]
}
```
