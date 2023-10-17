# Common Databus Payload Format

This tutorial explains the common databus payload format and shows an example how to create a custom connector out of it.

- [Common Databus Payload Format](#common-databus-payload-format)
  - [Description](#description)
    - [Overview](#overview)
    - [General Task](#general-task)
  - [Requirements](#requirements)
    - [Prerequisites](#prerequisites)
    - [Used components](#used-components)
  - [Format of Common Databus Payload](#format-of-common-databus-payload)
  - [Custom connector](#custom-connector)
  - [Documentation](#documentation)
  - [Contribution](#contribution)
  - [License and Legal Information](#license-and-legal-information)
  - [Disclaimer](#disclaimer)

## Description

### Overview

The Industrial Edge Common Databus Payload Format defines how connectors should publish data to the IE Databus via MQTT. Connectors that fulfill this specification can then reuse the existing functionality of Industrial Edge apps in the Industrial Edge Ecosystem.

The official documentation can be found here under chapter "General Common Payload Format":

[Industrial Edge Common Databus Payload Format](https://docs.eu1.edge.siemens.cloud/apis_and_references/apis/databus/reference/index.html)

<img src="docs/graphics/overview_payload_docu.png" width=700px />

### General Task

The first section explains the **structure of the Common Databus Payload Format**. Here all possible operations and the dedicated topics are listed. Furthermore the responding messages are explained.

<img src="docs/graphics/overview_payload.png" width=550 />

The second section shows an **example of a custom connector** using this format. Here we use a simple docker app "Custom Connector App", that acts as custom connector and provides some data. The data is published to the IE Databus via MQTT and can be then used by further apps. In this case we use the IE Flow Creator to read out the data and write some data back to the custom connector.

<img src="docs/graphics/overview_app.png" width=550 />

## Requirements

### Prerequisites

- Access to an Industrial Edge Management (IEM)
- Onboarded Industial Edge Device (IED) on IEM
- IEM: Installed system configurator for Databus
- IED: Installed system app Databus
- IED: Installed app Flow Creator
- Linux VM with docker and docker-compose installed
- Installed Industrial Edge App Publisher
- HTML5-capable Internet browser (in general it is advised to use Chrome, for Linux based systems it is recommended to use Firefox)

### Used components

- Industrial Edge Management OS V1.5.2-4
  - Databus Configurator V2.1.0-3
- Industrial Edge Management App V1.13.10
  - Databus V 2.1.0-4
  - Flow Creator V1.15.0-2
- Industrial Edge Device V 1.12.0-10
- Industrial Edge App Publisher V1.11.5
- Docker Engine V24.0.5
- Docker Compose V1.29.2

## Format of Common Databus Payload

You can find a detailed description of the Common Databus Payload Format here:

1. [Overview](/docs/payload-format/PayloadFormat.md#overview)
2. [Databus broker](/docs/payload-format/PayloadFormat.md#databus-broker)
3. [Topics](/docs/payload-format/PayloadFormat.md#topics)
4. [Operations](/docs/payload-format/PayloadFormat.md#operations)
5. [Messages](/docs/payload-format/PayloadFormat.md#messages)

## Custom connector

To successfully run the example app "Custom Connector App", you need to follow these steps:

1. [Build application](/docs/custom-connector/CustomConnector.md#build-application)
2. [Upload application to the Industrial Edge Management](/docs/custom-connector/CustomConnector.md#upload-application-to-the-industrial-edge-management)
3. [Create configuration for the application](/docs/custom-connector/CustomConnector.md#create-configuration-for-the-application)
4. [Install the application](/docs/custom-connector/CustomConnector.md#install-the-application)
5. [Test the application](/docs/custom-connector/CustomConnector.md#test-the-application)
  
## Documentation

You can find further documentation and help in the following links:

- [Industrial Edge Hub](https://iehub.eu1.edge.siemens.cloud/#/documentation)
- [Industrial Edge Forum](https://www.siemens.com/industrial-edge-forum)
- [Industrial Edge landing page](https://new.siemens.com/global/en/products/automation/topic-areas/industrial-edge/simatic-edge.html)
- [Industrial Edge GitHub page](https://github.com/industrial-edge)
- [Industrial Edge Common Databus Payload Format](https://docs.eu1.edge.siemens.cloud/apis_and_references/apis/databus/reference/index.html)

## Contribution

Thank you for your interest in contributing. Anybody is free to report bugs, unclear documentation, and other problems regarding this repository in the Issues section.
Additionally everybody is free to propose any changes to this repository using Pull Requests.

If you are interested in contributing via Pull Request, please check the [Contribution License Agreement](Siemens_CLA_1.1.pdf) and forward a signed copy to [industrialedge.industry@siemens.com](mailto:industrialedge.industry@siemens.com?subject=CLA%20Agreement%20Industrial-Edge).

## License and Legal Information

Please read the [Legal information](LICENSE.txt).

## Disclaimer

IMPORTANT - PLEASE READ CAREFULLY:

This documentation describes how you can download and set up containers which consist of or contain third-party software. By following this documentation you agree that using such third-party software is done at your own discretion and risk. No advice or information, whether oral or written, obtained by you from us or from this documentation shall create any warranty for the third-party software. Additionally, by following these descriptions or using the contents of this documentation, you agree that you are responsible for complying with all third party licenses applicable to such third-party software. All product names, logos, and brands are property of their respective owners. All third-party company, product and service names used in this documentation are for identification purposes only. Use of these names, logos, and brands does not imply endorsement.
