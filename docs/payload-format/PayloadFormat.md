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

![mqtt](/docs/payload-format/graphics/mqtt.png)

## Databus broker

The IE Databus is an MQTT broker within the Edge Ecosystem, which is by default only reachable within an Edge Device. The broker receives all incoming messages and distributes data to agents for their subscribed topics. Therefore, if you want to implement an own app that uses the Common Databus Payload Format, you also need to implement a MQTT client inside your app.

DNS name of the IE Databus broker:

**`mqtt://ie-databus:1883`**

## Topics

Topics are a form of defined addresses that allow MQTT clients to share information. They are structured in a hierarchy, using a *'/'* as delimiter. Edge apps can publish and subscribe to topics.

Within the Edge Ecosystem we have a fixed structure of topics:

**Topic: `ie/m/j/simatic/v1/...`**

- `ie`= industrial edge
- `m/d/s`= **m** = metadata / **d** = data / **s** = status ({mqttPayloadType})
- `j`= JSON format ({mqttPayloadEncoding})
- `simatic`= name for the SIMATIC schema ({msgStructureScheme})
- `v1`= major version of the SIMATIC payload schema ({msgStructureSchemeMajorVersion})

## Operations

### Get metadata (subDpMetadataSimaticV1)

The metadata provides information about the data structure of a connector. A client can **subscribe** to this topic to get the metadata.

**Topic: `ie/m/j/simatic/v1/{providerAppInstanceId}/dp`**

- `{providerAppInstanceId}`: The instance id of an app, like it is already defined for available Edge apps (e.g. *s7c1* for S7 Connector), for this example we use *'custom1'*
- `dp`: message type "datapoints" (`{mqttPayloadMsgType}`)

**Example: `ie/m/j/simatic/v1/custom1/dp`**

