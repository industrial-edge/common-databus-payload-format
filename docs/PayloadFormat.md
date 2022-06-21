# Format of Common Databus Payload

- [Format of Common Databus Payload](#format-of-common-databus-payload)
  - [Databus broker](#databus-broker)
  - [Operations](#operations)
    - [Datapoint metadata (Subscription)](datapoint-metadata-subsription)
    - [Read datapoint values (Subscription)](read-datapoint-values-subscription)
  - [Messages](#messages)
    - [Simatic Metadata](#simatic-metadata)
  
---

The official documentation can be found here under chapter "General Common Payload Format":

[Industrial Edge Common Databus Payload Format](https://industrial-edge.io/developer/systemapps/data-processing/databus/reference/index.html)

## Databus broker

Since the communication between the IE Databus and a connector goes via MQTT, we need to use the Industrial Edge Databus broker:

`mqtt://ie-databus:1883`

## Operations

### Datapoint metadata (Subscription)

This operation gets the Simatic Metadata of an app or connector in JSON format.

Topic: `ie/m/j/simatic/v1/{providerAppInstanceId}/dp`

Parameter 'providerAppInstanceId' = the instance id of an app, like it is already defined for available Edge apps (e.g. "s7c1" for the S7 Connector or "eip1" for the Ethernet IP Connector)

Example for S7 Connector: `ie/m/j/simatic/v1/s7c1/dp`

The dedicated message payload in JSON format is described [here](#simatic-metadata).

### Read datapoint values (Subscription)

This operation reads Simatic datapoint values of an app or connector in JSON format.

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
