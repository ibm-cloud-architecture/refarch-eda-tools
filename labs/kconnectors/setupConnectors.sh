#!/bin/bash
echo "##########################################################"
echo " Set up different IBM Kafka connectors. This tool will ask"
echo " which connectors to install , build the jars and copy "
echo " them in the libs folder, which will be used by the docker"
echo " build process"
echo "##########################################################"
echo

echo "Do you want to use IBM MQ sink [Y/n] ?"
read response
if [[ "$response" != "n"  ]]
then
   git clone https://github.com/ibm-messaging/kafka-connect-mq-sink
   cd kafka-connect-mq-sink
   mvn clean  package
   cp ./target/kafka-connect*jar-with-dependencies.jar ../libs/
   cd ..
fi

echo "Do you want to use IBM JDBC sink [Y/n] ?"
read response
if [[ "$response" != "n"  ]]
then
   git clone https://github.com/ibm-messaging/kafka-connect-jdbc-sink.git
   cd kafka-connect-jdbc-sink
   mvn clean  package
   cp ./target/kafka-connect*jar-with-dependencies.jar ../libs/
   cd ..
fi

echo "Do you want to use IBM RabbitMQ source [Y/n] ?"
read response
if [[ "$response" != "n"  ]]
then
   git clone https://github.com/ibm-messaging/kafka-connect-rabbitmq-source
   cd kafka-connect-rabbitmq-source
   mvn clean  package
   cp ./target/kafka-connect*jar-with-dependencies.jar ../libs/
   cd ..
fi
