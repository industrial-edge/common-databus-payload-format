# Format of Common Databus Payload

- [Format of Common Databus Payload](#format-of-common-databus-payload)
  - [Overview](#overview)
  - [Databus broker](#databus-broker)
  - [Topics](#topics)
  - [Operations](#operations)
    - [Get metadata (subDpMetadataSimaticV1)](#get-metadata-subdpmetadatasimaticv1)
    - [Read datapoint values (subDpValueSimaticV1)](#read-datapoint-values-subdpvaluesimaticv1)
    - [Write datapoint values (pubDpValueSimaticV1)](#write-datapoint-values-pubdpvaluesimaticv1)
    - [Get connector status (subDiagConnectorStatus)](#get-connector-status-subdiagconnectorstatus)
  - [Messages](#messages)
    - [Metadata (dpMetadataSimaticV1)](#metadata-dpmetadatasimaticv1)
    - [Read datapoints (subDpValueSimaticV1Msg))](#read-datapoints-subdpvaluesimaticv1msg)
    - [Write datapoints (pubDpValueSimaticV1Msg))](#write-datapoints-pubdpvaluesimaticv1msg)
    - [Connector status (subDiagConnectorStatusMsg)](#connector-status-subdiagconnectorstatusmsg)
  
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

The metadata provides information about the data structure of a connector. A client can **subscribe** to this topic to get the metadata.

Topic: **`ie/m/j/simatic/v1/{providerAppInstanceId}/dp`**

- **{providerAppInstanceId}**     = the instance id of an app, like it is already defined for available Edge apps (e.g. *s7c1* for S7 Connector), for this example we use ***custom1***

Example for Custom Connector: **`ie/m/j/simatic/v1/custom1/dp`**

The dedicated message payload in JSON format is described [here](#metadata-dpmetadatasimaticv1).

Using the IE Flow Creator, it could look like this:

![operation_get_metadata](/docs/graphics/operation_get_metadata.png)

### Read datapoint values (subDpValueSimaticV1)

A client can **subscribe** to this topic to read datapoint values.

Topic: **`ie/d/j/simatic/v1/{providerAppInstanceId}/dp/r{dpConnectionNamePath}{dpCollectionNamePath}`**

- **{providerAppInstanceId}**     = the instance id of an app, for this example we use ***custom1***
- **{dpConnectionNamePath}**      = the connection name including '/', for this example we use ***CustomConnector***
- **{dpCollectionNamePath}**      = the collection name including '/'1, e.g. "/default"

Example for Custom Connector: **`ie/d/j/simatic/v1/custom1/dp/r/CustomConnector/default`**

The dedicated message payload in JSON format is described [here](#datapoints-subdpvaluesimaticv1msg).

Using the IE Flow Creator, it could look like this:

![operation_read_data](/docs/graphics/operation_read_data.png)

### Write datapoint values (pubDpValueSimaticV1)

A client can **publish** a message to this topic to write datapoint values.

Topic: **`ie/d/j/simatic/v1/{providerAppInstanceId}/dp/w{dpConnectionNamePath}{dpCollectionNamePath}`**

- **{providerAppInstanceId}**     = the instance id of an app, for this example we use ***custom1***
- **{dpConnectionNamePath}**      = the connection name including '/', for this example we use ***CustomConnector***
- **{dpCollectionNamePath}**      = the collection name including '/'1, e.g. "/default"

Example for Custom Connector: **`ie/d/j/simatic/v1/custom1/dp/w/CustomConnector/default`**

The dedicated message payload in JSON format is described [here](#write-datapoints-pubDpValueSimaticV1Msg).

Using the IE Flow Creator, it could look like this:

![operation_write_data](/docs/graphics/operation_write_data.png)

### Get connector status (subDiagConnectorStatus)

A client can **subscribe** to this topic to get the current status of a connector and it's connections.

Topic: **`ie/s/j/simatic/v1/{providerAppInstanceId}/status`**

- **{providerAppInstanceId}**     = the instance id of an app, for this example we use ***custom1***

Example for Custom Connector: **`ie/s/j/simatic/v1/custom1/status`**

The dedicated message payload in JSON format is described [here](#connector-status-subdiagconnectorstatusmsg).

Using the IE Flow Creator, it could look like this:

![operation_get_status](/docs/graphics/operation_get_status.png)

## Messages

Each Operation responds with a dedicated message. Below the payload formats are described.

### Metadata (dpMetadataSimaticV1)

This payload contains the metadata.

```json
{"seq":1,"connections":
  [{"name":"CustomConnector","type":"simulated","dataPoints":
    [{"name":"default","topic":"ie/d/j/simatic/v1/custom1/dp/r/CustomConnector/default","publishType":"bulk","dataPointDefinitions":
      [
        {"name":"Datapoint_Bool","id":"101","dataType":"Bool"},
        {"name":"Datapoint_Int","id":"102","dataType":"Int"},
        {"name":"Datapoint_Real","id":"103","dataType":"Real"}
      ]
    }]
  }]
}
```

### Read datapoints (subDpValueSimaticV1Msg)

This payload contains the datapoint values, that have been read.

```json
{"seq":1,"vals":
  [
    {"id":"101","qc":3,"ts":"2022-07-21T13:01:50.159Z","val":true},
    {"id":"102","qc":3,"ts":"2022-07-21T13:01:50.159Z","val":123},
    {"id":"103","qc":3,"ts":"2022-07-21T13:01:50.159Z","val":9.99}
  ]
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
{
    "seq": 1,
    "vals":[
        {"id":"101","qc":3,"ts":"2022-07-21T13:01:50.159Z","val":true},
        {"id":"102","qc":3,"ts":"2022-07-21T13:01:50.159Z","val":123},
        {"id":"103","qc":3,"ts":"2022-07-21T13:01:50.159Z","val":9.99}
    ]
}
```

### Connector status (subDiagConnectorStatusMsg)

This payload contains the connector status.

```json
{"seq":2,"ts":"2022-07-26T06:45:17Z","connector":
  {"status":"good"},"connections":
    [
      {"name":"CustomConnector","status":"bad"}
    ]
}
```
