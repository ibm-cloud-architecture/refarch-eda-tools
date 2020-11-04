# Kafka Connector

This folder includes configuration scripts and files to build a docker image with three potential Kafka connectors: JDBC sink, RabbitMQ source and MQ Sink.

## How to build the connector

* Start the setup script which should ask you what are the connectors you want to use: RabbitMQ source, JDBC sink, MQ sink.

```shell
./setupConnectors.sh
```

The script clone the  github source repository for each selected connector and then compile, package each of then and save the uber jars to the libs folder.

* Build a docker image for these connectors:

```shell
docker build -t ibmcase/kconnect:0.1.0  .
```

This image will be used in the different lab.