Please see the dedicated [message payload](#metadata-dpmetadatasimaticv1).

**Flow Creator example**

![operation_get_metadata](/docs/payload-format/graphics/operation_get_metadata.png)

### Read datapoint values (subDpValueSimaticV1)

A client can **subscribe** to this topic to read datapoint values.

**Topic: `ie/d/j/simatic/v1/{providerAppInstanceId}/dp/r{dpConnectionNamePath}{dpCollectionNamePath}`**

- `{providerAppInstanceId}`:  the instance id of an app, for this example we use *'custom1'*
- `dp`:                       message type "datapoints" (`{mqttPayloadMsgType}`)
- `r`:                        datapoint access mode "read" (`{dpAccessmode}`)
- `{dpConnectionNamePath}`:   the connection name including '/', for this example we use *'Connection_1'*
- `{dpCollectionNamePath}`:   the collection name including '/', e.g. '/default', for this example we use *'/Collection_1'*

**Example: `ie/d/j/simatic/v1/custom1/dp/r/Connection_1/Collection_1`**

Please see the dedicated [message payload](#read-datapoints-subdpvaluesimaticv1msg).

**Flow Creator example**

![operation_read_data](/docs/payload-format/graphics/operation_read_data.png)

### Write datapoint values (pubDpValueSimaticV1)

A client can **publish** a message to this topic to write datapoint values.

**Topic: `ie/d/j/simatic/v1/{providerAppInstanceId}/dp/w{dpConnectionNamePath}{dpCollectionNamePath}`**

- `{providerAppInstanceId}`:  the instance id of an app, for this example we use *'custom1'*
- `dp`:                       message type "datapoints" (`{mqttPayloadMsgType}`)
- `w`:                        datapoint access mode "write" (`{dpAccessmode}`)
- `{dpConnectionNamePath}`:   the connection name including '/', for this example we use *'Connection_1'*
- `{dpCollectionNamePath}`:   the collection name including '/', e.g. '/default', for this example we use *'/Collection_1'*

**Example: `ie/d/j/simatic/v1/custom1/dp/w/Connection_1/Collection_1`**

Please see the dedicated [message payload](#write-datapoints-pubDpValueSimaticV1Msg).

**Flow Creator example**

![operation_write_data](/docs/payload-format/graphics/operation_write_data.png)

### Get connector status (subDiagConnectorStatus)

A client can **subscribe** to this topic to get the current status of a connector and it's connections.

**Topic: `ie/s/j/simatic/v1/{providerAppInstanceId}/status`**

- `{providerAppInstanceId}`: the instance id of an app, for this example we use *'custom1'*

**Example: `ie/s/j/simatic/v1/custom1/status`**

Please see the dedicated [message payload](#connector-status-subdiagconnectorstatusmsg).

**Flow Creator example**

![operation_get_status](/docs/payload-format/graphics/operation_get_status.png)

## Messages

Each Operation responds with a dedicated message in JSON format. Below the payload formats are described.

### Metadata (dpMetadataSimaticV1)

This payload contains the metadata.

```json
{"seq":1,"hashVersion":123456789,"applicationName":"Custom Connector V1.0","statustopic":"ie/s/j/simatic/v1/custom1/status","connections":
  [
    {"name":"Connection_1","type":"simulated","dataPoints":
      [
        {"name":"Collection_1","topic":"ie/d/j/simatic/v1/custom1/dp/r/Connection_1/Collection_1","pubTopic":"ie/d/j/simatic/v1/custom1/dp/w/Connection_1/Collection_1","publishType":"bulk","dataPointDefinitions":
          [
            {"name":"Datapoint_Bool","id":"101","dataType":"Bool"},
            {"name":"Datapoint_Int","id":"102","dataType":"Int"},
            {"name":"Datapoint_Real","id":"103","dataType":"Real"}]
        }]
    }]
}
```
Metadata
- `{seq}`:          [integer] sequence number (optional)
- `{hashVersion}`:  [integer] has value to identify the version of the metadata (**required**)
- `{applicationName}`: [string] official product name of the application (optional)
- `{statustopic}`:  [string] MQTT topic name of the connector and connection status (optional)
- `{connections}`:  [array(object)] ARRAY of connections information (**required**)

Connection
- `{name}`:         [string] name of the connection (**required**)
- `{type}`:         [string] type of the connection, e.g. "s7"/"pn" (**required**)
- `{dataPoints}`:   [array(object)] ARRAY of datapoints of this connection, datapoints can be grouped into different collections (**required**)

Datapoint collection
- `{name}`:         [string] name of the datapoint collection, e.g. "default" (**required**)
- `{topic}`:        [string] MQTT topic name of the datapoint collection (**required**)
- `{pubTopic}`:     [string] MQTT topic name of the datapoint collection for writing to datapoints of the connector, required when any writeable datapoint is defined (partially required)
- `{publishType}`:  [string] type of publishing, one of "bulk"/"timeseries"/"binarytimeseries" (optional)
- `{dataPointDefinitions}`: [array(object)] datapoints of this connection (**required**)

Datapoint
- `{name}`:         [string] name of the datapoint, the name is only unique within a connection (**required**)
- `{id}`:           [string] this is a reference between the properties "id" of the datapoint definition in the metadata and the property "id" in the datapoint value, only unique within the connection and not long term stable (and can change after new configuration) (**required**)
- `{dataType}`:     [string] datatype of datapoint, one of "Bool"/"Byte"/"Word"/"DWord"/"LWord"/"SInt"/"USInt"/"Int"/"UInt"/"DInt"/"UDInt"/"LInt"/"ULInt"/"Real"/"LReal"/"Char"/"String"/"Time"/"LTime"/"DateTime"/"Date"/"Time_Of_Day"/"LTime_Of_Day" (**required**)

### Read datapoints (subDpValueSimaticV1Msg)

This payload contains the datapoint values, that have been read.

```
{"seq":1,"vals":
  [
    {"id":"101","val":false,"ts":"2022-07-21T13:01:50.159Z","qc":3},
    {"id":"102","val":4,"ts":"2022-07-21T13:01:50.159Z","qc":3},
    {"id":"103","val":4.123,"ts":"2022-07-21T13:01:50.159Z","qc":3}
  ]
}
```

Datapoints
- `{seq}`    [integer] the sequence number (optional)
- `{vals}`   [array(object)] ARRAY of data points published in the payload (**required**)

Datapoint
- `{id}`     [string] unique id (string) of one datapoint, reference to 'id' as defined in metadata (**required**)
- `{val}`    [integer/number/string/array] value of the tag, must fit to datapoint definition in metadata (**required**)
- `{ts}` :    [string] timestamp of the datapoint, e.g. "2020-11-23T16:35:41.1234567Z" (optional)
- `{qc}`     [integer] quality of the value, see table below (optional)
- `{qx}`     [integer] extended quality of the value (optional)

Quality of values

qc    | description
----- | ------
0     | BAD - The dp value is not useful
1     | UNCERTAIN - The quality of the dp value is less than normal, but the value may still be useful
2     | GOOD (non-cascade) - The quality of the dp value is good
3     | GOOD (cascade) - The quality of the dp value is good and may be used in control


### Write datapoints (pubDpValueSimaticV1Msg)

This payload contains the datapoint values, that shall be written.

```
{"seq":1,"vals":
  [
    {"id":"101","val":false,"ts":"2022-07-21T13:01:50.159Z","qc":3,"qx":0},
    {"id":"102","val":4,"ts":"2022-07-21T13:01:50.159Z","qc":3,"qx":0},
    {"id":"103","val":4.123,"ts":"2022-07-21T13:01:50.159Z","qc":3,"qx":0}
  ]
}
```

Datapoints
- `{seq}`      [integer] the sequence number (optional)
- `{vals}`     [array(object)] ARRAY of data points published in the payload (**required**)

Datapoint
- `{id}`       [string] unique id (string) of one datapoint, as defined in metadata (**required**)
- `{val}`      [integer/number/string/array] value of the tag, must fit to datapoint definition in metadata (**required**)
- `{ts}`       [string] timestamp of the datapoint, e.g. "2020-11-23T16:35:41.1234567Z" (optional)
- `{qc}`       [integer] quality of the value, see table below (optional)
- `{qx}`       [integer] extended quality of the value (optional)

Quality of values

qc    | description
----- | ------
0     | BAD - The dp value is not useful
1     | UNCERTAIN - The quality of the dp value is less than normal, but the value may still be useful
2     | GOOD (non-cascade) - The quality of the dp value is good
3     | GOOD (cascade) - The quality of the dp value is good and may be used in control

### Connector status (subDiagConnectorStatusMsg)

This payload contains the connector status.

```
{ 
  "seq":1,
  "ts":"2022-07-21T13:01:50.159Z",
  "connector": {"status":"good"},
  "connections":
    [
      {"name":"Connection_1","status":"good"}
    ]
}
```

Connector
- `{seq}`        [integer] the sequence number (optional)
- `{ts}`         [string] timestamp of the status message, e.g. "2020-11-23T16:35:41.1234567Z" (optional)
- `{connector}`  [object] properties of connector (**required**)
- `{status}`     [string] status of the connector, one of "good"/"bad"/"available"/"unavailable" (**required**)
- `{connections}` [array(object)] ARRAY of connection status information (**required**)

Connection
- `{name}`       [string] name of the connection (**required**)
- `{status}`     [string] status of the connection, one of "good"/"stopped"/"bad" (**required**)

**Connector status values**

status      | description
----------- | ------
good        | Connector is running, connections to DataBus and underlying driver are established. Everything is fine.
bad         | Connector is running, but not fully functional.
available   | Connector started up and just established connection to DataBus. Status of underlying driver and connections is not yet known. This is the "birth" message.
unavailable | Connector lost connection to DataBus. This is the "last will" message.

**Connection status values**

status      | description
----------- | ------
good        | Connection to device is up. Device is in running state.
stopped     | Connection to device is up. Device is in stopped state. No process data will be available. Only System Alarms are available from some devices (e.g. S7-1500).
bad         | Connection to device is not working as expected, communication to device will not work.
