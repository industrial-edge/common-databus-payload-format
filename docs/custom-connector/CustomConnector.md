# Custom Connector

- [Custom Connector](#custom-connector)
	- [Build application](#build-application)
	- [Upload application to the Industrial Edge Management](#upload-application-to-the-industrial-edge-management)
	- [Create configuration for the application](#create-configuration-for-the-application)
	- [Install the application](#install-the-application)
	- [Test the application](#test-the-application)

The Custom Connector app simulates a custom connector that was implemented based on the Common Databus Payload Format. The app includes also a MQTT client to communicate with the IE Databus. This connector uses predefined MQTT topics (according to the configuration file) for handling metadata, datapoints and status data. The app is implemented in Python.

<img src="/docs/custom-connector/graphics/app_overview.png" width=900px />

## Build application

- Download the source code to your engineering VM
- Navigate to the *src* folder and rename the example Dockerfile (Dockerfile.example) to 'Dockerfile'
- Open a console in the source code folder where the docker-compose.yml file is located
- Use command `docker-compose build` to create the docker image
- This docker image can now be used to build you app with the Industrial Edge App Publisher
- `docker images | grep custom-connector` can be used to check for the images

## Upload application to the Industrial Edge Management

Please find below a short description how to publish your application in your IEM.

- Connect your Industrial Edge App Publisher to your docker engine
- Connect your Industrial Edge App Publisher to your Industrial Edge Managment System
- Create a new application
- Add a new version for the application
- Import the [docker-compose](/docker-compose.yml) file using the **Import YAML** button
- Review, validate and create the version
- The warning `Build (sevices >> scanner-service) is not supported` can be ignored

![publisher_create](/docs/custom-connector/graphics/publisher_create.png)

- **Start Upload** to transfer the app to Industrial Edge Managment

![iem_app](/docs/custom-connector/graphics/iem_app.png)

For more detailed information please see the section for [uploading apps to the IEM](https://github.com/industrial-edge/upload-app-to-iem).

## Create configuration for the application

For this app, several parameters need to be configured in advance:

- `MQTT_USER` (string): username of the databus user; for internal MQTT client login
- `MQTT_PASSWORD` (string): password of the databus user; for internal MQTT client login
- `APP_INSTANCE_ID` (string): instance id for this app; can be any string; included in all topics
- `CONNECTION` (string): the connection name; can be any string; included in read/write topics
- `COLLECTION` (string): the collection name; can be any string; included in read/write topics

The configuration file has to be named **config.json**.

You can find a predefined version [here](/cfg-data/config.json).

```json
{
	"MQTT_USER":"edge",
	"MQTT_PASSWORD":"edge",
	"APP_INSTANCE_ID":"custom1",
	"CONNECTION":"Connection_1",
	"COLLECTION":"Collection_1"
}
```

To add a configuration, follow these steps:

- Open the Industrial Edge Management web interface
- Go to "Applications" > "My Projects"
- Open the Custom Connector application
- Click on "Configurations" > "Add Configuration"
- Enter a name and description
- Enter `./cfg-data` as host path
- Enter a template name and description
- Browse for the `config.json` file
- Click "Add"

![config_1](/docs/custom-connector/graphics/config_1.png)

## Install the application

To install the application on an Industrial Edge Device, follow these steps:

- Open the Industrial Edge Management web interface
- Go to "Applications" > "My Projects"
- Open the Custom Connector application
- Click on the install button on the right of the version you want to deploy
- In tab "Configurations" select the above created configuration (if you do not select any configuration, the app will use the default values as listet in the config.json example above)

![install_1](/docs/custom-connector/graphics/install_1.png)

- In tab "Devices" select the corresponing Industrial Edge Device

![install_2](/docs/custom-connector/graphics/install_2.png)

- Click "Install Now" and wait for the job to be finished successfully

## Test the application

You can use the Flow Creator to verify the functionality of the Custom Connector app. You can subscribe and publish to the dedicated MQTT topics by using the MQTT nodes in Flow Creator. The Custom Connector app sends it's predefined metadata every 5 seconds. The status data is also send every 5 seconds. You can write on the defined datapoints and also read out the dedicated values.

- Go to your Edge device and make sure that the apps Flow Creator and Custom Connector are installed and started
- Open the Flow Creator UI
- Import [this](/src/flows.json) flow into the Flow Creator
- Open one of the MQTT nodes and edit the server "ie-databus:1883"
- Set the databus credentials (tab "safety") and safe the settings
- Deploy the flow
- All MQTT nodes should be shown as connected now

![flow](/docs/custom-connector/graphics/flow.png)

- Read out the **metadata** by activating the dedicated debug node (published when starting/restarting the app)

- Read out the **status data** by activating the dedicated debug node (published when starting/restarting the app)

- **Write** on the datapoints by clicking the "timestamp" node (inject); 10 value sets are written automatically on the dedicated topic

- **Read** out the datapoint values by activating the dedicated debug node
